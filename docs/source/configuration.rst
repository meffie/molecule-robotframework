Configuration
=============

Robot Framework verifier keywords.

Verifier
~~~~~~~~

name
  Verifier name: ``robotframework``
  Required: yes

group
  The Ansible group to run ``robot``. Set this to a group name when
  you have multiple instances in the scenario and you want to limit
  which instances are verified.

  Default: all

install
  Indicates if Robot Framework and the test libraries are to be installed before
  running the tests. Values are ``always``, ``never``, or ``auto``. When the
  value is ``never``, the verifier does not install the Robot Framework. When
  the value is ``always``, the verifier ensures the Robot Framework is installed
  before running the ``robot`` command. When the value is ``auto``, the verifier
  installs the Robot Framework the first time it is run, and installation will
  be skipped on subsequent runs.  When Robot Framework is installed, first
  ``pip`` will be installed on the instance, then ``pip`` will be used to
  install Robot Framework and any test libraries indicated by the ``libraries``
  configuration option (see ``libraries`` below).

  Default: auto

libraries
  A list of Robot Framework libraries to be installed with ``pip`` when ``install``
  is true or is 'auto' and this is the first time the verifier is run.

  Default: (empty list)

tests
  List of dictionaries to specify the Robot Framework test sources to be
  installed and executed. See Test Sources for keys.

  Default: (empty list)

resource_directory
  Resource destination path.

  Default: "." (current directory)

resources
  A list of jinja2 templates on the controller to be rendered to the ``resource_directory`` on the
  instances.

  Default: (empty list)

options
  The ``robot`` options as a dictionary. See the ``robot`` command for available options.


Test Sources
~~~~~~~~~~~~

name
  Destination directory on the instance.

  Default: 'tests'

type
  The test source type. Valid values are:

  * ``dir`` - copy the tests from the controller to the test instance
  * ``git`` - checkout the tests from a git repo
  * ``pre`` - run pre-loaded tests

  Default: ``dir``

source
  When type is ``dir``, the path to the tests on the controller.  When type is
  ``git``, the URL of the git repository to be checked out on the test instance.

version
  When the type is ``git``, the branch or tag name to be checked out.

  Default: 'master'

execute
  The files or directories to be be executed by robot.  The value of execute
  may be a single string or a list of strings.

  The destination directory specified by the ``name`` key is automatically
  prepended to each element.

  Default: 'tests'
