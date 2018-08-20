import json
import sys
from math import sin, cos, sqrt, atan2, radians


def check_coords(latitude, longitude):
    return 49.7 < latitude < 58.5 and -6 < longitude < 2.1


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

    coordinates_distance = earth_radius * c

    return coordinates_distance


def print_bar_data(bar):
    bar_attributes = bar['properties']['Attributes']
    print(bar_attributes['Name'])
    print(bar_attributes['AdmArea'])
    print(bar_attributes['District'])
    print(bar_attributes['Address'])
    print(bar_attributes['PublicPhone'][0]['PublicPhone'])
    print(bar_attributes['SeatsCount'])


def load_data(filepath):
    bars_data = []
    seats_count_data = []
    coordinates_data = []

    with open(filepath) as file:
        content = file.read()

    file_data = json.loads(content)
    for bar in file_data['features']:
        bars_data.append(bar)
        coordinates_data.append(bar['geometry']['coordinates'])
        seats_count_data.append(bar['properties']['Attributes']['SeatsCount'])

    return {
        'bars_data': bars_data,
        'seats_count_data': seats_count_data,
        'coordinates_data': coordinates_data}


def get_biggest_bar(seats_count_data):
    biggest_bar_value = max(seats_count_data)
    return seats_count_data.index(biggest_bar_value)


def get_smallest_bar(seats_count_data):
    smallest_bar_value = min(seats_count_data)
    return seats_count_data.index(smallest_bar_value)


def get_closest_bar(coordinates_data, longitude, latitude):
    distances_data = []

    for coordinates in coordinates_data:
        distance_value = get_distance(longitude, latitude,
                                      coordinates[1], coordinates[0])
        distances_data.append(distance_value)

    closest_distance_value = min(distances_data)
    return distances_data.index(closest_distance_value)


if __name__ == '__main__':
    filepath = 'bars.json'
    file_data = load_data(filepath)

    argv = sys.argv

    for bar_index in range(len(file_data['bars_data'])):
        print_bar_data(file_data['bars_data'][bar_index])
        print('\n')

    if 'min' in argv:
        bar_index = get_smallest_bar(file_data['seats_count_data'])
        print('Bar with a minimum number of seats is:')
    elif 'max' in argv:
        bar_index = get_biggest_bar(file_data['seats_count_data'])
        print('Bar with a maximum number of seats is:')
    else:
        longitude = input('Enter your longitude: ')
        latitude = input('Enter your latitude: ')

        try:
            longitude = float(longitude)
            latitude = float(latitude)
        except Exception:
            print('You have entered incorrect coordinates')
            exit()

        bar_index = get_closest_bar(file_data['coordinates_data'],
                                    longitude, latitude)
        print('The closest bar is:')

    print_bar_data(file_data['bars_data'][bar_index])
