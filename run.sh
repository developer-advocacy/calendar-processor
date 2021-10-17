#!/usr/bin/env bash

set -e

export CREDENTIALS_JSON_FN=$HOME/credentials.json
export AUTHENTICATED_CREDENTIALS_JSON_FN=$HOME/authenticated-credentials.json

echo "${AUTHENTICATED_CREDENTIALS_JSON}" | base64 -d > $AUTHENTICATED_CREDENTIALS_JSON_FN
echo "${CREDENTIALS_JSON}" | base64 -d > $CREDENTIALS_JSON_FN

pipenv install
pipenv run python main.py
