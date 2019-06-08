#!/usr/bin/env python3
# Get Port Information and Save It So We Can Use it When We Set Up Passworldless SSH on Admin 
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

def GetPortInfo():
    """loop through our list of machines and for each one get port information"""

    #open json file with IP data
    with open('iphost.json', 'r') as ipfile, \
            open('portinfo.json', 'w') as portfile:
        #get dictionary data
        ipdata = json.load(ipfile)

        #loop through machines
        portlist = [] 
        for guestname in ipdata:
            # Write port out to our temp file as long as it's not for the Admin node
            if guestname != 'Admin':
                port = GetPortNum(guestname)
                portlist.append(port)
        json.dump(portlist, portfile, sort_keys=False, indent=4)

if __name__ == "__main__":
    GetPortInfo()
