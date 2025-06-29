import requests
import urllib.parse

location_url = 'https://ipinfo.io/json'

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

def get_location(address):
    url = 'https://eu1.locationiq.com/v1/search.php'
    # encoded_address = urllib.parse.quote("Im Äuelchen 33, 53177 Bonn Germany")
    params = {
        'key': 'pk.3764a797567082a54713125597bc0271',
        'q': address,
        'format': 'json'
    }

    print(params)
    response = requests.get(url, params=params)
    data = response.json()
    print(data)
    first_item = next((item for item in data if 'lat' in item and 'lon' in item), None)
    if first_item:
        return first_item['lat'], first_item['lon']
    else:
        return None

def get_gas_stations(address):
    lat, lng = get_location(address)
    gas_station_url = url_generator(lat, lng)
    print(gas_station_url)
    response = requests.get(gas_station_url)
    data = response.json()
    return data['stations']

if __name__ == '__main__':
    print(get_gas_stations('wrong'))