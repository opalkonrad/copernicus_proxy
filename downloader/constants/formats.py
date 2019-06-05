class Format:
    def __init__(self, name, extension):
        self.name = name
        self.extension = tuple((extension[0], extension[1]))


list_sea_level = [
    Format('.zip file', ('.zip', 'zip')),
    Format('compressed .tar file', ('.tar.gz', 'tgz')),
    Format('GRIB', ('.grib', 'grib')),
    Format('NetCDF (experimental)', ('.nc', 'netcdf'))
]

list_era5 = [
    Format('GRIB', ('.grib', 'grib')),
    Format('NetCDF (experimental)', ('.nc', 'nc'))
]
