FROM alpine

ARG UV_VERSION=0.7.13

RUN apk add bash curl && \
    curl -L https://github.com/astral-sh/uv/releases/download/${UV_VERSION}/uv-x86_64-unknown-linux-musl.tar.gz | tar -C /usr/local/bin -zxp --strip-components=1
