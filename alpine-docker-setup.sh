#!/usr/bin/env sh

apk add --no-cache --update python3-dev gcc build-base
python -V
pip install pipenv
pipenv run setup
pipenv run test
pipenv run cov
pipenv run cov_report

python setup.py bdist_wheel
pip install dist/*
pipenv run app
