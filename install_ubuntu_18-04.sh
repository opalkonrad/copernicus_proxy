#!/bin/sh

sudo apt update
sudo apt install software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt install python3.7

sudo add-apt-repository universe
sudo apt-get update
sudo apt install python3-pip

sudo apt-get install libpq-dev libpython3.7-dev rabbitmq-server python-celery-common

python3.7 -m pip install -r requirements.txt
pip3 install -r requirements.txt
