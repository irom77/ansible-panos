# Ansible Collection - irom77.panos

- ansible-doc irom77.panos.panos_tags

# Requirements

- Ansible >= 2.9
- Python >= 3.6

# Example usage

See examples directory

```
$ ansible-galaxy collection install irom77.panos
Starting galaxy collection install process
Process install dependency map
Starting collection install process
Installing 'irom77.panos:1.0.0' to '/home/docker/.ansible/collections/ansible_collections/irom77/panos'
Downloading https://galaxy.ansible.com/download/irom77-panos-1.0.0.tar.gz to /home/docker/.ansible/tmp/ansible-local-27008mhvmdaft/tmpoe95ctrr
irom77.panos (1.0.0) was installed successfully

ansible-playbook mod_test_panos_tags.yml --ask-vault-pass
Vault password: 
[WARNING]: provided hosts list is empty, only localhost is available. Note that the implicit localhost does not match 'all'

PLAY [Test panos_tags module] *************************************************************************************************************************************************************
TASK [Gathering Facts] ********************************************************************************************************************************************************************ok: [localhost]

TASK [Register addresses] *****************************************************************************************************************************************************************changed: [localhost]

TASK [debug] ******************************************************************************************************************************************************************************ok: [localhost] => {
    "addresses": {
        "changed": true,
        "debug_msg": "{\"10.1.131.7\": \"https://10.1.131.7/api?type=user-id&cmd=<uid-message><type>update</type><payload><register><entry ip=\\\"1.2.3.1\\\" persistent=\\\"1\\\"><tag><member timeout=\\\"0\\\">azure-tag.dt2</member></tag></entry></register><register><entry ip=\\\"1.2.3.3\\\" persistent=\\\"1\\\"><tag><member timeout=\\\"0\\\">azure-tag.dt2</member></tag></entry></register><unregister><entry ip=\\\"10.102.9.35\\\" persistent=\\\"1\\\"><tag><member timeout=\\\"0\\\">azure-tag.dt2</member></tag></entry></unregister><unregister><entry ip=\\\"10.102.9.34\\\" persistent=\\\"1\\\"><tag><member timeout=\\\"0\\\">azure-tag.dt2</member></tag></entry></unregister><unregister><entry ip=\\\"10.102.9.16\\\" persistent=\\\"1\\\"><tag><member timeout=\\\"0\\\">azure-tag.dt2</member></tag></entry></unregister><unregister><entry ip=\\\"10.102.9.17\\\" persistent=\\\"1\\\"><tag><member timeout=\\\"0\\\">azure-tag.dt2</member></tag></entry></unregister><unregister><entry ip=\\\"10.102.9.30\\\" persistent=\\\"1\\\"><tag><member timeout=\\\"0\\\">azure-tag.dt2</member></tag></entry></unregister><unregister><entry ip=\\\"10.102.9.7\\\" persistent=\\\"1\\\"><tag><member timeout=\\\"0\\\">azure-tag.dt2</member></tag></entry></unregister><unregister><entry ip=\\\"10.102.9.23\\\" persistent=\\\"1\\\"><tag><member timeout=\\\"0\\\">azure-tag.dt2</member></tag></entry></unregister><unregister><entry ip=\\\"10.102.9.8\\\" persistent=\\\"1\\\"><tag><member timeout=\\\"0\\\">azure-tag.dt2</member></tag></entry></unregister><unregister><entry ip=\\\"10.102.9.24\\\" persistent=\\\"1\\\"><tag><member timeout=\\\"0\\\">azure-tag.dt2</member></tag></entry></unregister></payload></uid-message>\"}",
        "failed": false,
        "meta": {
            "deregister": [
                "10.12.9.35",
                "10.12.9.34",
                "10.12.9.16",
                "10.12.9.17",
                "10.12.9.30",
                "10.12.9.7",
                "10.12.9.23",
                "10.12.9.8",
                "10.12.9.24"
            ],
            "register": [
                "1.2.3.1",
                "1.2.3.3"
            ]
        }
    }
}

PLAY RECAP ********************************************************************************************************************************************************************************localhost                  : ok=3    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```