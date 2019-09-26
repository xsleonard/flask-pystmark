#!/usr/bin/env python

"""
Flask-Pystmark
--------------

A Flask extension for Pystmark (a Postmark API library)

Links
`````

* `documentation <http://flask-pystmark.readthedocs.org/en/latest/>`_
* `github <https://github.com/xsleonard/flask-pystmark>`_
* `development version <https://github.com/xsleonard/flask-pystmark/tarball/master#egg=Flask-Pystmark>`_
"""

import os
import sys
import subprocess
import shlex
from setuptools import setup, Command

pypy = False
if 'pypy' in sys.version.lower():
    pypy = True

about = {}
with open('__about__.py') as f:
    exec(f.read(), about)


class Test(Command):
    ''' Test application with the following:
        pep8 conformance (style)
        pyflakes validation (static analysis)
        no print statements (breaks wsgi)
        nosetests (code tests) [--with-integration] [--run-failed]
    '''
    description = 'Test {0} source code'.format(about['__title__'])
    user_options = [('run-failed', None,
                     'Run only the previously failed tests.'),
                    ('nose-only', None, 'Run only the nose tests.')]
    boolean_options = ['run-failed', 'nose-only']

    _files = ['__about__.py', 'flask_pystmark.py']

    _test_requirements = ['flake8', 'nose', 'disabledoc', 'coverage', 'mock']

    @property
    def files(self):
        return ' '.join(self._files)

    def initialize_options(self):
        self.run_failed = False
        # Disable the flake8 tests in pypy due to bug in pep8 module
        self.nose_only = pypy
        self.with_integration = False
        self.flake8 = 'flake8 {0} test/'.format(self.files)

    def finalize_options(self):
        pass

    def _no_print_statements(self):
        cmd = 'grep -rnw print {0}'.format(self.files)
        p = subprocess.Popen(shlex.split(cmd), close_fds=True,
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        err = p.stderr.read().strip()
        if err:
            msg = 'ERROR: stderr not empty for print statement grep: {0}'
            print(msg.format(err))
            raise SystemExit(-1)
        output = p.stdout.read().strip()
        if output:
            print('ERROR: Found print statements in source code:')
            print(output)
            raise SystemExit(-1)

    def _get_py_files(self, basepath, subpath=''):
        files = []
        badchars = ['.', '_', '~']
        path = os.path.join(basepath, subpath)
        for f in os.listdir(path):
            if (not f.endswith('.py') or
                    any(map(lambda c: f.startswith(c), badchars))):
                continue
            files.append(os.path.join(subpath, f))
        return files

    def _get_nose_command(self):
        nosecmd = ('nosetests -v -w test/ --cover-package=flask_pystmark '
                   '--cover-package=__about__ '
                   '--cover-min-percentage=100 --with-coverage '
                   '--disable-docstring --cover-erase')
        if self.run_failed:
            nosecmd += ' --failed'
        nose = ' '.join(shlex.split(nosecmd))
        return nose

    def _check_module(self, module):
        cmd = '/usr/bin/env python -c "import {0}"'.format(module)
        try:
            subprocess.check_call(shlex.split(cmd))
        except subprocess.CalledProcessError:
            msg = 'Python package "{0}" is required to run the tests'
            print(msg.format(module))
            raise SystemExit(-1)

    def _check_test_packages(self):
        for m in self._test_requirements:
            self._check_module(m)

    def run(self):
        print('Checking test packages installed...')
        self._check_test_packages()
        cmds = [self._get_nose_command()]
        if not self.nose_only:
            print('Checking no print statements in code...')
            self._no_print_statements()
            cmds = [self.flake8] + cmds
        cmds = filter(bool, cmds)
        if not cmds:
            print('No action taken.')
            SystemExit(-2)
        for cmd in cmds:
            print('Executing command: {0}'.format(cmd))
            c = shlex.split(cmd)
            try:
                subprocess.check_call(c)
            except subprocess.CalledProcessError:
                print('Command failed: {0}'.format(cmd))
                raise SystemExit(-1)
        raise SystemExit(0)

setup(
    name=about['__title__'],
    version=about['__version__'],
    url='https://github.com/xsleonard/flask-pystmark',
    license='MIT',
    author='Steve Leonard',
    author_email='sleonard76@gmail.com',
    description=about['__description__'],
    long_description=__doc__,
    long_description_content_type='text/x-rst',
    py_modules=['flask_pystmark', '__about__'],
    cmdclass=dict(test=Test),
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Flask', 'pystmark'
    ],
    tests_require=[
        'nose',
        'coverage',
        'disabledoc',
        'mock',
        'flake8',
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Communications :: Email',
        'Programming Language :: Python',
    ]
)
