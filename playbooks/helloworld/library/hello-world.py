#!/usr/bin/env python3



def RunModule():

    module = AnsibleModule(argument_spec={})
    response = {"hello": "world"}
    module.exit_json(changed=False, meta=response)


#from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.basic import *

if __name__ == '__main__':
    RunModule()
