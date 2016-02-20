#!/usr/bin/env bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

find $DIR \( -name "*.pyc" -o -name __pycache__ \) -delete

python $DIR/setup.py sdist upload