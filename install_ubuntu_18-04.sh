#!/bin/sh

# 1. Python 3.7 is required and can be installed using (via https://linuxize.com/post/how-to-install-python-3-7-on-ubuntu-18-04/):

sudo apt update
sudo apt install software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt install python3.7

# and pip for Python 3.7 can be installed using:

sudo add-apt-repository universe
sudo apt-get update
sudo apt install python3-pip

# 2. Other required system packages can be installed using:

sudo apt-get install libpq-dev libpython3.7-dev rabbitmq-server python-celery-common

# 3. Copernicus Proxy requirements must also be installed. It can be done by the following commands executed in copernicus_proxy/ (where the requirements.txt is located):

python3.7 -m pip install -r requirements.txt
pip3 install -r requirements.txt

# double installation is required due to module visibility reasons.

# To authorize connection with the Climate Data Store, CDS API Key must be added in $HOME/.cdsapirc (via https://cds.climate.copernicus.eu/api-how-to). At this moment only the Key is missing, since CDS API Client is already installed alongside other requirements in (3).