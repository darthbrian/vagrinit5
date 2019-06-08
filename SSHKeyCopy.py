#!/usr/bin/env python3
# set up passwordless ssh on each vagrant box
#

import os
import sys
import json

def CopyToGuest(ipaddr):
    """copy passwordless ssh key for each guest"""
    #pingsuccess = 0
    import pexpect

    cmd = "ssh-copy-id -i /home/vagrant/.ssh/id_rsa.pub vagrant@{0}".format(ipaddr)
    child = pexpect.spawn(cmd)
    plslog = open('sshcopylog.txt', 'wb')
    child.logfile = plslog
    try:
        index = child.expect(['continue connecting \(yes/no\)?','use -f option\)','verification failed.', pexpect.EOF], timeout=20)
        if index == 0:
            child.sendline('yes')
            child.expect('password:')
            child.sendline('vagrant')
            child.expect('were added.')
            child.sendline('\r\n')
        elif index == 1:
            print("WARNING: Key Already Exists")
            print(child.before,child.after)
        elif index == 2:
            print("ERROR: Remote Host Identification Has Changed!")
            print("       Remove existing key with:")
            print("       ssh-keygen -f \"/home/thor/.ssh/known_hosts\" -R \"[{0}]".format(ipaddr))
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
    
def SSHCopyKeys():
    """loop through our list of machines and for each one copy the Admin's public key to all the guests"""

    #open json file with IP data
    with open('/vagrant/iphost.json', 'r') as ipfile:
        #get dictionary data
        ipdata = json.load(ipfile)

        #loop through ports
        count = 0
        for guestip in ipdata['Admin']:
            #copy the public key the current target machine
            CopyToGuest(guestip)
            count += 1
        return count

if __name__ == "__main__":
    GuestCount = SSHCopyKeys()
