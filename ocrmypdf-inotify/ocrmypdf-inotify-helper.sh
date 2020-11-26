#! /bin/bash

input_filepath="$1"
base_dir=$(dirname "${input_filepath}")
input_filename=$(basename "${input_filepath}")
output_filename="${input_filename%.pdf}_ocr.pdf"

# Input file is not a PDF file
if [[ ${input_filename} != *.pdf ]]; then
    exit
fi

# Input file is the file produced by this script
if [[ ${input_filename} == *_ocr.pdf ]]; then
    exit
fi

echo "Processing ${input_filename}"

ocrmypdf -l "${OCRMYPDF_LANG:-eng}" "${base_dir}/${input_filename}" "${base_dir}/${output_filename}"

echo "Saved to ${output_filename}"

if [[ -n ${OCRMYPDF_CHOWN} ]]; then
    chown -c "${OCRMYPDF_CHOWN}" "${base_dir}/${output_filename}"
fi
