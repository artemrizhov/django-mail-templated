#!/usr/bin/env bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

find $DIR -name __pycache__ -exec rm -r {} \;
find $DIR -name "*.pyc" -exec rm {} \;

python $DIR/setup.py sdist upload