import requests
import urllib.parse

# This method generates the URL to retrieve gas stations
# Return the generated string
def url_generator(lat, lng):
       params = {
              'lat': lat,
              'lng': lng,
              'rad': 4,
              'sort': 'dist',
              'type': 'all',
              'apikey': '648907a9-76c6-87c0-fad9-a7943a072a58'
       }
       # Convert two-element tuples in the URL string
       query = urllib.parse.urlencode(params)
       return f'https://creativecommons.tankerkoenig.de/json/list.php?{query}'

# This method retrieves the lat and lng from a given address
# Need to pass the address as an argument
# Return the lat and lng
def get_location(address):
    url = 'https://eu1.locationiq.com/v1/search.php'
    params = {
        'key': 'pk.3764a797567082a54713125597bc0271',
        'q': address,
        'format': 'json'
    }

    try:
        response = requests.get(url, params=params)
        data = response.json()

        if not isinstance(data, list): return None, None
        # Get the lat and lng from the result list
        first_item = next((item for item in data if 'lat' in item and 'lon' in item), None)
        if first_item:
            return first_item['lat'], first_item['lon']
        else:
            return None, None
    except (requests.RequestException, ValueError, TypeError):
        return None, None

# Retrieve gas stations
# Return a list of gas stations
def get_gas_stations(address):
    # Get lat and lng
    lat, lng = get_location(address)

    if lat is None or lng is None:
        return []

    try:
        gas_station_url = url_generator(lat, lng)
        response = requests.get(gas_station_url)
        data = response.json()
        return data['stations']

    except (requests.RequestException, ValueError, TypeError):
        return []

if __name__ == '__main__':
    print(get_gas_stations('53177'))