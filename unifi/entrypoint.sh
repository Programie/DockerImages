#! /bin/bash

if [[ ! -f "${CERTDIR}/${CERTNAME}" ]]; then
    if [[ ! -d ${CERTDIR} ]]; then
        mkdir -p ${CERTDIR}
    fi

    openssl req \
            -x509 \
            -nodes \
            -new \
            -keyout ${CERTDIR}/${CERT_PRIVATE_NAME} \
            -out ${CERTDIR}/${CERTNAME} \
            -days 3650 \
            -subj "/CN=unifi" \
            -extensions san \
            -config <(echo '[req]'; echo 'distinguished_name=req';echo '[san]'; echo 'subjectAltName=DNS:unifi,DNS:localhost')

    touch ${CERTDIR}/chain.pem
fi

/usr/local/bin/docker-entrypoint.sh "$@"