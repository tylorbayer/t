from django.shortcuts import render, reverse, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import plotly.graph_objs as go
from tethys_sdk.gizmos import MapView, Button, TextInput, DatePicker, SelectInput, DataTableView, MVDraw, MVView, MVLayer, PlotlyView
import json
from .helpers import get_lis_time_series
import datetime as dt

from .model import create_forecast, get_forecast


@login_required()
def home(request):
    """
    Controller for the app home page.
    """
    # Default Values
    lat = ''
    lon = ''
    forecast_type = 'Rainfall'

    # Errors
    location_error = ''
    lat_error = ''
    lon_error = ''

    # Handle form submission
    if request.POST and 'add-button' in request.POST:
        # Get values
        has_errors = True
        location = request.POST.get('geometry', None)
        forecast_type = request.POST.get('forecast_type', None)
        lat = request.POST.get('lat', None)
        lon = request.POST.get('lon', None)

        # Validate
        if location and (not lat and not lon):
            location_dict = json.loads(location)
            lat = str(location_dict['geometries'][0]['coordinates'][1])
            lon = str(location_dict['geometries'][0]['coordinates'][0])

        if lat and lon:
            has_errors = False

        if not has_errors:
            create_forecast(forecast_type=forecast_type, lat=lat, lon=lon)
            return redirect(reverse('lis_time_series:forecast'))

        location_error = 'Location (or Lat, Lon) is required.'
        lat_error = ' '
        lon_error = ' '
        messages.error(request, "Please fix errors.")

    # Define form gizmos
    initial_view = MVView(
        projection='EPSG:4326',
        center=[85.3, 27.7],
        zoom=3.5
    )

    drawing_options = MVDraw(
        controls=['Modify', 'Delete', 'Move', 'Point'],
        initial='Point',
        output_format='GeoJSON',
        point_color='#FF0000'
    )

    location_input = MapView(
        height='300px',
        width='100%',
        basemap='OpenStreetMap',
        draw=drawing_options,
        view=initial_view
    )

    add_button = Button(
        display_text='Add',
        name='add-button',
        icon='glyphicon glyphicon-plus',
        style='success',
        attributes={'form': 'create-forecast-form'},
        submit=True
    )

    cancel_button = Button(
        display_text='Cancel',
        name='cancel-button',
        href=reverse('dam_inventory:home')
    )

    lat_input = TextInput(
        display_text='Lat',
        name='lat',
        placeholder='e.g.: 27.7',
        initial=lat,
        error=lat_error
    )

    lon_input = TextInput(
        display_text='Lon',
        name='lon',
        placeholder='e.g.: 85.3',
        initial=lon,
        error=lon_error
    )

    forecast_type_input = SelectInput(
        display_text='Forcast Type',
        name='forecast_type',
        multiple=False,
        options=[('Rainfall', 'rainfall'), ('Snowfall', 'snowfall'), ('Total Precipitation', 'total_precip'),
                 ('Evaporation', 'evap'), ('Surface Runoff', 'Qs'), ('Subsurface Runoff', 'Qsb'),
                 ('SWE', 'SWE'), ('Snow Depth', 'SnowDepth'), ('Soil Moisture', 'SoilMoist'),
                 ('Snow Cover', 'Snow Cover')],
        initial=forecast_type,
    )

    context = {
        'location_input': location_input,
        'location_error': location_error,
        'lat_input': lat_input,
        'lon_input': lon_input,
        'forecast_type_input': forecast_type_input,
        'add_button': add_button,
        'cancel_button': cancel_button
    }

    return render(request, 'lis_time_series/home.html', context)

@login_required()
def forecast(request):
    """
    Show all dams in a table view.
    """
    forecasts = get_forecast()

    for forecast in forecasts:
        forecast_type = forecast['forecast_type']
        lat = forecast['lat']
        lon = forecast['lon']

    x = []
    y = []

    json_string = get_lis_time_series(lat, lon, forecast_type)
    json_obj = json.loads(json_string)
    values = json_obj['values']

    for i in values:
        x.append(dt.datetime.utcfromtimestamp(i[0] / 1000))
        y.append(i[1])

    data = [go.Scatter(x=x, y=y)]
    layout = go.Layout(
        title=forecast_type.upper()
    )
    figure = go.Figure(data=data, layout=layout)
    lis_time_series_plot = PlotlyView(figure)

    context = {
        'lis_time_series_plot': lis_time_series_plot
    }

    return render(request, 'lis_time_series/forecast.html', context)