from . import partials
# from . import all_filters

filter_categories = [
    # {
    #     'name': 'All',
    #     'codename': 'all',
    #     'filters': all_filters.filters
    # },
    {
        'name': 'Popular',
        'codename': 'popular',
        'filters': partials.popular.filters
    },
    {
        'name': 'Temperature and pressure',
        'codename': 'temperature_and_pressure',
        'filters': partials.temperature_and_pressure.filters
    },
    {
        'name': 'Wind',
        'codename': 'wind',
        'filters': partials.wind.filters
    },
    {
        'name': 'Mean rates',
        'codename': 'mean_rates',
        'filters': partials.mean_rates.filters
    },
    {
        'name': 'Radiation and heat',
        'codename': 'radiation_and_heat',
        'filters': partials.radiation_and_heat.filters
    },
    {
        'name': 'Clouds',
        'codename': 'clouds',
        'filters': partials.clouds.filters
    },
    {
        'name': 'Lakes',
        'codename': 'lakes',
        'filters': partials.lakes.filters
    },
    {
        'name': 'Evaporation and runoff',
        'codename': 'evaporation_and_runoff',
        'filters': partials.evaporation_and_runoff.filters
    },
    {
        'name': 'Precipitation and rain',
        'codename': 'precipitation_and_rain',
        'filters': partials.precipitation_and_rain.filters
    },
    {
        'name': 'Snow',
        'codename': 'snow',
        'filters': partials.snow.filters
    },
    {
        'name': 'Soil',
        'codename': 'soil',
        'filters': partials.soil.filters
    },
    {
        'name': 'Vertical integrals',
        'codename': 'vertical_integrals',
        'filters': partials.vertical_integrals.filters
    },
    {
        'name': 'Vegetation',
        'codename': 'vegetation',
        'filters': partials.vegetation.filters
    },
    {
        'name': 'Ocean waves',
        'codename': 'ocean_waves',
        'filters': partials.ocean_waves.filters
    },
    {
        'name': 'Other',
        'codename': 'other',
        'filters': partials.other.filters
    }
]
