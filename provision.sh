#!/usr/bin/env bash

sudo apt-get install python-pip -y
sudo pip install virtualenv

sudo gem install foreman

sudo echo "export APP_CONFIG_OBJECT=config.DevelopmentConfig" >> /home/vagrant/.bashrc
