#! /bin/bash

base_dir="$1"
input_filename="$2"
output_filename="${input_filename%.pdf}_ocr.pdf"

echo "Base dir: $1, Input filename: $2"

# Input file is not a PDF file
if [[ ${input_filename} != *.pdf ]]; then
    exit
fi

# Input file is the file produced by this script
if [[ ${input_filename} == *_ocr.pdf ]]; then
    exit
fi

echo "${input_filename} -> ${output_filename}"

ocrmypdf -l ${OCRMYPDF_LANG:-eng} ${base_dir}/${input_filename} ${base_dir}/${output_filename}

if [[ -n ${OCRMYPDF_CHOWN} ]]; then
    chown ${OCRMYPDF_CHOWN} ${base_dir}/${output_filename}
fi
