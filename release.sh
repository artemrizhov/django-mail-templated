#!/usr/bin/env bash

find -name __pycache__ -exec rm -r {} \;
find -name "*.pyc" -exec rm {} \;

python setup.py sdist upload