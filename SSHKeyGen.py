#!/usr/bin/env python3
# Run the ssh-keygen command on the Admin vagrant box
#

import os
import os.path
import sys
import json

def RunSSHKeyGen():
    """Run the ssh-keygen command"""
    import pexpect

    #cmd = "ssh-keygen -t rsa"
    cmd = "ssh-keygen -t rsa -f /home/vagrant/.ssh/id_rsa"
    child = pexpect.spawn(cmd)
    logname = 'sshkeylog.txt'
    if os.path.isfile(logname):
        plslog = open(logname, 'r+b')
    else:
        plslog = open(logname, 'wb')
    child.logfile = plslog
    try:
        index = child.expect(['\/id_rsa\):','use -f option\)','verification failed.', pexpect.EOF], timeout=20)
        if index == 0:
            child.sendline('\r\n')
            #child.expect('Overwrite \(y\/n\)?')
            #child.sendline('y\r\n')
            child.expect('no passphrase\):')
            child.sendline('\r\n')
            child.expect('passphrase again:')
            child.sendline('\r\n')
            child.expect('-----+')
            child.sendline('\r\n')
            child.sendline('\r\n')
        elif index == 1:
            print("WARNING: Key Already Exists")
            print(child.before,child.after)
        elif index == 2:
            print("ERROR: Remote Host Identification Has Changed!")
            print("       Remove existing key with:")
            print("       ssh-keygen -f \"/home/thor/.ssh/known_hosts\" -R \"[127.0.0.1]:{0}".format(portnum))
        elif index == 3:
            print("EOF ERROR: ")
            print(child.before,child.after)
        else:
            print("UNKNOWN ERROR OCCURRED: ")
            print(child.before,child.after)
            
    except pexpect.TIMEOUT:
        print("TIMEOUT Exception was Thrown")
        print("debug information:")
        print("DEBUG INFO (child): " + str(child))
        child.close()
    else:
        plslog.close()
    
if __name__ == "__main__":
    RunSSHKeyGen()






