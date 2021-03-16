"""Functional tests."""
import os
import yaml
from pathlib import Path
from contextlib import contextmanager

from click.testing import CliRunner
import pytest

from molecule.util import run_command

@contextmanager
def change_dir(path):
    prev = Path.cwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(prev)

def test_molecule_init():
    """Verify that init scenario works."""
    cmd = ['molecule', 'init', 'role', 'test-init', '--verifier-name', 'robotframework']
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = run_command(cmd)
        assert result.returncode == 0
        verify_yml = Path('./test-init/molecule/default/verify.yml')
        assert verify_yml.exists()
        assert verify_yml.is_file()
        assert 'robotframework' in verify_yml.read_text()

@pytest.mark.parametrize(
    ('scenario_to_test', 'image'),
    [
        ('libvirt', 'generic-centos-7'),
        ('libvirt', 'generic-centos-8'),
        ('libvirt', 'generic-debian-9'),
        ('libvirt', 'generic-debian-10'),
        ('docker', 'docker.io/pycontribs/centos:8'),
        ('vagrant', 'generic/centos8'),
    ]
)
def test_molecule_scenario(scenario_to_test, image):
    #image_name = image.replace('/', '-').replace(':', '-')
    #tmp = Path('/tmp/scenario-%s-%s.txt' % (scenario_to_test, image_name))
    basedir = Path(__file__).resolve().parent
    testdir = basedir / 'scenarios' / scenario_to_test
    with change_dir(testdir):
        env = yaml.dump({'IMAGE': image})
        Path('.env.yml').write_text(env)
        result = run_command(['molecule', 'test'])
        #tmp.write_text(result.output)
        assert result.returncode == 0
