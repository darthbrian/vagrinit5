# This module generates a vagrant init file based on arguments passed in to the module.
# This version utilitizes Classes and Object Orientation instead of traditional function structures.

import json
import sys

def WriteIPFile(hostdict):
    """This function creates a file so the vagrping script can access the IP information"""
    with open('iphost.json', 'w') as ipfile:
        pingdict = {}
        for hostname,hostip in hostdict.items():
            iplist = []
            for curhost,curip in hostdict.items():
                if curip != hostip:
                    iplist.append(str(curip))
                if hostname == curhost:
                    pingdict[hostname] = iplist
        json.dump(pingdict, ipfile, sort_keys=False, indent=4)

def WriteEtcShell(hostdict):
    """This function writes out a shell script to run as a provisioner for modifying /etc/hosts"""
    with open('cathosts.sh', 'w') as hostsfile:
        hostsfile.write('#!/usr/bin/env bash\n')
        for hostname,hostip in hostdict.items():
            hostsfile.write("sed -i \'3i{0} {1}\' /etc/hosts\n".format(hostip, hostname))

def WriteAnsibleInv(hostdict):
    """This function writes out an Ansible inventory file in the playbooks directory for the Admin node to use"""
    with open('playbooks/hosts', 'w') as hostsfile:
        for hostname, hostip in hostdict.items():
            if hostname != 'Admin':
                hostsfile.write("{0}\n".format(hostip))

def BuildIPList(ipfilename):
    """open the JSON file with the IP information so we can pass it back for Vagrantfile creation"""
    with open(ipfilename, 'r') as vagripfile:
        ipdict = {} 
        ip_data = json.load(vagripfile)
        subnet = ip_data["subnet"]
        for box in ip_data["boxes"]:
            ipname = str(box["name"])
            ip = subnet + str(box["ip"])
            ipdict[ipname] = ip

    # write ip dictionary to a new .json file for the auto-ping script to access
    WriteIPFile(ipdict)

    # write contents of ip dictionary to a provisioner shell script to modify /etc/hosts
    WriteEtcShell(ipdict)

    # write contents of ip dictionary to a inventory file for the ansible provisioner to use
    WriteAnsibleInv(ipdict)

class VagrantClass(object):
    """Create a Vagrantinit file based on a .json input file"""

    def __init__(self, filename):
        self.json_input_file = filename

    def VagrantCreate(self):
        # Before we build the Vagrantfile, we need to create files for external processes
        BuildIPList(self.json_input_file)

        # Build the Vagrantfile
        with open("Vagrantfile", 'w') as f:
            f.write('# -*- mode: ruby -*-\n')
            f.write('# vi: set ft=ruby :\n')
            f.write('\n')
            f.write('Vagrant::DEFAULT_SERVER_URL.replace(\'https://vagrantcloud.com\')\n\n')
            f.write('Vagrant.configure("2") do |config|\n\n')

            with open(self.json_input_file, 'r') as vagrinfofile:
                info_data = json.load(vagrinfofile)
                subnet = info_data["subnet"]
                for box in info_data["boxes"]:
                    vmname = box["name"]
                    prefix = str.lower(vmname) + '.vm.'
                    machtype = box["machtype"]
                    ram = box["ram"]
                    ip = subnet + str(box["ip"])
                    f.write('config.vm.define "' + vmname + '" do |' + str.lower(vmname) + '|\n')
                    f.write('      ' + prefix + 'box = "' + machtype + '"\n')
                    f.write('      ' + prefix + 'network "private_network" , ip: "' + ip + '"\n') 
                    f.write('      ' + prefix + 'hostname = "' + str.lower(vmname) + '"\n')
                    f.write('      ' + prefix + 'provision "shell", path: "cathosts.sh"\n')
                    #f.write('      ' + prefix + 'provision "shell", path: "pyinstall.sh"\n')
                    f.write('      ' + prefix + 'provision "shell", path: "sshrestart.sh"\n')
                    if vmname == 'Admin':
                        f.write('      ' + prefix + 'provision "shell", path: "ansinstall.sh"\n')
                    if machtype == 'centpy64':
                        f.write('      ' + prefix + 'synced_folder ".", "/vagrant", type: "rsync", rsync__exclude: [".git/", "ansible/"]\n')
                    f.write('      ' + prefix + 'provider "virtualbox" do |vram|\n')
                    f.write('          vram.memory = "' + str(ram) + '"\n')
                    f.write('      end\n');
                    f.write('end\n');
            f.write('end')

