#! /usr/bin/env python3
from elasticsearch import helpers as es_helpers
from elasticsearch import Elasticsearch
import argparse
import datetime
import hashlib
import logging
import time
import os

try:
    import argcomplete
except ImportError:
    argcomplete = None


def get_by_path(data, path, default=None):
    for key in path.split("."):
        if key not in data:
            return default

        data = data[key]

    return data


def submit_documents(es_client, logger, index, documents, chunk_size):
    if not documents:
        return

    actions = []

    for key, document in documents.items():
        actions.append({
            "_index": index,
            "_id": hashlib.sha256(key.encode("utf-8")).hexdigest(),
            "_source": document,
        })

    success, failed = es_helpers.bulk(client=es_client, actions=actions, chunk_size=chunk_size, stats_only=True)

    logger.debug("Bulk index completed (succeeded = {}, failed = {})".format(success, failed))

    # There are no failed requests but succeeded document inserts do not equal to the number of documents
    if not failed and success != len(documents):
        failed = len(documents) - success

    if failed:
        logger.warning("Failed to index {} documents into index '{}'".format(failed, index))


def aggregate_index(es_client, index, new_index, fields, sum_fields, keep_fields, chunk_size, logger):
    scroll_ttl = "2m"  # How long to keep the scroll context alive
    datetime_formats = ["%Y-%m-%dT%H:%M:%S.%fZ", "%Y-%m-%dT%H:%M:%SZ"]  # Datetime format used by Logstash

    start_time = time.time()
    datetime_start = datetime.datetime.now()

    logger.debug("Searching documents for index '{}'".format(index))

    response = es_client.search(
        index=index,
        scroll=scroll_ttl,
        size=1000,
        sort=[
            {
                "@timestamp": {
                    "order": "asc"
                }
            }
        ]
    )

    scroll_id = response["_scroll_id"]
    total_documents = response["hits"]["total"]["value"]
    scroll_size = total_documents

    logger.info("Found {} documents in index '{}'".format(total_documents, index))

    logger.debug("scroll_id = {}, scroll_size = {}".format(scroll_id, scroll_size))

    if not scroll_size:
        logger.error("No documents found in index '{}'".format(index))
        return

    iteration = 0
    current_timestamp = None
    documents = {}
    document_count = 0
    processed_documents_count = 0
    total_count = 0
    current_documents_percentage = None

    while scroll_size > 0:
        iteration += 1

        logger.debug("Aggregating {} documents".format(scroll_size))

        documents_processing_start_time = time.time()

        for document in response["hits"]["hits"]:
            processed_documents_count += 1

            source = document["_source"]
            timestamp = None

            for datetime_format in datetime_formats:
                try:
                    timestamp = datetime.datetime.strptime(source["@timestamp"], datetime_format).replace(second=0, microsecond=0).strftime(datetime_format)
                    break
                except ValueError:
                    pass

            if timestamp is None:
                raise ValueError("Unable to parse timestamp: {}".format(source["@timestamp"]))

            if timestamp != current_timestamp:
                current_timestamp = timestamp

                if documents:
                    if len(documents) >= chunk_size:
                        submit_documents(es_client=es_client, logger=logger, index=new_index, documents=documents, chunk_size=chunk_size)
                        document_count += len(documents)
                        documents = {}

            field_values = {
                "@timestamp": timestamp
            }

            key = timestamp

            for field in fields:
                value = get_by_path(source, field)

                field_values[field] = value

                if value is not None:
                    key += str(value)

            if key in documents:
                item = documents[key]
            else:
                logger.debug("Key for new document: {}".format(key))

                item = {
                    "count": 0
                }

                for field in sum_fields:
                    item[field] = 0

                item.update(field_values)

            for field in sum_fields:
                item[field] += int(get_by_path(source, field, 0))

            for field in keep_fields:
                item[field] = get_by_path(source, field)

            count = int(source.get("count", 1))

            total_count += count

            item["count"] += count

            documents[key] = item

        documents_percentage = processed_documents_count / total_documents * 100

        documents_processing_time = time.time() - documents_processing_start_time
        documents_per_second = len(response["hits"]["hits"]) / documents_processing_time

        # end time calculation
        elapsed_sec = time.time() - start_time
        elapsed_min = int(elapsed_sec / 60)
        if documents_percentage > 0:
            seconds_per_percent = elapsed_sec / documents_percentage
            calculated_sec_finished = seconds_per_percent * 100

            finished_min = int(calculated_sec_finished / 60)
            finished_at = datetime_start + datetime.timedelta(minutes=finished_min)
            remaining_min = finished_min - elapsed_min

            if remaining_min < 0:
                remaining_min = 0
        else:
            finished_at = "n/a"
            remaining_min = "n/a"

        documents_percentage = int(documents_percentage)

        if documents_percentage != current_documents_percentage:
            current_documents_percentage = documents_percentage

            logger.info("Processed {:02d}% in {} minutes, ETA in {} @ {} ({} docs/sec)".format(documents_percentage, elapsed_min, remaining_min, finished_at.strftime("%Y-%m-%d %H:%M:%S"), int(documents_per_second)))

        # get next scroll result
        response = es_client.scroll(scroll_id=scroll_id, scroll=scroll_ttl)
        scroll_id = response["_scroll_id"]
        scroll_size = len(response["hits"]["hits"])

    submit_documents(es_client=es_client, logger=logger, index=new_index, documents=documents, chunk_size=chunk_size)
    document_count += len(documents)

    logger.info("Aggregation of index '{}' completed in {} minutes ({} documents, count = {})".format(index, int((time.time() - start_time) / 60), document_count, total_count))


