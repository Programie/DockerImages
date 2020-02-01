#! /bin/bash

certs_dir="/etc/letsencrypt/live"
webroot="/webroot"
email_address="${LETSENCRYPT_EMAIL}"

certs_requested=0

create_cert()
{
    domains="$1"

    primary_domain=$(echo ${domains} | cut -d "," -f 1)

    if [[ ! -e ${certs_dir}/${primary_domain}/cert.pem ]]; then
        certbot certonly --agree-tos --email ${email_address} --rsa-key-size 4096 -n --webroot -w ${webroot} -d ${domains}
        certs_requested=1
    fi
}

base_dir=$(dirname $(readlink -f $0))
conf_file="${base_dir}/create-certs.conf"

if [[ ! -e ${conf_file} ]]; then
    exit
fi

while read -r line; do
    # trim spaces
    line=$(echo ${line})

    if [[ -z ${line} ]] || [[ ${line} = \#* ]]; then
        continue
    fi

    create_cert ${line}
done < ${conf_file}

if [[ ${certs_requested} ]]; then
    /app/restart-container.sh ${LETSENCRYPT_CONTAINER_RESTART_REQUEST}
fi