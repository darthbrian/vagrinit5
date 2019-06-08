#!/usr/bin/env bash

echo "Installing Python and setting it up..."
isUbuntu=`uname -a | grep -ic 'ubuntu'`
isDebian=`uname -a | grep -ic 'debian'`
if [[ $isUbuntu -gt 0 || $isDebian -gt 0 ]];
then
    echo "Detected Ubuntu or Debian Installation. Using apt-get to install Python..."
    if ! [ -x "$(command -v python)" ];
    then
        sudo apt-get update >/dev/null 2>&1
        echo "Installing Python2 for custom mod support"
        sudo apt-get install -y python >/dev/null 2>&1
        echo "Installing python-apt and setting it up..."
        sudo apt-get install -y python-apt >/dev/null 2>&1
        echo "Installing Pip and setting it up..."
        sudo apt-get install -y python3-pip >/dev/null 2>&1
        echo "Installing the Python3 module Pexpect and setting it up..."
        sudo pip3 install pexpect >/dev/null 2>&1
    else
        echo "Detected python is already installed. Skipping installation..."
    fi

else
    echo "Detected Centos or Red Hat Installation. Using yum to install Python..."
    if ! [ -x "$(command -v python3.6)" ];
    then
        echo "Need to install python..."
        echo "Updating distribution and utils..."
        sudo yum -y update >/dev/null 2>&1
        sudo yum -y install yum-utils >/dev/null 2>&1
        sudo yum -y groupinstall development >/dev/null 2>&1
        sudo yum -y install https://centos7.iuscommunity.org/ius-release.rpm >/dev/null 2<&1
        echo "Installing Python 3 and setting it up..."
        sudo yum -y install python36u >/dev/null 2>&1
        echo "Installing Pip and setting it up..."
        sudo yum -y install python36u-pip >/dev/null 2>&1
        echo "Installing the Python3 module Pexpect and setting it up..."
        sudo pip3.6 install pexpect >/dev/null 2>&1
        sudo yum -y install python36u-devel >/dev/null 2>&1
    else
        echo "Detected python is already installed. Skipping installation..."
    fi
fi

