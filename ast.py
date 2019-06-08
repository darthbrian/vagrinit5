#!/usr/bin/env python3

#This script is intended to constantly run vagrant up on the Admin node.
#Each time it's spun up it checks to see if everything worked okay.
#If everything is fine, vagrant destroy and then vagrant up again.
#End if Admin vagrant up fails and save of the error log.


def RunStressTest():
    import subprocess

    #call exec or something to run 'vagrant up --debug > testbed.log
    #1. need a method or script that calls an external command and waits for it to end.

    error = False
    loop = 0
    while (not error) and (loop < 20):
        with open("testbed{0}.log".format(str(loop)), "wb", 0) as outfile:
            cmd = ["/usr/bin/vagrant up Admin --debug"]
            try:
                p = subprocess.run(cmd, stdin = None, stdout = outfile, stderr = outfile, shell = True, check = True)
            except subprocess.CalledProcessError as runexc:
                error = True
                print("ERROR: The 'vagrant up' command failed on attempt #{0}, with error code {1}.".format(str(loop+1), runexc.returncode))
            else:
                error = False
                # Before we continue execution to the next loop, we need to destroy the Admin node we just created.
                rmcmd = ["/usr/bin/vagrant destroy Admin -f"]
                try:
                    p = subprocess.run(rmcmd, stdin = outfile, stdout = outfile, stderr = outfile, shell = True, check = True)
                except subprocess.CalledProcessError as runexc:
                    error = True
                    print("ERROR: The 'vagrant destroy' command failed on attempt #{0}, with error code {1}.".format(str(loop+1), runexc.returncode))
        loop += 1 


#p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
#for line in p.stdout:
#    print line
    #p.wait()
#print p.returncode

#grep testbed.log for a particular error message.

#so

#error = false
#while (not error):
#    vagrant up

#    wait for it to finish

#    grep log for error message

#    if error message found:
#        error = true



#error message to grep for:

#The SSH command responded with a non-zero exit status. Vagrant
#assumes that this means the command failed. The output for this command
#should be in the log above. Please read the output to determine what
#went wrong.


if __name__ == "__main__":
    RunStressTest()
    #import argparse
    #from vagrcreate import VagrantClass
    #parser = argparse.ArgumentParser(description = "Create a Vagrant initialization file based on a JSON input file.")
    #parser.add_argument("filename", help = "The name of the JSON file to be used as input")
    #args = parser.parse_args()
    #args_dict = vars(args)
    #Vagr = VagrantClass(**args_dict)
    #Vagr.VagrantCreate()
