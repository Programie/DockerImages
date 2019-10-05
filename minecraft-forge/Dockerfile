FROM openjdk:8-jre-slim-stretch AS forge-installer

ENV MINECRAFT_VERSION=1.14.4
ENV MINECRAFT_FORGE_VERSION=1.14.4-28.1.0

WORKDIR /installer

RUN apt-get update && \
    apt-get install -y git wget && \
    rm -rf /var/lib/apt/lists/* && \
    wget -O forge-installer.jar https://files.minecraftforge.net/maven/net/minecraftforge/forge/${MINECRAFT_FORGE_VERSION}/forge-${MINECRAFT_FORGE_VERSION}-installer.jar

RUN java -jar forge-installer.jar --installServer && \
    mkdir -p /forge && \
    mv forge-${MINECRAFT_FORGE_VERSION}.jar /forge/minecraftforge.jar && \
    mv minecraft_server.${MINECRAFT_VERSION}.jar libraries /forge


FROM programie/minecraft-server

ENV MINECRAFT_SERVER_JAR=minecraftforge.jar \
    MINECRAFT_CMD_OPTS=--nogui

COPY --from=forge-installer /forge /usr/src/minecraft
COPY eula.txt /usr/src/minecraft/eula.txt