# Base image to use
FROM python:3.10.0b2-alpine3.12 as build
# update alpine OS and install python3 and pip3
RUN apk update -q --no-cache \
    && apk add -q --no-cache python3 py3-pip
# install environment for compiling (extra python packages dependencies)
RUN apk add --no-cache --virtual .pynacl_deps build-base python3-dev libffi-dev cargo openssl-dev gcc musl-dev
# upgrade setuptools_scm
RUN pip3 install --upgrade setuptools_scm wheel

# setup workdir
WORKDIR /source_code
# copy from local disk to container - to path /source_code
COPY . .
RUN python -m venv venv
RUN source /source_code/venv/bin/activate
# env arguments for versioning
ARG VERSION=0.0.0
ENV VERSION=$VERSION
ENV SETUPTOOLS_SCM_PRETEND_VERSION=$VERSION
# install source code as local package
RUN venv/bin/pip install --upgrade .
#RUN apk del .pynacl_deps build-base python3-dev libffi-dev cargo openssl-dev gcc musl-dev

# final app docker
FROM python:3.10.0b2-alpine3.12
# setup workdir
WORKDIR /source_code
COPY --from=0 /source_code .
# add user: app and group app - application user
RUN addgroup -S app && adduser -S app -G app
# create app directories
RUN mkdir /opt/output && mkdir /opt/logs && mkdir /opt/jira
# app permissions
RUN chmod +x start.sh && chown -R app:app /opt/output && chown -R app:app /opt/logs && chown -R app:app /opt/jira
# adding os (ping) functionality for operation system testing
RUN apk add iputils
# sets the user to run the application with: "app"
USER app:app
# cmd to run
CMD ["/bin/sh","-c", "/source_code/start.sh"]

