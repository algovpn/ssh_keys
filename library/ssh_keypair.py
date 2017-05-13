#!/usr/bin/python

# (c) 2017, defunct <https://keybase.io/defunct>
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.

import os
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends.openssl.backend import backend
from ansible.module_utils.basic import *


def main():
    mod = AnsibleModule(
        argument_spec=dict(
            base_name=dict(required=True, type='str'),
            output_path=dict(type='str'),
            overwrite=dict(default=False, type='bool'),
            curve=dict(default='prime256v1', type='str')
        ),
        supports_check_mode=True,
        add_file_common_args=True,
    )

    if mod.params.get('curve') not in ec._CURVE_TYPES.keys():
        mod.fail_json(msg='Curve %s is not a valid curve type.' % mod.params.get('curve'))

    key = ec.generate_private_key(
        backend=backend,
        curve=ec._CURVE_TYPES[mod.params.get('curve')]
    )

    priv_key = key.private_bytes(
        serialization.Encoding.PEM,
        serialization.PrivateFormat.PKCS8,
        serialization.NoEncryption()
    )

    pub_key = key.public_key().public_bytes(
        serialization.Encoding.OpenSSH,
        serialization.PublicFormat.OpenSSH
    )

    out = {
        'changed': True,
        'result': {
            'pub': pub_key,
            'priv': priv_key
        }
    }

    if mod.params.get('output_path'):
        path = os.path.expanduser(mod.params.get('output_path'))
        basefile = path + '/' + mod.params.get('base_name')
        if not os.path.exists(path):
            os.makedirs(path)
        pemfile = basefile + '.pem'
        pubfile = basefile + '.pub'
        if mod.params.get('overwrite') and os.path.isfile(pemfile)\
                or not os.path.isfile(pemfile):
            with open(pemfile, 'w') as pem:
                pem.write(out['result']['priv'])
        else:
            with open(pemfile, 'r') as pem:
                out['result']['priv'] = pem.read()

        if mod.params.get('overwrite') and os.path.isfile(pubfile)\
                or not os.path.isfile(pubfile):
            with open(pubfile, 'w') as pub:
                pub.write(out['result']['pub'])
        else:
            with open(pubfile, 'r') as pub:
                out['result']['pub'] = pub.read()

    mod.exit_json(**out)


if __name__ == '__main__':
    main()
