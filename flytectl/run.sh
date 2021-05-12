#!/bin/bash

[[ ! -z "$FLYTE_AWS_ENDPOINT" ]] && export ENDPOINT="--endpoint-url $FLYTE_AWS_ENDPOINT" && echo $ENDPOINT;

echo aws ${ENDPOINT} s3 cp /opt/true.pb "$1"/outputs2.pb;

echo hi && aws "${ENDPOINT}" s3 cp /opt/true.pb "$1"/outputs2.pb

