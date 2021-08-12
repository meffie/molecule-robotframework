Configuration
=============

Robot Framework verifier keywords.

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

test_directory
  Test destination path.

  Default: "." (current directory)

resource_directory
  Resource destination path.

  Default: "." (current directory)

test_data
  List of paths on the controller to Robot Framework test data directories (test suites).
  These files are copied to the ``test_directory``.

  Default: empty list

test_repos
  A list of dictionaries which describe git repositories of Robot Framework test data (test suites)
  to be installed on the test instances. Each item should have a ``name``, ``repo`` URI, and optional
  ``version`` (branch name or tag).

resources
  A list of jinja2 templates on the controller to be rendered to the ``resource_directory`` on the
  instances.

  Default: empty list

options
  The ``robot`` options as a dictionary. See the ``robot`` command for available options.

data_sources
  The ``robot`` data sources as a list of paths to tests and/or test suite directories.
