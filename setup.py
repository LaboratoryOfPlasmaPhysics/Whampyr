#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup
import sys, os

# taken from here : https://github.com/mesonbuild/meson/blob/master/setup.py#L30
try:
    from setuptools import setup
    from setuptools.command.install_scripts import install_scripts as orig
except ImportError:
    from distutils.core import setup
    from distutils.command.install_scripts import install_scripts as orig


class install_scripts(orig):
    def run(self):
        if sys.platform == 'win32':
            super().run()
            return

        if not self.skip_build:
            self.run_command('build_scripts')
        self.outfiles = []
        if not self.dry_run:
            self.mkpath(self.install_dir)

        # We want the files to be installed without a suffix on Unix
        for infile in self.get_inputs():
            infile = os.path.basename(infile)
            in_built = os.path.join(self.build_dir, infile)
            in_stripped = infile[:-3] if infile.endswith('.py') else infile
            outfile = os.path.join(self.install_dir, in_stripped)
            # NOTE: Mode is preserved by default
            self.copy_file(in_built, outfile)
            self.outfiles.append(outfile)


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['PyQt5', 'scipy', 'numpy', 'matplotlib', 'astropy']

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest', ]

setup(
    author="Alexis Jeandet",
    author_email='alexis.jeandet@lpp.polytechnique.fr',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    description="Python clone of WHAMP",
    install_requires=requirements,
    license="GNU General Public License v3",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='whampyr',
    name='whampyr',
    packages=['whampyr', 'whampyr.GUI'],
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/jeandet/whampyr',
    version='0.1.0',
    zip_safe=False,
    scripts=['whampyr.py'],
    cmdclass={'install_scripts': install_scripts},
)
