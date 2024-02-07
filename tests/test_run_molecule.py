import os
import subprocess
from pathlib import Path
from contextlib import contextmanager

import pytest

LOGDIR = Path('/tmp/molecule-robotframework')


ANSIBLE_VARS = {
    'ANSIBLE_VERBOSITY': '1',
    'ANSIBLE_STDOUT_CALLBACK': 'debug',
    'ANSIBLE_NOCOLOR': '1',       # Remove color escape codes
    'ANSIBLE_FORCE_COLOR': '0',
}


PLATFORMS = {
    'alma8': {
        'box': ('generic/alma8', '4.3.10'),
    },
    'alma9': {
        'box': ('generic/alma9', '4.3.10'),
    },
    'centos6': {
        'box': ('rbrunckhorst/centos6', '1.7'),
        'skip': 'ansible fails on this box.',
        # Ansible fails with the error message:
        #   ansible-core requires a minimum of Python2 version 2.7 or Python3
        #   version 3.6. Current version: 2.6.6'
    },
    'centos7': {
        'box': ('generic/centos7', '4.3.10'),
    },
    'centos8': {
        'box': ('generic/centos8', '4.3.10'),
    },
    'debian10': {
        'box': ('generic/debian10', '4.3.10'),
    },
    'debian11': {
        'box': ('generic/debian11', '4.3.10'),
    },
    'debian12': {
        'box': ('generic/debian12', '4.3.10'),
    },
    'fedora38': {
        'box': ('generic/fedora38', '4.3.10'),
    },
    'fedora39': {
        'box': ('generic/fedora39', '4.3.10'),
    },
    'freebsd11': {
        'box': ('generic/freebsd11', '4.3.10'),
    },
    'freebsd12': {
        'box': ('generic/freebsd12', '4.3.8'),
        'skip': '"pkg install" fails on this box.',
    },
    'freebsd13': {
        'box': ('generic/freebsd13', '4.3.10'),
    },
    'rocky8': {
        'box': ('generic/rocky8', '4.3.10'),
    },
    'rocky9': {
        'box': ('generic/rocky9', '4.3.10'),
    },
    'suse15': {
        'box': ('generic/opensuse15', '4.3.10'),
    },
    'solaris114': {
        'box': ('rbrunckhorst/solaris11.4', '1.2'),
    },
}


@contextmanager
def chdir(path):
    prev = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(prev)


def molecule_test(scenario, platform=None):
    """
    Run molecule test and capture output.
    """
    if platform:
        instance = PLATFORMS[platform]
        logfile = LOGDIR / (scenario + '-' + platform + '.log')
    else:
        instance = {}
        logfile = LOGDIR / (scenario + '.log')

    skip = instance.get('skip')
    if skip:
        pytest.skip('Reason: ' + skip)
        return

    if not os.path.exists(LOGDIR):
        os.makedirs(LOGDIR)
    with open(logfile, 'w') as f:
        print('\nLogging to "%s".' % logfile)
        testdir = Path(__file__).resolve().parent
        with chdir(testdir):
            for n, v in ANSIBLE_VARS.items():
                os.environ[n] = v

            box = instance.get('box')
            if box:
                os.environ['BOX'] = box[0]
                os.environ['BOX_VERSION'] = box[1]

            proc = subprocess.Popen(
                ['molecule', 'test', '--scenario-name', scenario],
                stdout=f.fileno(),
                stderr=subprocess.STDOUT)
            rc = proc.wait()
            assert rc == 0, 'See "%s".' % logfile


def test_molecule_list():
    proc = subprocess.Popen(['molecule', 'list'])
    rc = proc.wait()
    assert rc == 0


def test_default():
    molecule_test('default')


def test_git_test_source():
    molecule_test('git-test-source')


def test_multiple_testers():
    molecule_test('multiple-testers')


def test_multiple_test_source():
    molecule_test('multiple-test-sources')


def test_outputdir():
    molecule_test('outputdir')


def test_pre_test_source():
    molecule_test('pre-test-source')


def test_resources():
    molecule_test('resources')


def test_variablefiles():
    molecule_test('variablefiles')


def test_local_libs():
    molecule_test('local-libs')


@pytest.mark.parametrize('platform', sorted(PLATFORMS.keys()))
def test_vagrant(platform):
    molecule_test('vagrant', platform)
