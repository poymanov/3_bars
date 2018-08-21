import json
import sys
import argparse
from math import sin, cos, sqrt, atan2, radians


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('file', help='Path to file with json data')
    parser.add_argument('mode', help='Output data result',
                        choices=['min', 'max', 'closest'])
    return parser.parse_args()


def get_bars_list(bars_data):
    return bars_data['features']


def get_bar_seats_count(bar):
    return bar['properties']['Attributes']['SeatsCount']


def get_bar_coordinates(bar):
    return bar['geometry']['coordinates'][1], bar['geometry']['coordinates'][0]


def get_coordinates():
    try:
        longitude = float(input('Enter your longitude: '))
        latitude = float(input('Enter your latitude: '))
        return longitude, latitude
    except ValueError:
        return None, None


def get_distance(origin, destination):
    earth_radius = 6373.0

    lon1, lat1 = origin
    lon2, lat2 = destination

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
    bars_list = get_bars_list(bars_data)
    bar = max(bars_list, key=(lambda bar: get_bar_seats_count(bar)))
    description = 'Bar with a maximum number of seats is:'
    return bar, description


def get_smallest_bar(bars_data):
    bars_list = get_bars_list(bars_data)
    bar = min(bars_list, key=(lambda bar: get_bar_seats_count(bar)))
    description = 'Bar with a minimum number of seats is:'
    return bar, description


def get_closest_bar(bars_data, longitude, latitude):
    bars_list = get_bars_list(bars_data)

    origin_coordinates = longitude, latitude

    bar = min(bars_list, key=lambda bar:
              get_distance(origin_coordinates, get_bar_coordinates(bar)))
    description = 'The closest bar is:'
    return bar, description


if __name__ == '__main__':
    args = parse_args()

    filepath = args.file
    file_data = load_data(filepath)

    if args.mode == 'min':
        output_data = get_smallest_bar(file_data)
    elif args.mode == 'max':
        output_data = get_biggest_bar(file_data)
    elif args.mode == 'closest':
        longitude, latitude = get_coordinates()

        if None not in (longitude, latitude):
            output_data = get_closest_bar(file_data, longitude, latitude)
        else:
            sys.exit('You have entered incorrect coordinates')

    print(output_data[1], '\n')
    print_bar_data(output_data[0])
