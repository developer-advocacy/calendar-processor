#!/usr/bin/env bash

export CREDENTIALS_JSON_FN=${HOME}/credentials.json
export TOKEN_FN=${HOME}/token.pickle
export OUTPUT_JSON_FN=$output/appearances.json

cd appearances-site-generator

export EXISTING_GIT_USERNAME=$( git config --global user.name  )
git config --global user.email "josh@joshlong.com"
git config --global user.name "Appearances Bot"

echo "$PICKLED_TOKEN" | base64 -d > ${TOKEN_FN}
echo "$CREDENTIALS_JSON" > ${CREDENTIALS_JSON_FN}


ls -la ${TOKEN_FN}
ls -la ${CREDENTIALS_JSON_FN}

echo "TOKEN_FN=$TOKEN_FN"

pipenv install
pipenv run python main.py
