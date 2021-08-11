Configuration
=============

Robot Framework verifier keywords.

name
  Verifier name: ``robotframework``
  Required: yes

group
  The ansible group to run ``robot``. Set this to a group name when
  you have multiple instances in the scenario and you want to limit
  which instances are verified.

  Default: all

install
  Indicates if Robot Framework and the Test Libraries are to be installed before
  running the tests. Values are 'yes' (True), 'no' (False), or 'auto'.  When
  'auto', Robot Framework will be installed the first time the verifier is run
  on an instance, and the installation will be skipped on subsequent runs.  The
  python ``pip`` program will be installed on the instance, and then ``pip``
  will be used to install Robot Framework and any libraries listed by ``libraries``
  (see below).

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
  ``version`` (branch name or tag). Eample.

resources
  A list of jinja2 templates on the controller to be rendered to the ``resource_directory`` on the
  instances.

  Default: empty list

options
  The ``robot`` options as a dictionary. See the ``robot`` command for available options.

data_sources
  The ``robot`` data sources as a list of paths to tests and/or test suite directories.
