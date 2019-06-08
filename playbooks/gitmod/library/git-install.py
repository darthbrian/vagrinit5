#!/usr/bin/python

def InstallGit():
    import subprocess
    status = subprocess.call(["touch", "InstallGit.txt"])
    status = status + subprocess.call(["/usr/bin/apt-get", "update"])
    status = status + subprocess.call(["/usr/bin/apt-get",  "install git-core -y"])
    #call(["apt-get", "update"])
    #call(["sudo", "apt-get install -y git-all >/dev/null 2>&1"])
    #call(["apt-get", "install -y git-all"])
    #sudo apt-get update >/dev/null 2>&1
    #sudo apt-get install -y git-all >/dev/null 2>&1
    return status

def RunModule():

    module = AnsibleModule(argument_spec={})
    response = {"git": "install"}

    status = InstallGit()

    if status == 0:
        module.exit_json(changed=True, meta=response)
    else:
        module.fail_json(changed=False, meta="It didn't work")


from ansible.module_utils.basic import *

if __name__ == '__main__':
    RunModule()
