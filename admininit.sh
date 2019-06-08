#!/usr/bin/env bash

readonly SCRIPT_NAME=${0##*/}

log() {
  echo "$@"
  logger -p user.notice -t $SCRIPT_NAME "$@"
}

err() {
  echo "$@" >&2
  logger -p user.error -t $SCRIPT_NAME "$@"
}

log "Setting up Passwordless SSH between Admin and Target Nodes"
sudo /vagrant/SSHKeyGen.py -f /home/vagrant/.ssh/id_rsa
#sudo /vagrant/SSHKeyGen.py -f /home/vagrant/.ssh/id_rsa
#sudo /vagrant/SSHKeyGen.py >/dev/null 2>&1

log "waiting 15 seconds to make sure the key get generated..."
sleep 15

#log "Copy SSH Key to target machines..."
#sudo /vagrant/SSHKeyCopy.py >/dev/null 2>&1

#/vagrant/SSHKeyCopy.py
#echo "Installing Ansible on Admin node and setting it up..."
#sudo apt-get install ansible -y
#sudo apt install ansible >/dev/null 2>&1
