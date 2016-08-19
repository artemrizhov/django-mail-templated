#!/usr/bin/env bash
# Run tests with all supported Django and Python versions.
# If --install is passed, also test installation from PyPI.

set -e

# Get the dir where the script is located.
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

if [[ $1 == '--install' || $2 == '--install' ]] ; then
  test_install=true
else
  test_install=false
fi

if [[ $1 == '--upgrade' || $2 == '--upgrade' ]] ; then
  upgrade=true
else
  upgrade=false
fi


function activate {
    v=$1
    pv=$2
    install=$3
    cdir=`pwd`

    # Setup virtual environment for the specified Django version if absent.
    IFS='.' read v1 v2 <<< "$v"
    if $install ; then
        env="$cdir/envs/install-$pv-$v"
    else
        env="$cdir/envs/$pv-$v"
    fi
    if [ ! -d $env ] ; then
        virtualenv --no-site-packages -p python$pv $env
    fi

    source $env/bin/activate
    # Install or upgrade the required Django version.
    if $upgrade ; then
        packages="django>=$v1.$v2,<$v1.$(($v2+1))"
        if [[ $pv == "2" ]] ; then
            packages="$packages pysqlite"
        fi
        pip install -U --cache-dir=$cdir/envs/cache $packages
    fi
}


function test {
    v=$1
    pv=$2
    cdir=`pwd`
    echo ""
    echo "Testing with Django $v and Python $pv"
    echo "===================================================================="

    activate $v $pv false

    # Run tests in a standalone environment.
    $env/bin/python$pv $DIR/mail_templated/test_utils/run.py

    deactivate

    # Test installation into virtual environment.
    if $test_install ; then
        activate $v $pv true

        # Install a fresh version of the application.
        find $DIR \( -name "*.pyc" -o -name __pycache__ \) -delete
        pip install -U --force-reinstall "$DIR/dist/django-mail-templated-test.tar.gz"

        # Create test Django project.
        project_dir="$cdir/testproject"
        if [ -d $project_dir ] ; then
            rm -r $project_dir
        fi
        mkdir $project_dir
        $env/bin/django-admin.py startproject testproject $project_dir
        cat $DIR/mail_templated/test_utils/settings_extra.py >> $project_dir/testproject/settings.py

        # Run tests via the test project.
        $project_dir/manage.py test mail_templated

        # Cleanup.
        rm -r $project_dir
        deactivate
    fi

    echo ""
}

current_dir=`pwd`

cd $DIR
# Make new package for tests.
if $install ; then
    find $DIR -name __pycache__ -exec rm -r {} \; || true
    find $DIR -name "*.pyc" -exec rm {} \;
    MAIL_TEMPLATED_VERSION=test python $DIR/setup.py sdist
fi

cd $DIR/..

p2v=`pyenv versions --bare | grep -P '^2.\d+.\d+$' | tail -n 1`
p34v=`pyenv versions --bare | grep -P '^3.4.\d+$' | tail -n 1`
p3v=`pyenv versions --bare | grep -P '^3.\d+.\d+$' | tail -n 1`
export PYENV_VERSION="$p2v:$p3v:$p34v"

echo ""
echo "Python versions to be used: $p2v, $p34v, $p3v"
echo "===================================================================="
p2v=`echo $p2v | sed -r 's/\.[^.]+$//'`
p34v=`echo $p34v | sed -r 's/\.[^.]+$//'`
p3v=`echo $p3v | sed -r 's/\.[^.]+$//'`

test "1.4" $p2v
test "1.5" $p2v
test "1.5" $p34v
test "1.6" $p2v
test "1.6" $p34v
test "1.7" $p2v
test "1.7" $p34v
test "1.8" $p2v
test "1.8" $p34v
test "1.9" $p2v
test "1.9" $p3v
test "1.10" $p2v
test "1.10" $p3v

cd $current_dir
