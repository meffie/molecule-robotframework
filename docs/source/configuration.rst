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

resources
  List of dictionaries to specify Robot Framework resource files to be
  installed on test instances. Resource files provide common settings and
  keywords. Resource files are imported using the Resource setting in the
  Settings table in your test files.  See Resources for keys.

  Default: (empty list)

variablefiles
  List of dictionaries to specify Robot Framework variable file templates to be
  rendered and installed on the test instances.  The molecule inventory variables
  may be used to generate the variable file.  This allows test data values to be
  customized in the molecule.yml file.

  Test data files can import variable files using the Variables setting in the
  Setting section. Another way to take variable files into use is using ``robot``
  option ``variablefile``.

  See Variablefiles for keys.

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

Resources
~~~~~~~~~

source
  The path to the resource file or template on the controller.

type
  The source file type, ``file`` or ``template``.

directory
  The destination path on the test instances.


Variablefiles
~~~~~~~~~~~~~

source
  The path to the variable file template on the controller.

directory
  The destination path on the test instances.
