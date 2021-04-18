# Base image to use
FROM python:3.6-alpine3.12
# add user: app and group app - application user
RUN addgroup -S app && adduser -S app -G app
# update alpine OS and install python3 and pip3
RUN apk update -q --no-cache \
    && apk add -q --no-cache python3 py3-pip
# upgrade setuptools_scm
RUN pip3 install --upgrade setuptools_scm wheel
# create app directories
RUN mkdir /opt/output && mkdir /opt/logs && mkdir /opt/jira
# setup workdir
WORKDIR /source_code
# env arguments for versioning
ARG VERSION=0.0.0
ENV VERSION=$VERSION
ENV SETUPTOOLS_SCM_PRETEND_VERSION=$VERSION

# copy from local disk to container - to path /source_code

COPY . .
# install source code as local package
RUN pip3 install --upgrade .
# app permissions
RUN chmod +x start.sh && chown -R app:app /opt/output && chown -R app:app /opt/logs && chown -R app:app /opt/jira

# sets the user to run the application with: "app"
USER app:app
# cmd to run
CMD ["/bin/sh","-c", "/source_code/start.sh"]

