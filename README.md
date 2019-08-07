# Copernicus Data Proxy

RESTful API for download management of data from Copernicus Climate Data Store: https://cds.climate.copernicus.eu/

Swagger documentation: https://app.swaggerhub.com/apis-docs/wfabjanczuk/copernicus_proxy/1.0.0

Mock interface for testing purposes is available at URL `canvas/copernicus/`. Enable it by:
- uncommenting `path('canvas/', include('canvas.urls')),` in `copernicus_proxy/urls.py`,
- entering command `python3.7 manage.py collectstatic` in the project root folder.

Online demo (debug mode, no downloading and 20 maximum tasks) can be seen here: https://intense-island-59212.herokuapp.com/canvas/copernicus/

## Installation process (Ubuntu 18.04 and Python 3.7)

Full installation script and instructions are available in file `install_ubuntu_18-04.sh` in the project root folder.

## Usage

At first do not forget to initialize Django database in the project root folder (where the `manage.py` is located):

```
python3.7 manage.py migrate
```

To start or restart workers and reload task queue use the following commands (unfinished tasks will be restarted):

```
python3.7 manage.py restartworkers <number_of_workers>
```

where **<number_of_workers>** is an integer from 1 to 30 specifying how many background processes will be created to handle download requests to Copernicus Climate Data Store.

To start the Copernicus Data Proxy API itself, use standard Django runserver command:

```
python3.7 manage.py runserver
```
