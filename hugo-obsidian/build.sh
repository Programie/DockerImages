#! /bin/bash

clone_url="$1"

if [[ ${clone_url} ]]; then
    rm -rf /workspace/content
    git clone "${clone_url}" /workspace/content
fi

hugo-obsidian -input=content -output=assets/indices -index -root=.

rm -rf /workspace/public/*

hugo --minify