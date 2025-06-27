import requests
import urllib.parse

def url_generator(lat, lng):
       params = {
              'lat': lat,
              'lng': lng,
              'rad': 4,
              'sort': 'dist',
              'type': 'all',
              'apikey': '648907a9-76c6-87c0-fad9-a7943a072a58'
       }
       query = urllib.parse.urlencode(params)
       return f'https://creativecommons.tankerkoenig.de/json/list.php?{query}'

location_url = 'https://ipinfo.io/json'

def get_location():
    location_response = requests.get(location_url)
    data = location_response.json()
    loc = data['loc']
    lat, lng = loc.split(',')
    return lat, lng

def get_gas_stations():
    lat, lng = get_location()
    gas_station_url = url_generator(lat, lng)
    print(gas_station_url)
    response = requests.get(gas_station_url)
    data = response.json()
    return data['stations']

if __name__ == '__main__':
       stations = get_gas_stations()
       print(stations)