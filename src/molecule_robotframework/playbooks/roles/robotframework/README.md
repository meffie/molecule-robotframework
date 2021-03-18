# Ansible Role: Robot Framework

Install the [Robot Framework](https://robotframework.org) test automation
framework, and optionally, one or more external test libraries.

This role will install Robot Framework with ``pip``. ``pip`` will be
installed if not already present. The EPEL repository will be installed on
RHEL/CentOS distributions in order to install ``pip``.

After importing this role, copy your test data and resources on the server,
the execute ``robot`` to run tests.

## Requirements

Ansible 2.10 or later.

## Role Variables

Available variables are listed below, along with default values (see `defaults/main.yml`):

    robotframework_package_name

The Robot Framework pip package name. Default value is `robotframework`.

    robotframework_package_version_spec

The `pip` version specification to install a specific Robot Framework version.
The default value is empty, so `pip` will install the latest when Robot Framework
is not already present.

    robotframework_external_libraries

A list of external Robot Framework libraries to be installed via `pip`. The
default list is empty.

## Dependencies

None

## Example Playbook

    - hosts: testers
      roles:
        - robotframework
      tasks:
        - name: Copy test data
          copy:
            src: /path/to/tests/on/controller
            src: /path/to/my/test/data/

        - name: Run tests
          command: robot /path/to/my/test/data

## License

MIT
