FROM golang AS build

RUN go get github.com/deepch/RTSPtoWebRTC

WORKDIR src/github.com/deepch/RTSPtoWebRTC

RUN go build -o /rtsp-to-webrtc .

FROM debian:buster

COPY --from=build /rtsp-to-webrtc /app/rtsp-to-webrtc
COPY --from=build /go/src/github.com/deepch/RTSPtoWebRTC/web /app/web

WORKDIR /app

CMD ["/app/rtsp-to-webrtc"]

EXPOSE 8083