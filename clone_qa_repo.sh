#!/bin/bash

#####################################################
# Clone and pull the openapi-integration-tests automation repo
#####################################################

echo "**** Cloning the repo, branch ($1)..."
rm -rf openapi-integration-tests
git clone git@github.com:hellosign/openapi-integration-tests.git
cd openapi-integration-tests
if [ "$1" != "main" ]
then
    git fetch
    git branch -a
    git checkout "remotes/origin/$1"
    git pull origin "$1"
else
    git pull
fi

cd ..
