FROM python:3.6-alpine3.12

RUN mkdir /source_code
RUN mkdir /opt/output
WORKDIR /source_code

COPY . .

RUN apk update -q --no-cache \
    && apk add -q --no-cache python3 py3-pip

RUN pip3 install setuptools_scm
RUN pip3 install .
RUN apk del py3-pip

# ENV PYTHONPATH=${PYTHONPATH}:'/source_code'

RUN chmod +x start.sh
CMD ["sh", "start.sh"]