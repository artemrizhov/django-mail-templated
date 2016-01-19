#!/usr/bin/env bash

set -e

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
    env="../env/$pv-$v"
    if $install ; then
        env="../env/install-$pv-$v"
    fi
    if [ ! -d $env ] ; then
        virtualenv --no-site-packages -p /usr/bin/python$pv $env
    fi

    source $env/bin/activate
    # Install or upgrade the required Django version.
    pip install -U "django>=$v1.$v2,<$v1.$(($v2+1))"
    if $install ; then
        pip install -U "django-mail-templated"
        project_dir="../testproject"
        mkdir $project_dir
        django-admin startproject testproject $project_dir
        sed -i -- 's/\(INSTALLED_APPS\s*=\s*\[\)/\1"mail_templated",/' $project_dir/testproject/settings.py
        $project_dir/manage.py test mail_templated
#        rm -r $project_dir
    else
        $env/bin/python$pv runtests.py
    fi

    deactivate
    echo ""
}

for v in "1.4" "1.5" "1.6" "1.7" "1.8" "1.9" ; do
    test $v 2
    if [[ ! ( $v =~ ^(1.4)$ ) ]] ; then
        test $v 3
    fi
done
