FROM alpine

ENV TERM linux
RUN apk --no-cache add apache2-utils
RUN apk --no-cache add curl

CMD ["/usr/bin/ab"]
