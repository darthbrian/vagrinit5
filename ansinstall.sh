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

log "Installing Ansible and setting it up..."
isUbuntu=`uname -a | grep -ic 'ubuntu'`
isDebian=`uname -a | grep -ic 'debian'`
if [[ $isUbuntu -gt 0 || $isDebian -gt 0 ]];
then
    log "Detected Ubuntu or Debian Installation. Using apt-get..."
    if ! [ -x "$(command -v ansible)" ];
    then
        # Step 1. Stop apt-daily.timer
        log "Kill apt-daily.service so it doesn't interfere with our installation"
        systemctl stop apt-daily.timer
        systemctl disable apt-daily.timer
        systemctl kill --kill-who=all apt-daily.timer
        log "wait until apt-daily.timer has been killed "
        while ! (systemctl list-units --all apt-daily.timer | fgrep -q dead)
        do
            log "sleeping for 1 second"
            sleep 1;
        done

        # Step 2. Stop apt-daily.service
        systemctl stop apt-daily.service
        systemctl disable apt-daily.service
        systemctl kill --kill-who=all apt-daily.service
        log "wait until apt-daily.service has been killed "
        while ! (systemctl list-units --all apt-daily.service | fgrep -q dead)
        do
            log "sleeping for 1 second"
            sleep 1;
        done

        # Step 3. Stop apt-daily-upgrade.timer
        systemctl stop apt-daily-upgrade.timer
        systemctl disable apt-daily-upgrade.timer
        systemctl kill --kill-who=all apt-daily-upgrade.timer

        # Step 4. Stop apt-daily-upgrade.service
        systemctl stop apt-daily-upgrade.service
        systemctl disable apt-daily-upgrade.service
        systemctl kill --kill-who=all apt-daily-upgrade.service

        log "Beginning update and install"
        #sudo apt-get update
        sudo apt-get update >/dev/null 2>&1
        #sudo apt-get install -y ansible
        sudo apt-get install -y ansible >/dev/null 2>&1
    else
        log "Detected ansible is already installed. Skipping installation..."
    fi
else
    log "Detected CentOS or Red Hat Installation. Using yum..."
    if ! [ -x "$(command -v ansible)" ];
    then
        sudo yum install -y ansible >/dev/null 2>&1
    else
        log "Detected Ansible is already installed. Skipping installation..."
    fi
fi
