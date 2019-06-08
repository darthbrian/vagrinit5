#!/usr/bin/env python
# This program will be called remotely from the host so that it can ping all its neighbors. 
# We write the data to an output file.

import os
import json


def PingGuest(machname, iplist):
    """ping each guest from the specified guest"""
    #Open our output file
    with open('/vagrant/pingstatus/' + machname + '_ping.out', 'w') as outfile:
        pingsuccess = 0
        num_of_ips = len(iplist)
        outfile.write("*** " + machname + " is currently attempting to ping all guests on the private Vagrant network. ***\n")
        for eachip in iplist:
            #use system command to ping
            response = os.system("ping -c 1 " + str(eachip) + " > /dev/null 2>&1")
            if response == 0:
                pingsuccess += 1
                outfile.write('{0} has successfully pinged IP {1}\n'.format(machname, str(eachip)))
            else:
                outfile.write('***ERROR: Vagrant machine {0} was unable to ping guest with IP {1}\n'.format(machname, eachip))

        if pingsuccess == num_of_ips:
            outfile.write(machname + ' has successfully pinged all guests on the private Vagrant network.\n')
        else:
            outfile.write('>>> ERROR: ' + machname + ' was not able to ping one or more machines on the private Vagrant network. <<<\n')

def GetGuestList(machname):
    """determine which IPs need to be pinged and build a list"""

    #open json file with IP data
    with open('/vagrant/iphost.json', 'r') as ipfile:
        #get dictionary data
        ipdata = json.load(ipfile)

        #loop through machines
        for curname in ipdata:
            #for each machine...
            if curname == machname:
                iplist = ipdata[curname]

                #ping all the other machines
                PingGuest(machname, iplist)

if __name__ == "__main__":
    import argparse
    """The list of machines to ping are passed in as arguments. We parse them out via argparse and the 'pinglist' argument."""
    parser = argparse.ArgumentParser()
    parser.add_argument("machname", help = "The name of virtual machine that is doing the pinging")
    args = parser.parse_args()
    GetGuestList(args.machname)
