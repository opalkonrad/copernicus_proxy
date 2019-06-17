# Copernicus Data Proxy

RESTful API for download management of data from Copernicus Climate Data Store: https://cds.climate.copernicus.eu/

Swagger documentation: https://app.swaggerhub.com/apis-docs/wfabjanczuk/copernicus_proxy/1.0.0

Mock interface for testing purposes is available at URL `canvas/copernicus/`. Enable it by uncommenting `path('canvas/', include('canvas.urls')),` in `copernicus_proxy/urls.py`. Online demo (debug mode, no downloading and 20 maximum tasks) can be seen here: https://intense-island-59212.herokuapp.com/canvas/copernicus/

## Installation process (Ubuntu 18.04 and Python 3.7)

Full installation script is available in file `install_ubuntu_18-04.sh` in the project root folder.

1. Python 3.7 is required and can be installed using (via https://linuxize.com/post/how-to-install-python-3-7-on-ubuntu-18-04/): 

```
sudo apt update
sudo apt install software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt install python3.7
```

and pip for Python 3.7 can be installed using:

```
sudo add-apt-repository universe
sudo apt-get update
sudo apt install python3-pip
```

2. Other required system packages can be installed using:

```
sudo apt-get install libpq-dev libpython3.7-dev rabbitmq-server python-celery-common
```

3. Copernicus Proxy requirements must also be installed. It can be done by the following commands executed in the project root folder (where the `requirements.txt` is located):

```
python3.7 -m pip install -r requirements.txt
pip3 install -r requirements.txt
```

double installation is required due to module visibility reasons.

4. To authorize connection with the Climate Data Store, CDS API Key must be added in `$HOME/.cdsapirc` (via https://cds.climate.copernicus.eu/api-how-to). At this moment only the Key is missing, since CDS API Client is already installed alongside other requirements in (3).

## Usage

At first do not forget to initialize Django database in the project root folder (where the `manage.py` is located):

```
python3.7 manage.py migrate
```

To restart workers and task queue use the following commands (unfinished tasks will be restarted):

```
python3.7 manage.py restartworkers <number_of_workers>
```

where **<number_of_workers>** is an integer from 1 to 30 specifying how many background processes will be created to handle download requests to Copernicus Climate Data Store.

To start the Copernicus Data Proxy API itself, use standard Django runserver command:

```
python3.7 manage.py runserver
```
