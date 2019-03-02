#!/bin/sh

# sane shell environment
set -o pipefail -o noclobber -o errexit -o nounset -o xtrace
cd $(dirname $0)

sudo apt-get -y update
sudo apt-get -y install python3-pip i2c-tools
pip3 install --user opencv-python ipython RPi.GPIO
