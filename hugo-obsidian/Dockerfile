FROM golang

RUN go install github.com/gohugoio/hugo@latest && \
    go install github.com/jackyzha0/hugo-obsidian@latest && \
    mkdir /workspace

WORKDIR /workspace

RUN git clone https://github.com/64bitpandas/amethyst.git /workspace && \
    git clone https://github.com/alex-shpak/hugo-book /workspace/themes/hugo-book && \
    rm -rf /workspace/content

COPY build.sh /workspace