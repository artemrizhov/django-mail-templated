#!/usr/bin/env bash

set -e

function test {
    v=$1
    pv=$2
    echo "===================================================================="
    echo "Testing with Django $v and Python $pv"

    # Setup virtual environment for the specified Django version if absent.
    IFS='.' read v1 v2 <<< "$v"
    env="../env$pv-$v"
    if [ ! -d $env ] ; then
        virtualenv --no-site-packages -p /usr/bin/python$pv $env
    fi

    source $env/bin/activate
    # Install or upgrade the required Django version.
    pip install -U "django>=$v1.$v2,<$v1.$(($v2+1))"

    $env/bin/python$pv runtests.py

    deactivate
    echo ""
}

for v in "1.4" "1.5" "1.6" "1.7" "1.8" "1.9" ; do
    test $v 2
    if [ $v != "1.4" ] ; then
        test $v 3
    fi
done
