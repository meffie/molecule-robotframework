import os
import subprocess
import glob
from pathlib import Path
from contextlib import contextmanager

import pytest

images = [
    'generic/alma8',
    'generic/alma9',
    'generic/rocky8',
    'generic/centos7',
    'generic/fedora35',
    'generic/fedora36',
    'generic/debian10',
    'generic/debian11',
    #'rbrunckhorst/solaris11.4',
]

logdir = Path('/tmp/molecule-robotframework')

# Remove color escape codes for logs.
ansible_vars = {
    'ANSIBLE_VERBOSITY': '1',
    'ANSIBLE_STDOUT_CALLBACK': 'debug',
    'ANSIBLE_NOCOLOR': '1',
    'ANSIBLE_FORCE_COLOR': '0',
}

@contextmanager
def chdir(path):
    prev = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(prev)

def detect_scenarios():
    """
    Find non-default scenario names.
    """
    scenarios = []
    testdir = Path(__file__).resolve().parent
    with chdir(testdir):
        for path in glob.glob('molecule/*/molecule.yml'):
            s = path.split('/')[1]
            if s != 'default':
                scenarios.append(s)
    return sorted(scenarios)

def molecule_scenario(image, scenario):
    """
    Verify molecule test on platform.
    """
    if '/' in image:
        platform = image.split('/')[1]
    else:
        platform = image
    logfile = logdir / (platform + '-' + scenario + '.log')
    if not os.path.exists(logdir):
        os.makedirs(logdir)
    with open(logfile, 'w') as f:
        testdir = Path(__file__).resolve().parent
        with chdir(testdir):
            cmd = ['molecule', 'test', '--scenario-name', scenario]
            for n, v in ansible_vars.items():
                os.environ[n] = v
            if 'debian9' in image:
                os.environ['ANSIBLE_PYTHON_INTERPRETER'] = '/usr/bin/python3'
            os.environ['IMAGE'] = image
            print('\nLogging to "%s".' % logfile)
            proc = subprocess.Popen(cmd, stdout=f.fileno(), stderr=subprocess.STDOUT)
            rc = proc.wait()
        assert rc == 0, 'See "%s".' % logfile

@pytest.mark.parametrize('image', sorted(images))
def test_platform(image):
    molecule_scenario(image, 'default')

@pytest.mark.parametrize('scenario', detect_scenarios())
def test_scenario(scenario):
    molecule_scenario('generic/debian11', scenario)
