#!/usr/bin/env bash

set -e
DIR=$(cd `dirname $0` && pwd)

git clone https://github.com/hellosign/openapi-integration-tests.git
cd openapi-integration-tests
./node-build
./php-build
./python-build
