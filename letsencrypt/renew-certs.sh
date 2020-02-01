#! /bin/bash

certbot renew --rsa-key-size 4096 --deploy-hook "/app/restart-container.sh ${LETSENCRYPT_CONTAINER_RESTART_RENEW}"