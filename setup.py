import setuptools
import re

name = 'molecule-robotframework'
description='Robot Framework Molecule Plugin :: run molecule tests with Robot Framework as verifier'

def find_version():
    text = open('src/%s/__init__.py' % name.replace('-', '_')).read()
    return re.search(r"__version__\s*=\s*'(.*)'", text).group(1)

setuptools.setup(
    name=name,
    version=find_version(),
    author='Michael Meffie',
    author_email='mmeffie@sinenomine.net',
    description=description,
    long_description=open('README.rst').read(),
    long_description_content_type='text/x-rst',
    url='https://github.com/meffie/molecule-robotframework',
    packages=setuptools.find_packages(where='src'),
    package_dir={'': 'src'},
    include_package_data=True,
    entry_points={
        'molecule.verifier': [
            'robotframework = molecule_robotframework.robotframework:Robotframework',
        ],
        'console_scripts': [
            'patch-molecule-schema = molecule_robotframework.patch_molecule_schema:main',
        ],
    },
    install_requires=[
        # molecule plugins are not allowed to mention Ansible as a direct dependency
        'molecule>=6.0.0',
        'pyyaml>=5.1',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',
)
