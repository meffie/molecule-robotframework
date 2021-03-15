*******************************
Molecule Robot Framework Plugin
*******************************

Use Robot Framework as a Molecule verifier.

Runs the ``verify`` playbook to install Robot Framework, extra libraries, and
test data, then runs ``robot`` on the Molecule managed instances, showing the
live output as tests are executed.  Finally, runs an optional ``fetch_results``
playbook to retrieve the generated Robot Framework report and logs.

Documentation
=============

.. _installation-and-usage:

Installation and Usage
======================

Install molecule-robotframework:

.. code-block::

   pip install molecule molecule-robotframework

Create a new role with molecule using the robotframework verifier:

.. code-block::

   molecule init role <role_name> --verifier-name robotframework [--driver-name <name>]

Create a new scenario for an existing role or playbook:

.. code-block::

   molecule init scenario <scenario_name> --verifier-name robotframework [--driver-name <name>]

Copy the Robot Framework test data (.robot files) to a directory the Ansible
controller. The default location is the directory ``molecule/<scenario_name>/tests``.

Configure ``molecule.yml`` with the desired robot options in the verifier section.

Execute ``molecule test`` on the role or scenario to run the verify playbook and run
``robot`` on the molecule instance.

.. _authors:

Authors
=======

Molecule Robot Framework Plugin was created by Michael Meffie based on code from Molecule.

.. _license:

License
=======

The `MIT`_ License.

.. _`MIT`: https://github.com/ansible/molecule/blob/master/LICENSE

The logo is licensed under the `Creative Commons NoDerivatives 4.0 License`_.

If you have some other use in mind, contact us.

.. _`Creative Commons NoDerivatives 4.0 License`: https://creativecommons.org/licenses/by-nd/4.0/