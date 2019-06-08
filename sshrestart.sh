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

log "Making sure SSH is configured properly and restart it if necessary..."
isUbuntu=`uname -a | grep -ic 'ubuntu'`
isDebian=`uname -a | grep -ic 'debian'`
if [[ $isUbuntu -gt 0 || $isDebian -gt 0 ]];
then
    log "Detected Ubuntu or Debian Installation. Configuring SSH..."
    log "Checking to make sure the PasswordAuthentication flag is set to 'yes' in sshd_config..."
    sudo sed -i -e 's/PasswordAuthentication no/PasswordAuthentication yes/g' /etc/ssh/sshd_config
    log "Restarting ssh service..."
    sudo service ssh restart
else
    log "Detected CentOS or Red Hat Installation. Configuring SSH..."
    log "Checking to make sure the PasswordAuthentication flag is set to 'yes' in sshd_config..."
    sudo sed -i -e 's/PasswordAuthentication no/PasswordAuthentication yes/g' /etc/ssh/sshd_config
    log "Restarting ssh service..."
    sudo systemctl restart sshd.service
fi

