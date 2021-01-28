FROM python:3.6-alpine3.12
RUN addgroup -S app && adduser -S app -G app

RUN mkdir /opt/output
RUN mkdir /opt/logs
WORKDIR /source_code

ARG VERSION=0.0.0
ENV VERSION=$VERSION
ENV SETUPTOOLS_SCM_PRETEND_VERSION=$VERSION

RUN python3 -m pip install --upgrade pip
RUN apk update -q --no-cache \
    && apk add -q --no-cache python3 py3-pip
RUN pip3 install setuptools_scm

COPY . .

RUN pip3 install .
RUN apk del py3-pip

# ENV PYTHONPATH=${PYTHONPATH}:'/source_code'

RUN chmod +x start.sh

RUN chown -R app . && chown -R app /opt/output
USER app:app

CMD ["sh", "start.sh"]
