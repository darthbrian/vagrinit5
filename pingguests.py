#!/usr/bin/env python3
# This program automatically pings all the guests in a vagrant environment consisting of multiple boxes. 
# We read in a JSON file created when vagrinit4 runs and walk over the IPs.
# Can issue a command to a guest to ping another guest with this command : vagrant ssh <guest1> -c 1 'ping <guest 2>'

import os
import json
import paramiko

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
                #print(row[4:5])
                return row[4]
            rownum += 1

def PingGuest(machname):
    """ping each guest from the specified guest"""
    pingsuccess = 0

    # To use paramiko we need the port number of the current machine
    portnum = str(GetPortNum(machname))

    # Run the process on the guest machine using paramiko
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('127.0.0.1', portnum, 'vagrant', 'vagrant')
    command = "/vagrant/guestping.py {0} &".format(machname)
    (stdin, stdout, stderr) = ssh.exec_command(command)

    # Check for errors
    output = stderr.readlines()
    if output != []:
        print('Error: {0}\n'.format(output))
    ssh.close()

def PingEachGuest():
    """loop through our list of machines and for each one ping all the other guests"""

    # Open json file with IP data
    with open('iphost.json', 'r') as ipfile:
        # Get dictionary data
        ipdata = json.load(ipfile)

        # Loop through machines
        count = 0
        for guestname in ipdata:
            # Ping the current machine
            PingGuest(guestname)
            count += 1
        return count

def CheckStatus(numofguests):
    """scan the output files created by guestping.py to see if there were any problems and give the user information"""
    import glob
    import time
    # Determine if all the output files have been created
    filelist = glob.glob("./pingstatus/*.out")
    while len(filelist) < numofguests:
        time.sleep(1)
        filelist = glob.glob("./pingstatus/*.out")

    # All files are created so figure out if any of them contain errors
    for filename in filelist:
        # Get current filename
        curfile = filename

        if os.system("cat {0} | grep 'successfully pinged all' > /dev/null 2>&1".format(curfile)) == 0:
            print('File: "{0}" reports that all guests were successfully pinged.'.format(curfile))
        else:
            print('*** ERROR *** File: "{0}" reported errors while pinging one or more guests.'.format(curfile))

if __name__ == "__main__":
    GuestCount = PingEachGuest()
    CheckStatus(GuestCount)
