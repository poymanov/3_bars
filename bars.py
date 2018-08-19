import json
import sys
from math import sin, cos, sqrt, atan2, radians


def get_distance(lon1, lat1, lon2, lat2):
    radius = 6373.0

    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = radius * c

    return distance


def print_bar_data(bar):
    print(bar['Name'])
    print(bar['AdmArea'])
    print(bar['District'])
    print(bar['Address'])
    print(bar['PublicPhone'][0]['PublicPhone'])
    print(bar['SeatsCount'])


def compare_data(compare_value_1, compare_value_2, compare_type):
    if compare_type == '<' and compare_value_1 < compare_value_2:
        return True
    elif compare_type == '>' and compare_value_1 > compare_value_2:
        return True

    return False


def iter_bars_data(bars_data, compare_type):
    seats_count = bars_data[0]['attributes']['SeatsCount']
    bar_data = []

    for bar in bars_data:
        bar_seats_count = bar['attributes']['SeatsCount']
        if compare_data(bar_seats_count, seats_count, compare_type):
            seats_count = bar_seats_count
            bar_data = bar['attributes']

    return bar_data


def load_data(filepath):
    bars_data = []

    with open(filepath) as file:
        content = file.read()

    json_data = json.loads(content)
    for bar in json_data['features']:
        bar_data = {
            'coordinates': bar['geometry']['coordinates'],
            'attributes': bar['properties']['Attributes']
        }
        bars_data.append(bar_data)

    return bars_data


def get_biggest_bar(bars_data):
    return iter_bars_data(bars_data, '>')


def get_smallest_bar(bars_data):
    return iter_bars_data(bars_data, '<')


def get_closest_bar(bars_data, longitude, latitude):
    closest_destination = None
    closest_bar_data = []

    for bar in bars_data:
        distance_value = get_distance(
            longitude, latitude,
            bar['coordinates'][1], bar['coordinates'][0])

        if closest_destination is None or \
           compare_data(distance_value, closest_destination, '<'):
            closest_destination = distance_value
            closest_bar_data = bar['attributes']

    return closest_bar_data


if __name__ == '__main__':
    filepath = 'bars.json'
    bars_data = load_data(filepath)

    argv = sys.argv

    if 'min' in argv:
        result = get_smallest_bar(bars_data)
        print('Bar with a minimum number of seats is:')
    elif 'max' in argv:
        result = get_biggest_bar(bars_data)
        print('Bar with a maximum number of seats is:')
    else:
        longitude = float(input('Enter your longitude: '))
        latitude = float(input('Enter your latitude: '))

        result = get_closest_bar(bars_data, longitude, latitude)
        print('The closest bar is:')

    print_bar_data(result)
