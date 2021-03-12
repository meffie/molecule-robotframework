import setuptools
import re

name = 'molecule-robotframework'
description='Robotframework Molecule Plugin :: run molecule tests with Robotframework as verifier'

def find_version():
    text = open('src/%s/__init__.py' % name.replace('-', '_')).read()
    return re.search(r"__version__\s*=\s*'(.*)'", text).group(1)

setuptools.setup(
    name=name,
    version=find_version(),
    author='Michael Meffie',
    author_email='mmeffie@sinenomine.net',
    description=description,
    long_description=description,
    # url=
    packages=setuptools.find_packages(where='src'),
    package_dir={'': 'src'},
    #include_package_data=True,
    entry_points={
        'molecule.verifier': [
            'robotframework = molecule_robotframework.robotframework:Robotframework',
        ],
    },
    install_requires=[
        'molecule',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
