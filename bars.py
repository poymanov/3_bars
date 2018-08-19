import json
import sys
from math import sin, cos, sqrt, atan2, radians

def get_distance(lon1, lat1, lon2, lat2):
    r = 6373.0

    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = r * c

    return distance

def print_bar_data(data):
    print(result['Name'])
    print(result['AdmArea'])
    print(result['District'])
    print(result['Address'])
    print(result['PublicPhone'][0]['PublicPhone'])
    print(result['SeatsCount'])

def compare_data(data1, data2, type):
    if type == '<' and data1 < data2:
        return True
    elif type == '>' and data1 > data2:
        return True

    return False

def iter_bars_data(data, compare_type):
    seats_count = data[0]['attributes']['SeatsCount']
    bar_data = []

    for item in data:
        item_seats_count = item['attributes']['SeatsCount']
        if compare_data(item_seats_count, seats_count, compare_type):
            seats_count = item_seats_count
            bar_data = item['attributes']

    return bar_data

def load_data(filepath):
    data = []

    with open(filepath) as file:
        content = file.read()

    json_data = json.loads(content)
    for bar in json_data['features']:
        new_data_item = {
            'coordinates': bar['geometry']['coordinates'],
            'attributes': bar['properties']['Attributes']
        }
        data.append(new_data_item)

    return data


def get_biggest_bar(data):
    return iter_bars_data(data, '>')

def get_smallest_bar(data):
    return iter_bars_data(data, '<')

def get_closest_bar(data, longitude, latitude):
    closest_destination = None
    closest_bar_data = []

    for item in data:
        distance_value = get_distance(longitude, latitude, item['coordinates'][1], item['coordinates'][0])

        if closest_destination is None or \
            compare_data(distance_value, closest_destination, '<'):
            closest_destination = distance_value
            closest_bar_data = item['attributes']

    return closest_bar_data

if __name__ == '__main__':
    filepath = 'bars.json'
    data = load_data(filepath)

    argv = sys.argv

    if 'min' in argv:
        result = get_smallest_bar(data)
        print('Bar with a minimum number of seats is:')
    elif 'max' in argv:
        result = get_biggest_bar(data)
        print('Bar with a maximum number of seats is:')
    else:
        longitude = float(input('Enter your longitude: '))
        latitude = float(input('Enter your latitude: '))

        result = get_closest_bar(data, longitude, latitude)
        print('The closest bar is:')

    print_bar_data(result)
