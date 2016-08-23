#!/usr/bin/env bash

set -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
CDIR=`pwd`

cd $DIR

./runtests.sh --install --upgrade

find . \( -name "*.pyc" -o -name __pycache__ \) -delete
python ./setup.py sdist upload

cd $CDIR
