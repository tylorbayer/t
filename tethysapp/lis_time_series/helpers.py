# Use the LIS time-series API to get data
import requests
def get_lis_time_series(lat, lon, var):
    url = 'http://tethys.byu.edu/apps/lis-viewer/api/GetPointValues/?latitude=' + lat + '&longitude=' + lon + '&variable='+ var
    res = requests.get(url).content
    return res
