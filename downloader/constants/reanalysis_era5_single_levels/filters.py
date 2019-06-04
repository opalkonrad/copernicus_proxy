from . import partials
from . import all_filters

filter_categories = [
    {
        'name': 'All',
        'filters': all_filters.filters
    },
    {
        'name': 'Popular',
        'filters': partials.popular.filters
    },
    {
        'name': 'Temperature and pressure',
        'filters': partials.temperature_and_pressure.filters
    },
    {
        'name': 'Wind',
        'filters': partials.wind.filters
    },
    {
        'name': 'Mean rates',
        'filters': partials.mean_rates.filters
    },
    {
        'name': 'Radiation and heat',
        'filters': partials.radiation_and_heat.filters
    },
    {
        'name': 'Clouds',
        'filters': partials.clouds.filters
    },
    {
        'name': 'Lakes',
        'filters': partials.lakes.filters
    },
    {
        'name': 'Evaporation and runoff',
        'filters': partials.evaporation_and_runoff.filters
    },
    {
        'name': 'Precipitation and rain',
        'filters': partials.precipitation_and_rain.filters
    },
    {
        'name': 'Snow',
        'filters': partials.snow.filters
    },
    {
        'name': 'Soil',
        'filters': partials.soil.filters
    },
    {
        'name': 'Vertical integrals',
        'filters': partials.vertical_integrals.filters
    },
    {
        'name': 'Vegetation',
        'filters': partials.vegetation.filters
    },
    {
        'name': 'Ocean waves',
        'filters': partials.ocean_waves.filters
    },
    {
        'name': 'Other',
        'filters': partials.other.filters
    }
]
