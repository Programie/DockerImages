FROM openjdk:8-jre-slim-stretch AS buildtools

ARG MINECRAFT_VERSION

WORKDIR /build

RUN apt-get update && \
    apt-get install -y git wget

RUN wget -O BuildTools.jar https://hub.spigotmc.org/jenkins/job/BuildTools/lastSuccessfulBuild/artifact/target/BuildTools.jar

RUN java -jar BuildTools.jar --rev ${MINECRAFT_VERSION} && \
    mv spigot-${MINECRAFT_VERSION}.jar spigot.jar


FROM programie/minecraft-server

ENV MINECRAFT_SERVER_JAR=spigot.jar \
    MINECRAFT_CMD_OPTS=--noconsole

COPY --from=buildtools /build/spigot.jar /usr/src/minecraft/spigot.jar
COPY eula.txt /usr/src/minecraft/eula.txt
COPY docker-entrypoint.d/ /docker-entrypoint.d/