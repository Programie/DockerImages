#! /bin/bash

case "$1" in
    carddav2fb)
        for file in /config/*.php; do
            filename=$(basename ${file})

            if [[ ${filename} =~ \.inc\. ]]; then
                continue
            fi

            echo "Executing for ${filename}"
            php carddav2fb.php ${file}
        done
    ;;

    *)
        exec "$@"
    ;;
esac