FROM golang:alpine AS builder

RUN go install github.com/jackyzha0/hugo-obsidian@latest


FROM alpine

COPY --from=builder /go/bin/hugo-obsidian /usr/local/bin/

RUN mkdir /workspace && \
    apk add hugo git bash && \
    git clone https://github.com/64bitpandas/amethyst.git /workspace && \
    git clone https://github.com/alex-shpak/hugo-book /workspace/themes/hugo-book && \
    rm -rf /workspace/content

WORKDIR /workspace

COPY build.sh /workspace