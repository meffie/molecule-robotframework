import os
import subprocess
import glob
from pathlib import Path
from contextlib import contextmanager

import pytest


platforms = {
    'alma8': {
        'box': 'generic/alma8',
        'version': '4.3.10',
    },
    'alma9': {
        'box': 'generic/alma9',
        'version': '4.3.10',
    },
    #
    # Skip centos6 test.
    # Reason: ansible setup fails with:
    # 'ansible-core requires a minimum of Python2 version 2.7 or Python3
    #  version 3.6. Current version: 2.6.6'
    #
    # 'centos6': {
    #     'box': 'rbrunckhorst/centos6',
    #     'version': '1.7',
    # },
    #
    'centos7': {
        'box': 'generic/centos7',
        'version': '4.3.10',
    },
    'centos8': {
        'box': 'generic/centos8',
        'version': '4.3.10',
    },
    'debian10': {
        'box': 'generic/debian10',
        'version': '4.3.10',
    },
    'debian11': {
        'box': 'generic/debian11',
        'version': '4.3.10',
    },
    'debian12': {
        'box': 'generic/debian12',
        'version': '4.3.10',
    },
    'fedora38': {
        'box': 'generic/fedora38',
        'version': '4.3.10',
    },
    'fedora39': {
        'box': 'generic/fedora39',
        'version': '4.3.10',
    },
    'freebsd11': {
        'box': 'generic/freebsd11',
        'version': '4.3.10',
    },
    #
    # Skip freebsd12 test.
    # Reason: 'pkg install' fails on this box.
    #
    # 'freebsd12': {
    #     'box': 'generic/freebsd12',
    #     'version': '4.3.8',
    # },
    #
    'freebsd13': {
        'box': 'generic/freebsd13',
        'version': '4.3.10',
    },
    'rocky8': {
        'box': 'generic/rocky8',
        'version': '4.3.10',
    },
    'rocky9': {
        'box': 'generic/rocky9',
        'version': '4.3.10',
    },
    'suse15': {
        'box': 'generic/opensuse15',
        'version': '4.3.10',
    },
    'solaris114': {
        'box': 'rbrunckhorst/solaris11.4',
        'version': '1.2',
    },
}

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
            scenarios.append(s)
    return sorted(scenarios)


def molecule_scenario(platform, scenario):
    """
    Verify molecule test on platform.
    """
    logfile = logdir / (platform + '-' + scenario + '.log')
    if not os.path.exists(logdir):
        os.makedirs(logdir)
    with open(logfile, 'w') as f:
        testdir = Path(__file__).resolve().parent
        with chdir(testdir):
            cmd = ['molecule', 'test', '--scenario-name', scenario]
            for n, v in ansible_vars.items():
                os.environ[n] = v
            os.environ['BOX'] = platforms[platform]['box']
            os.environ['BOX_VERSION'] = platforms[platform]['version']
            print('\nLogging to "%s".' % logfile)
            proc = subprocess.Popen(cmd,
                                    stdout=f.fileno(),
                                    stderr=subprocess.STDOUT)
            rc = proc.wait()
        assert rc == 0, 'See "%s".' % logfile


def test_molecule_list():
    proc = subprocess.Popen(['molecule', 'list'])
    rc = proc.wait()
    assert rc == 0


@pytest.mark.parametrize('platform', sorted(platforms.keys()))
def test_platform(platform):
    molecule_scenario(platform, 'default')


@pytest.mark.parametrize('scenario', detect_scenarios())
def test_scenario(scenario):
    molecule_scenario('debian12', scenario)
