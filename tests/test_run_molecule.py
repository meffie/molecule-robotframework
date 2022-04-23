import os
import subprocess
import glob
from pathlib import Path
from contextlib import contextmanager
from tempfile import TemporaryDirectory

import pytest

platforms = [
    'alma8',
    'rocky8',
    'centos7',
    'fedora34',
    'fedora35',
    'debian11',
    'debian10',
]

logdir = Path('/tmp/molecule-robotframework')
driver = os.getenv('MOLECULE_DRIVER')

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
    return scenarios

def test_molecule_init():
    """Verify that init scenario works."""
    with TemporaryDirectory() as tmpdir:
        with chdir(tmpdir):
            cmd = ['molecule', 'init', 'role', 'acme.myrole', '--verifier-name', 'robotframework']
            proc = subprocess.Popen(cmd)
            rc = proc.wait()
            assert rc == 0

def molecule_scenario(platform, scenario):
    """
    Verify molecule test on platform.
    """
    image = 'generic/%s' % platform
    logfile = logdir / ('%s-%s.log' % (platform, scenario))
    if not os.path.exists(logdir):
        os.makedirs(logdir)
    with open(logfile, 'w') as f:
        testdir = Path(__file__).resolve().parent
        with chdir(testdir):
            cmd = ['molecule', 'test', '--scenario-name', scenario]
            if driver:
                cmd.append('--driver-name=%s' % driver)
            for n, v in ansible_vars.items():
                os.environ[n] = v
            if platform in ('debian9'):
                os.environ['ANSIBLE_PYTHON_INTERPRETER'] = '/usr/bin/python3'
            os.environ['IMAGE'] = image
            os.environ['TEMPLATE'] = platform
            print('\nLogging to "%s".' % logfile)
            proc = subprocess.Popen(cmd, stdout=f.fileno(), stderr=subprocess.STDOUT)
            rc = proc.wait()
        assert rc == 0, 'See "%s".' % logfile

@pytest.mark.parametrize('platform', platforms)
def test_platform(platform):
    molecule_scenario(platform, 'default')

@pytest.mark.parametrize('scenario', detect_scenarios())
def test_scenario(scenario):
    molecule_scenario('debian11', scenario)
