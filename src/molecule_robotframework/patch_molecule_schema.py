#
#  Copyright (c) 2020-2024 Sine Nomine Associates
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

#
# Usage: python patch_molecule_schema.py
#
# Add 'robotframework' to the verifier names in the installed molecule schema
# file.  Unfortunately, the verifier name list was hardcoded in molecule as of
# version 4.0.2 so a local change is required to be able to load the
# molecule-robotframe verifier plugin.
#

"""Patch Robot Framework Schema."""

import os
import sys
import json
import molecule.data


def main():
    schema_file = os.path.dirname(molecule.data.__file__) + '/molecule.json'
    print('Reading file ' + schema_file)
    with open(schema_file, encoding='utf-8') as f:
        schema = json.load(f)

    try:
        names = schema['$defs']['VerifierModel']['properties']['name']['enum']
    except KeyError:
        sys.exit('Unexpected schema in file ' + schema_file)

    if 'molecule-robotframework' in names:
        print('Skipping: Schema already patched.')
    else:
        os.rename(schema_file, schema_file + '.orig')
        names.append('molecule-robotframework')
        with open(schema_file, 'w', encoding='utf-8') as f:
            json.dump(schema, f, indent=2)
        print('Updated file ' + schema_file)


if __name__ == '__main__':
    main()
