import os
import uuid

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))


with open('requirements.txt') as f:
    install_reqs = f.readlines()
    reqs = [str(ir) for ir in install_reqs]

with open(os.path.join(here, 'README.md')) as fp:
    long_description = fp.read()

setup(
    name='pspt-verifier',
    version='2.0.15',
    description='Verifies blockchain passports',
    author='AlvinaKundhlande',
    tests_require=['tox'],
    url='https://github.com/blockchain-passports/pspt-verifier',
    license='alvina',
    author_email='nakundhlande@gmail.com',
    long_description=long_description,
    packages=find_packages(),
    install_requires=reqs
)
