#!/bin/bash

set -e

rm -rf ./*.py
python -m grpc_tools.protoc -I . --proto_path=../../proto --python_betterproto_out=. ../../proto/*.proto
