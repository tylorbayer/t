import os
import uuid
import json
from .app import LisTimeSeries as app


def create_forecast(forecast_type, lat, lon):
    """
    Persist new dam.
    """
    forecast_dict = {
        'forecast_type': forecast_type,
        'lat': lat,
        'lon': lon,
    }

    forecast_json = json.dumps(forecast_dict)

    # Make forecast dir if it doesn't exist
    app_workspace = app.get_app_workspace()
    forecast_dir = os.path.join(app_workspace.path, 'forecast')
    if not os.path.exists(forecast_dir):
        os.mkdir(forecast_dir)

    # Name of the file is its id
    file_name = 'lis.json'
    file_path = os.path.join(forecast_dir, file_name)

    # Write json
    with open(file_path, 'w') as f:
        f.write(forecast_json)


def get_forecast():
    """
    Get all persisted dams.
    """
    # Write to file in app_workspace/dams/{{uuid}}.json
    # Make dams dir if it doesn't exist
    app_workspace = app.get_app_workspace()
    forecast_dir = os.path.join(app_workspace.path, 'forecast')
    if not os.path.exists(forecast_dir):
        os.mkdir(forecast_dir)

    forecasts = []

    # Open each file and convert contents to python objects
    for forecast_json in os.listdir(forecast_dir):
        # Make sure we are only looking at json files
        if '.json' not in forecast_json:
            continue

        forecast_json_path = os.path.join(forecast_dir, forecast_json)
        with open(forecast_json_path, 'r') as f:
            forecast_dict = json.loads(f.readlines()[0])
            forecasts.append(forecast_dict)

    return forecasts
