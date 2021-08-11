#  Copyright (c) 2020-2021 Sine Nomine Associates
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to
#  deal in the Software without restriction, including without limitation the
#  rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
#  sell copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#  FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#  DEALINGS IN THE SOFTWARE.

"""Robot Framework Verifier Module."""

import os

try:
    from shlex import join as join_args
    assert join_args  # hush pyflakes
except ImportError:
    from subprocess import list2cmdline as join_args

from molecule import logger
from molecule import util
from molecule.provisioner import ansible_playbook, ansible_playbooks
from molecule.api import Verifier

LOG = logger.get_logger(__name__)

def dict2args(data):
    """Convert a dictionary of options to command like arguments.

    Note: This implementation supports arguments with multiple values.
    """
    result = []
    for k, v in data.items():
        if v is not False:
            prefix = "-" if len(k) == 1 else "--"
            flag = f"{prefix}{k}".replace("_", "-")
            if v is True:
                result.append(flag)
            elif isinstance(v, (tuple, list)):
                for x in v:
                    result.extend([flag, str(x)])
            else:
                result.extend([flag, str(v)])
    return result

def dict2lines(data, getlines=False):
    """Convert a dictionary of options to a list of lines for robot --argumentfile."""
    result = []
    for k, v in data.items():
        if v is not False:
            prefix = "-" if len(k) == 1 else "--"
            flag = f"{prefix}{k}".replace("_", "-")
            if v is True:
                result.append(flag + '\n')
            elif isinstance(v, (tuple, list)):
                for x in v:
                    result.append(join_args([flag, str(x)]) + '\n')
            else:
                result.append(join_args([flag, str(v)]) + '\n')
    return result

