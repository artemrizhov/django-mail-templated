#!/usr/bin/env bash

set -e

for v in "1.4" "1.5" "1.6" "1.7" "1.8" "1.9" ; do
    echo "======================================================================"
    echo "Testing with Django $v"

    # Setup virtual environment for the specified Django version if absent.
    IFS='.' read v1 v2 <<< "$v"
    if [ ! -d "../env-$v" ] ; then
        virtualenv --no-site-packages ../env-$v
    fi

    source ../env-$v/bin/activate
    # Install or upgrade the required Django version.
    pip install -U "django>=$v1.$v2,<$v1.$(($v2+1))"

    ../env-$v/bin/python runtests.py

    deactivate
    echo ""
done
