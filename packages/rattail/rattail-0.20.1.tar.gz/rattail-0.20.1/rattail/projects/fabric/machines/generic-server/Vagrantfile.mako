# -*- mode: ruby; -*-

Vagrant.configure("2") do |config|

  # live machine runs Debian 10 Buster
  config.vm.box = "debian/buster64"

  # # live machine runs Ubuntu 20.04 Focal Fossa
  # config.vm.box = "ubuntu/focal64"

  # # this may be necessary for big data import tasks.  you can raise or lower
  # # it, or comment out if you find that you don't need it
  # config.vm.provider "virtualbox" do |v|
  #   v.memory = 4096
  # end

  # # ${name} web app
  # config.vm.network "forwarded_port", guest: 9761, host: 9761

  # # apache
  # config.vm.network "forwarded_port", guest: 80, host: 8080
  # config.vm.network "forwarded_port", guest: 443, host: 8443

end
