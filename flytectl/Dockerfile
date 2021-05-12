FROM python:3.8-slim-buster

RUN apt-get update && apt install -y curl

RUN pip install awscli
RUN pip install gsutil

WORKDIR /tmp
RUN curl -s https://raw.githubusercontent.com/flyteorg/flytectl/master/install.sh | bash
RUN mv /tmp/bin/flytectl /usr/local/bin

# These are literal maps with "success": True and False
COPY true_map.pb /opt/true.pb
COPY false_map.pb /opt/false.pb

ENV FLYTE_INTERNAL_IMAGE=flyte_ctl_task:123

WORKDIR /app
