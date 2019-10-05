#! /bin/bash

certbot renew --deploy-hook "/app/restart-container.sh ${LETSENCRYPT_CONTAINER_RESTART_RENEW}"