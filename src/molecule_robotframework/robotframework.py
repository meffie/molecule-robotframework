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

from molecule import logger
from molecule import util
from molecule.provisioner import ansible_playbook, ansible_playbooks
from molecule.api import Verifier

LOG = logger.get_logger(__name__)

class Robotframework(Verifier):
    """
    `Robotframework`_ is not default test verifier.

    The robotframework test verifier runs the verify playbook to install
    Robot Framework, external Robot Framework libraries, and the test data
    sources to the test instances, then runs the ``robot`` command, showing the
    live test output. Finally, the optional ``fetch_results`` playbook is
    executed to retrieve the test logs.

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

    Path to the test data sources to copy to the test instance and
    destination path on the test instance. The source defaults to 'test'
    in the scenario directory. The destination defaults to '.' on the
    test instance.

    .. code-block:: yaml

        verifier:
          name: robotframework
          testdata:
            src: /path/to/my/tests
            dest: /tmp/tests

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
            # Inject a default fetch_results playbook filename.
            if 'fetch_results' not in self._config.config['provisioner']['playbooks']:
                self._config.config['provisioner']['playbooks']['fetch_results'] = 'fetch_results.yml'
            self._playbooks = ansible_playbooks.AnsiblePlaybooks(self._config)
        return self._playbooks

    def execute_playbook(self, name):
        playbook = self.playbooks._get_playbook(name)
        if not os.path.exists(playbook):
            LOG.info('Skipping playbook f{name}, not found.')
            return
        pb = ansible_playbook.AnsiblePlaybook(playbook, self._config)
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
        data_sources = self._config.config['verifier'].get('data_sources', ['tests'])
        return data_sources

    @property
    def test_hosts(self):
        inventory = self._config.provisioner.inventory
        return inventory.get(self.test_group, inventory.get('all', {})).get('hosts', {})

    def bake(self, name, host):
        """Prepare a command to run robot on a test instance."""
        robot_cmd=[
            'robot',
            *util.dict2args(self.robot_options),
            *self.data_sources # last
        ]
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
        ``fetch_results`` to retrieve the ``robot`` output files.
        """
        if not self.enabled:
            LOG.warning('Skipping, verifier is disabled.')
            return

        LOG.info('Running robotframework verifier playbook.')
        self.execute_playbook('verify')

        LOG.info('Running robotframework verifier tests.')
        for name, host in self.test_hosts.items():
            self.bake(name, host)
            LOG.info(f'Running robotframework tests on instance {name}.')
            result = util.run_command(self._robot_command, debug=self._config.debug)
            if result.returncode != 0:
                util.sysexit_with_message(
                    f"Failed to run robot: {result.returncode}, command was: {result.args}",
                    result.returncode,
                )

        LOG.info('Retrieve output/log/report files.')
        self.execute_playbook('fetch_results')

        LOG.info('Verifier completed successfully.')

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
        p = os.path.abspath(os.path.join(os.path.dirname(__file__), "cookiecutter"))
        return p
