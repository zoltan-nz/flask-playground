#!/usr/bin/env sh

apk add --no-cache --update python3-dev gcc build-base
python -V
pip install pipenv
pipenv --rm || true
pipenv run setup
pipenv run init-db
pipenv run test
pipenv run cov
pipenv run cov-report

python setup.py bdist_wheel
pip install dist/*
pipenv run env
pipenv run app
