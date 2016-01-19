from setuptools import setup, find_packages


DESCRIPTION = 'Send emails with Django template system'

LONG_DESCRIPTION = None
try:
    LONG_DESCRIPTION = open('README.rst').read()
except:
    pass

CLASSIFIERS = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'Framework :: Django',
]


setup(
    name='django-mail-templated',
    version='2.4.3',
    packages=find_packages(),
    include_package_data=True,
    author='Artem Rizhov',
    author_email='artem.rizhov@gmail.com',
    url='https://github.com/artemrizhov/django-mail-templated',
    license='MIT',
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    platforms=['any'],
    classifiers=CLASSIFIERS,
    test_suite='runtests.runtests',
)
