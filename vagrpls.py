#!/usr/bin/env python3
# set up passwordless ssh on each vagrant box
#

import os
import sys
import json

def GetPortNum(curmachname):
    import csv

    #first we need to call the 'vagrant port' command for the current machine to get our info in csv format
    response = os.system("vagrant port {0} --machine-readable > ./pingcsv/{0}.csv ".format(curmachname))

    with open('./pingcsv/{0}.csv'.format(curmachname), newline='') as f:
        reader = csv.reader(f)
        rownum = 1
        for row in reader:
            if rownum == 5:
                #The 4th element in the list is the forwarded port number
                return row[4]
            rownum += 1

def PlsGuest(machname):
    """copy passwordless ssh key for each guest"""
    #pingsuccess = 0
    import pexpect

    portnum = str(GetPortNum(machname))
    cmd = "ssh-copy-id -i /home/thor/.ssh/id_rsa.pub vagrant@127.0.0.1 -p {0}".format(portnum)
    child = pexpect.spawn(cmd)
    plslog = open('plslog.txt', 'wb')
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
    
def PingEachGuest():
    """loop through our list of machines and for each one ping all the other guests"""

    #open json file with IP data
    with open('iphost.json', 'r') as ipfile:
        #get dictionary data
        ipdata = json.load(ipfile)

        #loop through machines
        count = 0
        for guestname in ipdata:
            #ping the current machine
            PlsGuest(guestname)
            count += 1
        return count

if __name__ == "__main__":
    GuestCount = PingEachGuest()
