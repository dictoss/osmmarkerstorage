#!/bin/bash

TEST_MODE=
APP_NAME=markerstorage
BIN_PYTHON=python3
BIN_PIP=pip3
APP_ENV=test

# execute unittest
PYTHONWARNINGS=default coverage run --source='.' manage.py test -v2 ${APP_NAME}
RET=$?
echo "unittest result code: ${RET}"
coverage report
coverage xml
coverage html
exit ${RET}
