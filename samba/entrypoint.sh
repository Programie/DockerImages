#! /bin/bash

users=$(while read -r line; do
    line=$(echo ${line})

    if [[ ${line} =~ ^valid\ users ]]; then
        echo ${line} | cut -d "=" -f 2 | tr ' ' '\n'
    fi
done < /etc/samba/smb.conf | sort | uniq)

for user in ${users}; do
    if grep -q "^${user}:" /etc/passwd; then
        continue
    fi

    useradd -d /nonexistent -g users -s /usr/sbin/nologin ${user}
done

exec "$@"