#
# Usage: python patch_molecule_schema.py
#
# Add 'robotframework' to the verifier names in the installed molecule schema
# file.  Unfortunately, this name list was hardcoded in molecule as of version 4.0.2
# so a local change is required to be able to load the molecule-robotframe
# verifier plugin.
#

import os
import sys
import json
import molecule.data

schema_file = os.path.dirname(molecule.data.__file__) + '/molecule.json'
with open(schema_file, encoding='utf-8') as f:
    schema = json.load(f)

try:
    names = schema['$defs']['VerifierModel']['properties']['name']['enum']
except KeyError as e:
    sys.exit(f'Unexpected schema in file {schema_file}.')

if 'robotframework' in names:
    print('Schema is already up to date.')
else:
    print('Updating ' + schema_file)
    os.rename(schema_file, schema_file + '.orig')
    names.append('robotframework')
    with open(schema_file, 'w', encoding='utf-8') as f:
        json.dump(schema, f, indent=2)