def aggregate_indices(es_client, pattern, fields, sum_fields, keep_fields, chunk_size, logger, dryrun=False):
    logger.info("Getting indices matching '{}'".format(pattern))

    indices = es_client.indices.get(index=pattern)

    logger.info("Got {} indices".format(len(indices)))

    iteration = 0
    for index in indices:
        index_without_date, date_string = index.rsplit("-", 1)

        year, month, day = date_string.split(".")
        date = datetime.date(year=int(year), month=int(month), day=int(day))
        month_string = date.strftime("%Y.%m")

        new_index = "{}-{}".format(index_without_date, month_string)

        logger.info("Aggregating data of index '{}' into '{}'".format(index, new_index))

        if not dryrun:
            aggregate_index(es_client=es_client, index=index, new_index=new_index, fields=fields, sum_fields=sum_fields, keep_fields=keep_fields, chunk_size=chunk_size, logger=logger)

        logger.info("waiting 5 seconds to complete indexing new documents")
        time.sleep(5)

        verify_delete(es_client=es_client, index=index, logger=logger, dryrun=dryrun)

        logger.info("{} indices to aggregate remaining".format(len(indices) - iteration - 1))

        iteration += 1
    return indices


def aggregate_count(es_client, search_index, logger):
    year, month, day = search_index.rsplit("-")[-1].split(".")
    index = search_index[0:-3]
    date = "{}-{}-{}".format(year, month, day)

    logger.info("summing up count in index '{}' (date: {})".format(index, date))

    raw_documents_count = 0
    indices = es_client.indices.get(index=index)
    for index in indices:
        response = es_client.search(
            index=index,
            scroll="2m",
            size=2000,
            sort=[
                {
                    "@timestamp": {
                        "order": "desc"
                    }
                }
            ]
        )

        scroll_id = response["_scroll_id"]
        iteration = 0
        scroll_size = len(response["hits"]["hits"])
        raw_documents_count = 0

        while scroll_size > 0:
            iteration += 1

            for document in response["hits"]["hits"]:
                if date in document["_source"]["@timestamp"]:
                    raw_documents_count += document["_source"]["count"]

            response = es_client.scroll(scroll_id=scroll_id, scroll="2m")
            scroll_size = len(response["hits"]["hits"])

        logger.info("summed up count: {}".format(raw_documents_count))
    return int(raw_documents_count)


