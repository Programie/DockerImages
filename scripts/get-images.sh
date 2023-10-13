#! /bin/bash

log_message() {
    echo "[${image}] "$@ >&2
}

return_image() {
    if ! printf '%s\0' "${exclude_images[@]}" | grep -qwz "${image}"; then
        echo "${image}"
    fi
}

exclude_images=("${EXCLUDE_IMAGES}")

for image_path in images/*; do
    image=$(basename ${image_path})

    # Previous commit not available
    if [[ -z ${PREVIOUS_PUSH} ]]; then
        log_message "No previous commit available"
        return_image "${image}"
        continue
    fi

    # Found changes in the image
    if [[ $(git diff ${PREVIOUS_PUSH}..HEAD ${image_path}) ]]; then
        log_message "Found changes"
        return_image "${image}"
        continue
    fi

    log_message "No changes found"
done