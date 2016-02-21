#!/usr/bin/env bash

set -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

$DIR/runtests.sh --install --upgrade

find $DIR \( -name "*.pyc" -o -name __pycache__ \) -delete

python $DIR/setup.py sdist upload