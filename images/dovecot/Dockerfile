FROM ubuntu

RUN apt-get update && \
    apt-get install -y dovecot-imapd && \
    rm -rf /var/lib/apt/lists/*

RUN sed -ri -e 's/^!include auth-system.conf.ext$/!include auth-passwdfile.conf.ext/g' /etc/dovecot/conf.d/10-auth.conf && \
    sed -ri -e 's!^#log_path = syslog$!log_path = /dev/stdout!g' /etc/dovecot/conf.d/10-logging.conf && \
    sed -ri -e 's!^mail_location = mbox:~/mail:INBOX=/var/mail/%u$!mail_location = maildir:/var/lib/mail/%u!g' /etc/dovecot/conf.d/10-mail.conf && \
    sed -ri -e 's/^#mail_uid =$/mail_uid = nobody/g' /etc/dovecot/conf.d/10-mail.conf && \
    sed -ri -e 's/^#mail_gid =$/mail_gid = nogroup/g' /etc/dovecot/conf.d/10-mail.conf && \
    sed -ri -e 's/^ssl = yes$/ssl = required/g' /etc/dovecot/conf.d/10-ssl.conf

VOLUME ["/var/lib/mail"]

EXPOSE 143 993

CMD ["dovecot", "-F"]