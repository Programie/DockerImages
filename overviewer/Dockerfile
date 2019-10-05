FROM debian:stretch

ENV MINECRAFT_VERSION=1.14.4

RUN apt-get update && \
    apt-get install -y wget gnupg apt-transport-https && \
    echo "deb https://overviewer.org/debian ./" > /etc/apt/sources.list.d/overviewer.list && \
    wget -O - https://overviewer.org/debian/overviewer.gpg.asc | apt-key add - && \
    apt-get update && \
    apt-get install -y minecraft-overviewer

RUN mkdir -p ~/.minecraft/versions/${MINECRAFT_VERSION} && \
    wget https://overviewer.org/textures/${MINECRAFT_VERSION} -O ~/.minecraft/versions/${MINECRAFT_VERSION}/${MINECRAFT_VERSION}.jar

COPY entrypoint.sh /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]