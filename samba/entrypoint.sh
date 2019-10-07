#! /bin/bash

users=$(while read -r line; do
    line=$(echo ${line})

    if [[ ${line} =~ ^\;\ create-user: ]]; then
        echo ${line} | cut -d ":" -f 2,3 | tr ' ' '\n'
    fi
done < /etc/samba/smb.conf | sort | uniq)

for user_line in ${users}; do
    user=$(echo ${user_line} | cut -d ":" -f 1)
    user_id=$(echo ${user_line} | cut -d ":" -f 2)
    if grep -q "^${user}:" /etc/passwd; then
        continue
    fi

    useradd -d /nonexistent -g users -s /usr/sbin/nologin -u ${user_id} ${user}
done

exec "$@"