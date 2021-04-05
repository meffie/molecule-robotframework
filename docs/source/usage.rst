Usage
=====

Create a new scenario for an existing role or playbook:

.. code-block::

   molecule init scenario <scenario_name> --verifier-name robotframework [--driver-name <name>]

Copy the Robot Framework test data (.robot files) to a directory the Ansible
controller. The default location is the directory ``molecule/<scenario_name>/tests``.

Configure the desired ``robot`` options in the ``molecule.yml`` verifier section.
Example code:

.. code-block:: yaml

   verifier:
      name: robotframework
      libraries:
         - robotframework-openafslibrary
      test_data:
         - ${MOLECULE_SCENARIO_DIRECTORY}/tests/
      resources:
         - ${MOLECULE_SCENARIO_DIRECTORY}/templates/myvars.py.j2
      options:
         exitonerror: yes
         exclude: bogus
         report: index.html
      data_sources:
         - example.robot


Execute ``molecule test`` to run the full molecule sequence, or ``molecule
converge`` then ``molecule verify`` to converge then run the Robot Framework
tests.

By default, ``robot`` will be run on each instance in the scenario, one
instance at a time. Set the ``group`` option to limit which instances the
plugin will run robot.

A ``robot`` arguments file is created on the test instance. This can be used
to manually run the ``robot`` command after ``molecule verify`` and before
``molecule destroy``. To run the tests manually, run ``molecule login`` to logon
to the test instance, the run ``robot -A robotrc <path-to-tests>``.
