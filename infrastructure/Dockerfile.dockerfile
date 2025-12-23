FROM alpine:latest

RUN apk add --no-cache fortune

CMD ["fortune"]
