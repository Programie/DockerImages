#! /usr/bin/env python3

import asyncio
import logging
import os
from datetime import datetime

import sys

from elasticsearch import Elasticsearch
from telethon import TelegramClient, events
from telethon.tl.types import PeerUser, User

api_id = os.getenv("TG_API_ID")
api_hash = os.getenv("TG_API_HASH")

LOG_LEVEL_INFO = 35

logging.basicConfig(format="[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s", level=logging.WARNING)
logging.addLevelName(LOG_LEVEL_INFO, "INFO")

tg_client = TelegramClient(os.getenv("SESSION_FILE", "/sessions/client.session"), api_id, api_hash)
es_client = Elasticsearch(hosts=os.getenv("ES_HOST", "elasticsearch"))


async def index_message(message):
    # Only log private messages (e.g. no group or channel messages)
    if not isinstance(message.to_id, PeerUser):
        return

    chat = await message.get_chat()
    sender_user = await message.get_sender()

    doc_data = {
        "timestamp": message.date,
        "sender": {
            "username": sender_user.username,
            "firstName": sender_user.first_name,
            "lastName": sender_user.last_name,
        },
        "chat": {
            "username": chat.username,
            "firstName": chat.first_name,
            "lastName": chat.last_name,
        },
        "message": message.text
    }

    es_client.index("telegram-{}".format(message.date.strftime("%Y.%m")), body=doc_data, id=message.id)


async def main():
    @tg_client.on(events.NewMessage())
    @tg_client.on(events.MessageEdited())
    async def handler(event):
        await index_message(event.message)

    await tg_client.catch_up()

    if "import-history" in sys.argv:
        start_date_index = sys.argv.index("import-history") + 1
        if len(sys.argv) > start_date_index:
            offset_date = datetime.strptime(sys.argv[start_date_index], "%Y-%m-%d")
        else:
            offset_date = None

        for chat in await tg_client.get_dialogs():
            if not isinstance(chat.entity, User):
                continue

            if chat.entity.bot:
                continue

            if not chat.entity.contact:
                continue

            if offset_date:
                logging.log(LOG_LEVEL_INFO, "Importing history for chat '{}' starting at {}".format(chat.title, offset_date.strftime("%c")))
            else:
                logging.log(LOG_LEVEL_INFO, "Importing full history for chat '{}'".format(chat.title))

            async for message in tg_client.iter_messages(chat, offset_date=offset_date, reverse=True):
                await index_message(message)

        logging.log(LOG_LEVEL_INFO, "Import finished")


with tg_client:
    loop = asyncio.get_event_loop()
    loop.create_task(main())

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
