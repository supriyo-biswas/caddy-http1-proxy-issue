#!/bin/bash

set -eu

function _in_container_task() {
    yum install -y oracle-softwarecollection-release-el7 which
    yum install -y scl-utils rh-python38
    scl enable rh-python38 "pip install pipenv"
    scl enable rh-python38 "pipenv install --dev"
    scl enable rh-python38 "pipenv run pyinstaller --onefile app.py"
    mv dist/app data/app
    rm -rf build app.spec
}

cd "$(dirname "$0")"

if [[ -z ${1+x} ]]; then
    docker run -v "$PWD":/data --rm -it oraclelinux:7 /data/build-app.sh _in_container_task
    rm -rf app.spec
else
    "$@"
fi
