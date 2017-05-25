algovpn.ssh_keys
================

SSH key generation and management for AlgoVPN.

Role Variables
--------------

| Name           | Default Value | Description                        |
| -------------- | ------------- | -----------------------------------|
| `ssh_keys_name` | algo | The base name for the ssh key |
| `ssh_keys_curve` | prime256v1 | The curve name to use for key generation |
| `ssh_keys_overwrite` | false | Overwrite existing SSH keys |
| `ssh_keys_output_path` | None | Output path for SSH key storage |

Registered Variables
--------------------
Variables available after this role has been included.

| Name           | Default Value | Description                        |
| -------------- | ------------- | -----------------------------------|
| `ssh_keys`| dict(`output`) | The public / private keypair |

`output`:
```
{
    'result': {
        'pub': pub_key,
        'priv': priv_key
    }
}
```

Example Playbook
----------------

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:

    - hosts: servers
      roles:
         - { role: algovpn.ssh_keys, ssh_keys_name: master, ssh_keys_output_path: ~/.ssh }

License
-------

MIT

Author Information
------------------

AlgoVPN