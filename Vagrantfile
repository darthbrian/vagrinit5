# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant::DEFAULT_SERVER_URL.replace('https://vagrantcloud.com')

Vagrant.configure("2") do |config|

config.vm.define "fred" do |fred|
      fred.vm.box = "xenpy64"
      fred.vm.network "private_network" , ip: "10.0.0.11"
      fred.vm.hostname = "fred"
      fred.vm.provision "shell", path: "cathosts.sh"
      fred.vm.provision "shell", path: "sshrestart.sh"
      fred.vm.provider "virtualbox" do |vram|
          vram.memory = "1024"
      end
end
config.vm.define "wilma" do |wilma|
      wilma.vm.box = "xenpy64"
      wilma.vm.network "private_network" , ip: "10.0.0.12"
      wilma.vm.hostname = "wilma"
      wilma.vm.provision "shell", path: "cathosts.sh"
      wilma.vm.provision "shell", path: "sshrestart.sh"
      wilma.vm.provider "virtualbox" do |vram|
          vram.memory = "512"
      end
end
config.vm.define "barney" do |barney|
      barney.vm.box = "centpy64"
      barney.vm.network "private_network" , ip: "10.0.0.13"
      barney.vm.hostname = "barney"
      barney.vm.provision "shell", path: "cathosts.sh"
      barney.vm.provision "shell", path: "sshrestart.sh"
      barney.vm.synced_folder ".", "/vagrant", type: "rsync", rsync__exclude: [".git/", "ansible/"]
      barney.vm.provider "virtualbox" do |vram|
          vram.memory = "512"
      end
end
config.vm.define "betty" do |betty|
      betty.vm.box = "centpy64"
      betty.vm.network "private_network" , ip: "10.0.0.14"
      betty.vm.hostname = "betty"
      betty.vm.provision "shell", path: "cathosts.sh"
      betty.vm.provision "shell", path: "sshrestart.sh"
      betty.vm.synced_folder ".", "/vagrant", type: "rsync", rsync__exclude: [".git/", "ansible/"]
      betty.vm.provider "virtualbox" do |vram|
          vram.memory = "512"
      end
end
config.vm.define "Admin" do |admin|
      admin.vm.box = "xenpy64"
      admin.vm.network "private_network" , ip: "10.0.0.10"
      admin.vm.hostname = "admin"
      admin.vm.provision "shell", path: "cathosts.sh"
      admin.vm.provision "shell", path: "sshrestart.sh"
      admin.vm.provision "shell", path: "ansinstall.sh"
      #admin.vm.provision "shell", path: "admininit.sh"
      admin.vm.provider "virtualbox" do |vram|
          vram.memory = "1024"
      end
end
#config.vm.define "pebbles" do |pebbles|
#      pebbles.vm.box = "xenpy64"
#      pebbles.vm.network "private_network" , ip: "10.0.0.15"
#      pebbles.vm.hostname = "pebbles"
#      pebbles.vm.provision "shell", path: "cathosts.sh"
#      pebbles.vm.provision "shell", path: "sshrestart.sh"
#      pebbles.vm.provider "virtualbox" do |vram|
#          vram.memory = "1024"
#      end
#end
#config.vm.define "bammbamm" do |bammbamm|
#      bammbamm.vm.box = "xenpy64"
#      bammbamm.vm.network "private_network" , ip: "10.0.0.16"
#      bammbamm.vm.hostname = "bammbamm"
#      bammbamm.vm.provision "shell", path: "cathosts.sh"
#      bammbamm.vm.provision "shell", path: "sshrestart.sh"
#      bammbamm.vm.provider "virtualbox" do |vram|
#          vram.memory = "512"
#      end
#end
#config.vm.define "dino" do |dino|
#      dino.vm.box = "xenpy64"
#      dino.vm.network "private_network" , ip: "10.0.0.17"
#      dino.vm.hostname = "dino"
#      dino.vm.provision "shell", path: "cathosts.sh"
#      dino.vm.provision "shell", path: "sshrestart.sh"
#      dino.vm.provider "virtualbox" do |vram|
#          vram.memory = "512"
#      end
#end
#config.vm.define "hoppy" do |hoppy|
#      hoppy.vm.box = "xenpy64"
#      hoppy.vm.network "private_network" , ip: "10.0.0.18"
#      hoppy.vm.hostname = "hoppy"
#      hoppy.vm.provision "shell", path: "cathosts.sh"
#      hoppy.vm.provision "shell", path: "sshrestart.sh"
#      hoppy.vm.provider "virtualbox" do |vram|
#          vram.memory = "512"
#      end
#end
#config.vm.define "misterSlate" do |misterslate|
#      misterslate.vm.box = "xenpy64"
#      misterslate.vm.network "private_network" , ip: "10.0.0.19"
#      misterslate.vm.hostname = "misterslate"
#      misterslate.vm.provision "shell", path: "cathosts.sh"
#      misterslate.vm.provision "shell", path: "sshrestart.sh"
#      misterslate.vm.provider "virtualbox" do |vram|
#          vram.memory = "1024"
#      end
#end
#config.vm.define "gazoo" do |gazoo|
#      gazoo.vm.box = "xenpy64"
#      gazoo.vm.network "private_network" , ip: "10.0.0.20"
#      gazoo.vm.hostname = "gazoo"
#      gazoo.vm.provision "shell", path: "cathosts.sh"
#      gazoo.vm.provision "shell", path: "sshrestart.sh"
#      gazoo.vm.provider "virtualbox" do |vram|
#          vram.memory = "512"
#      end
#end
end