def verify_delete(es_client, index, logger, dryrun):
    max_tries = 5

    for iteration in range(0, max_tries):
        aggregated_count = aggregate_count(es_client=es_client, search_index=index, logger=logger)
        index_count = es_client.count(index=index)["count"]
        logger.info("{} (original index) vs {} (aggregated)".format(index_count, aggregated_count))

        if index_count == aggregated_count:
            if dryrun:
                logger.info("counts are the same")
            else:
                wait_for_pending(es_client, logger)
                logger.info("counts are the same, nothing pending, deleting '{}'".format(index))
                es_client.indices.delete(index=index)

            break
        else:
            logger.info("counts are different")

            if iteration < max_tries - 1:
                logger.info("retrying in 10 seconds")
                time.sleep(10)


def wait_for_pending(es_client, logger):
    pending_tasks = True

    while pending_tasks:
        pending_tasks = False
        pending = es_client.cluster.pending_tasks()
        logger.info("pending tasks: {}".format(len(pending.get("tasks"))))

        for task in pending.get("tasks"):
            if task.get("priority") == "URGENT":
                pending_tasks = True
                logger.info("deleting would fail, will sleep 30s, pending task: {}".format(task.get("source")))
                time.sleep(30)
                break


def main():
    argument_parser = argparse.ArgumentParser(description="Aggregate documents in Elasticsearch")

    argument_parser.add_argument("--host", nargs="*", help="elasticsearch hosts to connect to", default=os.getenv("ES_HOST", "elasticsearch").split(","))
    argument_parser.add_argument("--timeout", "-t", help="timeout in seconds for Elasticsearch API requests (default: 60)", default=60)
    argument_parser.add_argument("--quiet", "-q", action="store_true", help="only output warnings and errors")
    argument_parser.add_argument("--verbose", "-v", action="store_true", help="be more verbose")
    argument_parser.add_argument("--dryrun", action="store_true", help="Do not write data to Elasticsearch or delete indices")
    argument_parser.add_argument("--group-field", nargs="*", help="the fields used to group the documents together", default=os.getenv("ES_GROUP_FIELDS", "").split(","))
    argument_parser.add_argument("--sum-field", nargs="*", help="the fields which should be summed up", default=os.getenv("ES_SUM_FIELDS", "").split(","))
    argument_parser.add_argument("--keep-field", nargs="*", help="the fields which should be kept (copied) without modification", default=os.getenv("ES_KEEP_FIELDS", "").split(","))
    argument_parser.add_argument("--chunk-size", help="number of documents to submit in batch", default=os.getenv("ES_CHUNK_SIZE", "1000"))

    argument_parser.add_argument("pattern", help="the search pattern used to get the indices")

    if argcomplete:
        argcomplete.autocomplete(argument_parser)

    arguments = argument_parser.parse_args()

    logger = logging.getLogger(__name__)

    if arguments.quiet:
        logger.setLevel(logging.WARNING)
    elif arguments.verbose:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    console_logger = logging.StreamHandler()
    console_logger.setFormatter(logging.Formatter("[%(asctime)s] %(levelname)s:%(name)s: %(message)s"))
    logger.addHandler(console_logger)

    elasticsearch_username = os.getenv("ES_USERNAME")
    elasticsearch_password = os.getenv("ES_PASSWORD")

    if elasticsearch_username is not None and elasticsearch_password is not None:
        elasticsearch_httpauth = [elasticsearch_username, elasticsearch_password]
    else:
        elasticsearch_httpauth = None

    es_client = Elasticsearch(hosts=arguments.host, request_timeout=int(arguments.timeout), basic_auth=elasticsearch_httpauth)

    aggregate_indices(es_client=es_client, pattern=arguments.pattern, fields=arguments.group_field, sum_fields=arguments.sum_field, keep_fields=arguments.keep_field, chunk_size=int(arguments.chunk_size), logger=logger, dryrun=arguments.dryrun)


if __name__ == "__main__":
    main()
