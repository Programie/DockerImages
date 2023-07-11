#! /bin/bash

url="$1"
output_dir="$2"
filename_format="${3:-%Y-%m-%d_%H-%M-%S%z}"

if [[ -z ${url} ]] || [[ -z ${output_dir} ]]; then
    echo "Usage: $0 <url> <output dir> [<filename format>]"
    exit 1
fi

while true; do
    mkdir -p "${output_dir}/$(date +%Y/%m/%d)"

    start_time=$(date +%s)

    ffmpeg \
        -hide_banner \
        -loglevel info \
        -i "${url}" \
        -f segment \
        -reset_timestamps 1 \
        -strftime 1 \
        -segment_time 1800 \
        -segment_atclocktime 1 \
        -segment_format mkv \
        -c copy \
        -map 0 \
        "${output_dir}/%Y/%m/%d/${filename_format}.mkv"

    end_time=$(date +%s)
    duration=$((end_time - start_time))

    if [[ ${duration} -lt 10 ]]; then
        sleep 10
    fi
done
