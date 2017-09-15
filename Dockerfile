FROM alpine
# load any public updates from Alpine packages
RUN apk update
# upgrade any existing packages that have been updated
RUN apk upgrade
# add/install python3 and related libraries
# https://pkgs.alpinelinux.org/package/edge/main/x86/python3
RUN apk add python3
# move requirements file into the container
COPY requirements.txt /tmp/
# install the library dependencies for this application
RUN pip3 install -r /tmp/requirements.txt
