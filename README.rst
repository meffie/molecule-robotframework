*******************************
Molecule Robot Framework Plugin
*******************************

Use Robot Framework as a Molecule verifier.

Runs the ``verify`` playbook to install Robot Framework, extra libraries, and
test data, then runs ``robot`` on the Molecule managed instances, showing the
live output as tests are executed.  Finally, runs an optional ``verify_fetch_report``
playbook to retrieve the generated Robot Framework report and logs.

Bundled ``verify`` and ``verify_fetch_report`` playbooks are included with
the plugin. You can override these with custom playbooks if desired.

Documentation: `https://molecule-robot-framework-plugin.readthedocs.io <https://molecule-robot-framework-plugin.readthedocs.io>`_

Installation and Usage
======================

Install molecule and molecule-robotframework:

.. code-block::

    $ python3 -m venv .venv
    $ source .venv/bin/activate
    (.venv) $ pip install molecule molecule-robotframework
    (.venv) $ patch-molecule-schema

Create a new scenario with molecule:

.. code-block::

    (.venv) $ molecule init scenario

Edit the ``molecule.yml`` file and set the verifier to ``molecule-robotframework``:

.. code-block::

    ...
    verifier:
      name: molecule-robotframework

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
