#! /bin/bash

url="$1"
output_dir="$2"

if [[ -z ${url} ]] || [[ -z ${output_dir} ]]; then
    echo "Usage: $0 <url> <output dir>"
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
        -segment_format mp4 \
        -segment_format_options "movflags=frag_keyframe+empty_moov+default_base_moof" \
        -c copy \
        -map 0 \
        "${output_dir}/%Y/%m/%d/%Y-%m-%d_%H-%M-%S%z.mp4"

    end_time=$(date +%s)
    duration=$((end_time - start_time))

    if [[ ${duration} -lt 10 ]]; then
        sleep 10
    fi
done
