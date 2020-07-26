FROM golang AS build

RUN go get github.com/deepch/RTSPtoWSMP4f

WORKDIR src/github.com/deepch/RTSPtoWSMP4f

RUN sed -i 's|"://127.0.0.1"+port|"://"+document.location.host|g' /go/src/github.com/deepch/RTSPtoWSMP4f/web/static/js/app.js

RUN go build -o /rtsp-to-wsmp4f .

FROM debian:buster

COPY --from=build /rtsp-to-wsmp4f /app/rtsp-to-wsmp4f
COPY --from=build /go/src/github.com/deepch/RTSPtoWSMP4f/web /app/web

WORKDIR /app

CMD ["/app/rtsp-to-wsmp4f"]

EXPOSE 8083