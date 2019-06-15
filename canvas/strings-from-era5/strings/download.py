#!/usr/bin/env python
import cdsapi

c = cdsapi.Client()

c.retrieve(
    'reanalysis-era5-single-levels',
    {
        'product_type':'reanalysis',
        'format':'grib',
        'variable':'sea_surface_temperature',
        'year':[
            '1999','2010'
        ],
        'month':'08',
        'day':'27',
        'time':'20:00'
    },
    'download.grib')