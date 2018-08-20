import json
import sys
from math import sin, cos, sqrt, atan2, radians


def get_distance(lon1, lat1, lon2, lat2):
    earth_radius = 6373.0

    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return earth_radius * c


def print_bar_data(bar):
    bar_attributes = bar['properties']['Attributes']
    print(bar_attributes['Name'])
    print(bar_attributes['AdmArea'])
    print(bar_attributes['District'])
    print(bar_attributes['Address'])
    print(bar_attributes['PublicPhone'][0]['PublicPhone'])
    print(bar_attributes['SeatsCount'])


def load_data(filepath):
    with open(filepath) as file:
        content = file.read()

    return json.loads(content)


def get_biggest_bar(bars_data):
    return max(bars_data['features'],
               key=(lambda k: k['properties']['Attributes']['SeatsCount']))


def get_smallest_bar(bars_data):
    return min(bars_data['features'],
               key=(lambda k: k['properties']['Attributes']['SeatsCount']))


def get_closest_bar(bars_data, longitude, latitude):
    return min(bars_data['features'],
               key=(lambda k:
                    get_distance(
                        longitude, latitude, k['geometry']['coordinates'][1],
                        k['geometry']['coordinates'][0])))


if __name__ == '__main__':
    argv = sys.argv

    if not any('.json' in arg for arg in argv):
        sys.exit('You did not specify the path to the data file')

    filepath = 'bars.json'
    file_data = load_data(filepath)

    if 'min' in argv:
        bar = get_smallest_bar(file_data)
        bar_description = 'Bar with a minimum number of seats is:'
    elif 'max' in argv:
        bar = get_biggest_bar(file_data)
        bar_description = 'Bar with a maximum number of seats is:'
    else:
        try:
            longitude = float(input('Enter your longitude: '))
            latitude = float(input('Enter your latitude: '))

            bar = get_closest_bar(file_data, longitude, latitude)
            bar_description = 'The closest bar is:'
        except ValueError:
            sys.exit('You have entered incorrect coordinates')

    print(bar_description, '\n')
    print_bar_data(bar)
