#! /bin/bash

shopt -s nullglob

days_warn=21
days_crit=7

for conf_file in /etc/nginx/conf.d/*.conf; do
    for cert_file in $(grep -F "# cert_check:" ${conf_file} | cut -d "#" -f 2 | cut -d ":" -f 2 | sort | uniq); do
        domain_name=$(openssl x509 -in ${cert_file} -noout -subject | tr -d ' ' | grep -E -o 'CN=(.*)' | cut -d '=' -f 2)
        expire_date=$(openssl x509 -in ${cert_file} -noout -enddate | cut -d = -f 2)
        days_left=$(echo "(" $(date -d "${expire_date}" +%s) - $(date +%s) ")" / 86400 | bc)

        if [[ ${days_left} -gt ${days_warn} ]]; then
            status=0
        elif [[ ${days_left} -gt ${days_crit} ]]; then
            status=1
        else
            status=2
        fi

        echo "${status} Certificate_${domain_name} days=${days_left} Certificate expires in ${days_left} days (${expire_date})"
    done
done