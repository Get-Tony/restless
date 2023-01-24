#!/bin/bash
set -e

# This script is run before the build starts. It is used to check that the
# environment is set up correctly and to do any other pre-build setup.

PACKAGE_NAME=$1

echo -e "Running pre-build tests for $PACKAGE_NAME\n"

# Run black
echo -e "--> Starting: black"
black --check $PACKAGE_NAME
echo -e "<-- Finished: black\n"

# Run pylint
echo -e "--> Starting: pylint"
pylint $PACKAGE_NAME
echo -e "<-- Finished: pylint\n"

# Run mypy
echo -e "--> Starting: mypy"
mypy $PACKAGE_NAME
echo -e "<-- Finished: mypy\n"

# Run pytest verbose and with coverage
echo -e "--> Starting: pytest"
pytest --cov=$PACKAGE_NAME --cov-report term-missing -v
echo -e "<-- Finished: pytest\n"
