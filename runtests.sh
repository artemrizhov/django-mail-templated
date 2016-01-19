#!/usr/bin/env bash

set -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

if [[ $1 == '--install' ]] ; then
  install=true
else
  install=false
fi

function test {
    v=$1
    pv=$2
    echo "===================================================================="
    echo "Testing with Django $v and Python $pv"

    # Setup virtual environment for the specified Django version if absent.
    IFS='.' read v1 v2 <<< "$v"
    if $install ; then
        env="$DIR/../env/install-$pv-$v"
    else
        env="$DIR/../env/$pv-$v"
    fi
    if [ ! -d $env ] ; then
        virtualenv --no-site-packages -p /usr/bin/python$pv $env
    fi

    source $env/bin/activate
    # Install or upgrade the required Django version.
    pip install -U "django>=$v1.$v2,<$v1.$(($v2+1))"
    if $install ; then
        pip install -U "django-mail-templated"
        project_dir="$DIR/../testproject"
        mkdir $project_dir
        $env/bin/django-admin.py startproject testproject $project_dir
        sed -i -- "s/\(INSTALLED_APPS\s*=\s*[\[(]\)/\1'mail_templated',/" $project_dir/testproject/settings.py
        sed -i -- "s/\('django.db.backends.\)'/\1sqlite3'/" $project_dir/testproject/settings.py
        sed -i -- "s/\('NAME': '\)'/\1db.sqlite3'/" $project_dir/testproject/settings.py
        $project_dir/manage.py test mail_templated
        rm -r $project_dir
    else
        $env/bin/python$pv $DIR/runtests.py
    fi

    deactivate
    echo ""
}

current_dir=`pwd`
cd $DIR/..

for v in "1.4" "1.5" "1.6" "1.7" "1.8" "1.9" ; do
    test $v 2
    if [[ ! ( $v =~ ^(1.4)$ ) ]] ; then
        test $v 3
    fi
done

cd $current_dir