class Robotframework(Verifier):
    """
    `Robotframework`_ is not default test verifier.

    The robotframework test verifier runs the verify playbook to install
    Robot Framework, external Robot Framework libraries, and the test data
    sources to the test instances, then runs the ``robot`` command, showing the
    live test output. Finally, the optional ``verify_fetch_report`` playbook is
    executed to retrieve the test logs.

    Bundled ``verify.yml`` and ``verify_fetch_report.yml`` playbooks are provided
    by the plugin. You can customize these plays by creating ``verify.yml``
    and/or ``verify_fetch_report.yml`` in your scenario directory.

    The testing can be disabled by setting ``enabled`` to False.

    .. code-block:: yaml

        verifier:
          name: robotframework
          enabled: False

    Options to ``robot`` can be passed to through the options dict. See the ``robot``
    command help for a complete list of options.

    .. code-block:: yaml

        verifier:
          name: robotframework
          options:
            dryrun: yes
            exitonerror: yes
            include: mytag

    The data sources arguments to ``robot`` can be passed through the ``data_sources``
    list. The default data_sources is 'tests'.

    .. code-block:: yaml

        verifier:
          name: robotframework
          data_sources:
            - test/example.robot

    Environment variables can be passed to the verifier.

    .. code-block:: yaml

        verifier:
          name: robotframework
          env:
            ROBOT_SYSLOG_FILE: /tmp/syslog.txt

    Paths to the test data sources to be copied to the test instance(s)
    Provide a list of fully qualified paths to directories on the
    controller. The default is an empty list.  An external ``verify.yml``
    playbook can be provided if you want to copy your tests from another
    source, such as a git checkout.

    .. code-block:: yaml

        verifier:
          name: robotframework
          test_data:
            - /path/to/my/tests/on/the/controller
            - /path/to/more/tests/on/the/controller

    The destination path to install ``test_data`` files on the
    test instance(s). This directory will be created on the instance
    if it does not already exist.

    .. code-block:: yaml

        verifier:
          name: robotframework
          test_dest: /path/to/install/test_files/on/instance

    External Robot Framework libraries to install on the test instances
    with pip.

    .. code-block:: yaml

        verifier:
          name: robotframework
          libraries:
            - robotframework-sshlibrary
            - robotframework-openafslibrary

    The inventory group name of the test instances. Defaults to 'all'.

    .. code-block:: yaml

        verifier:
          name: robotframework
          group: testers

    .. _`Robotframework`: https://robotframework.org
    """

    def __init__(self, config=None):
        super(Robotframework, self).__init__(config)
        self._robot_command = None
        self._playbooks = None

    @property
    def name(self):
        return 'robotframework'

    @property
    def default_options(self):
        return {}

    @property
    def default_env(self):
        return util.merge_dicts(os.environ.copy(), self._config.env)

    @property
    def playbooks(self):
        if not self._playbooks:
            # Inject a default verify_fetch_report playbook filename.
            if 'verify_fetch_report' not in self._config.config['provisioner']['playbooks']:
                self._config.config['provisioner']['playbooks']['verify_fetch_report'] = 'verify_fetch_report.yml'
            self._playbooks = ansible_playbooks.AnsiblePlaybooks(self._config)
        return self._playbooks

    def execute_playbook(self, name):
        """Excute the named playbook."""
        # First look for the user provided playbook in the scenario directory.
        # If not found, use the playbook bundled with the plugin.
        playbook = self.playbooks._get_playbook(name)
        if not playbook or not os.path.isfile(playbook):
            playbook = self._get_bundled_playbook(name)
        pb = ansible_playbook.AnsiblePlaybook(playbook, self._config)
        # Target just the testers (all by default.)
        pb.add_cli_arg('extra_vars', f'molecule_robotframework_hosts={self.test_group}')
        pb.execute()

    @property
    def ansible_args(self):
        return self._config.config['provisioner']['ansible_args']

    @property
    def test_group(self):
        return self._config.config['verifier'].get('group', 'all')

    @property
    def robot_options(self):
        return self._config.config['verifier'].get('options', {})

    @property
    def data_sources(self):
        return self._config.config['verifier'].get('data_sources', ['tests'])

    @property
    def test_hosts(self):
        inventory = self._config.provisioner.inventory
        return inventory.get(self.test_group, inventory.get('all', {})).get('hosts', {})

    @property
    def argumentfile(self):
        return os.path.join(self._config.scenario.ephemeral_directory, 'robotrc')

    def bake(self, name, host):
        """Prepare a command to run robot on a test instance."""

        # The robot command line.
        robot_cmd = [
            'robot',
            *dict2args(self.robot_options),
            *self.data_sources # last
        ]
        LOG.info('robot command: %s' % ' '.join(robot_cmd))

        ansible_connection = host.get('ansible_connection', 'ssh')
        if ansible_connection == 'docker':
            cmd = [
                'docker',
                'exec',
                name,
                *robot_cmd  # last
            ]
        elif ansible_connection == 'ssh':
            ssh_args = host['ansible_ssh_common_args'].split()
            ssh_dest = '@'.join((host['ansible_user'], host['ansible_host']))
            cmd = [
                'ssh',
                '-p', host['ansible_port'],
                '-i', host['ansible_private_key_file'],
                *ssh_args,
                ssh_dest,
                *robot_cmd, # last
            ]
        else:
            util.sysexit_with_message("Unsupported connection: {{ansible_connection}}", 1)

        self._robot_command = util.BakedCommand(
            cmd=cmd,
            cwd=self._config.scenario.directory,
            env=self.env,
        )

    def execute(self):
        """
        Execute the robotframework verifier.

        First run the verify playbook (if provided) to install
        robotframework, libraries, and test data. Next, run ``robot`` on each
        host in the test group (``all`` by default). Show the live output of
        the ``robot`` command. Finally, run an optional playbook called
        ``verify_fetch_report`` to retrieve the ``robot`` output files.
        """
        if not self.enabled:
            LOG.warning('Skipping, verifier is disabled.')
            return

        # Save the robot args to a file in our ephemeral directory before
        # running the verify playbook.
        with open(self.argumentfile, 'w') as fh:
            fh.writelines(dict2lines(self.robot_options))

        LOG.info('Prepare for verification.')
        self.execute_playbook('verify')

        LOG.info('Running robotframework verifier tests.')
        verified = None
        for name, host in self.test_hosts.items():
            self.bake(name, host)
            LOG.info(f'Running robotframework tests on instance {name}.')
            result = util.run_command(self._robot_command, debug=self._config.debug)
            LOG.info(f"robot return code: {result.returncode}")
            if result.returncode == 0:
                verified = True
            else:
                verified = False
                LOG.error(f"Failed to run command: {result.args}")

        LOG.info('Download report files.')
        self.execute_playbook('verify_fetch_report')

        if verified:
            LOG.info('Verifier completed successfully.')
        else:
            LOG.error('Verification failed.')

    def schema(self):
        return {
            "verifier": {
                "type": "dict",
                "schema": {
                    "name": {"type": "string", "allowed": ["robotframework"]},
                },
            }
        }

    def template_dir(self):
        """Return the path to the cookiecutter templates for molecule init."""
        return os.path.abspath(os.path.join(os.path.dirname(__file__), "cookiecutter"))

    def _get_bundled_playbook(self, name):
        """Lookup our bundled playbook."""
        playbooks = os.path.abspath(os.path.join(os.path.dirname(__file__), "playbooks"))
        path = os.path.join(playbooks, f"{name}.yml")
        if not os.path.isfile(path):
            raise AssertionError(f"Failed to lookup bundled {name}.yml playbook.")
        return path
