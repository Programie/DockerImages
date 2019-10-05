#! /bin/bash

action="$1"
recording="$2"

if [[ -z ${action} ]] || [[ -z ${recording} ]]; then
    echo "Usage: $0 <action> <recording>"
    exit 1
fi

case ${action} in
    rec_start)
        message="Recording started: ${recording}"
    ;;

    rec_finish)
        message="Recording finished: ${recording}"
    ;;

    *)
        echo "Invalid action: ${action}"
        exit 1
    ;;
esac

curl -s \
  --form-string "token=${PUSHOVER_TOKEN}" \
  --form-string "user=${PUSHOVER_USER}" \
  --form-string "message=${message}" \
  --form-string "sound=${PUSHOVER_SOUND}" \
  https://api.pushover.net/1/messages.json