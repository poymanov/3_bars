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


def load_data(filepath):
    bars_data = []
    seats_count_data = []
    coordinates_data = []

    with open(filepath) as file:
        content = file.read()

    json_data = json.loads(content)
    for bar in json_data['features']:
        bars_data.append(bar['properties']['Attributes'])
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

    if 'min' in argv:
        bar_index = get_smallest_bar(file_data['seats_count_data'])
        print('Bar with a minimum number of seats is:')
    elif 'max' in argv:
        bar_index = get_biggest_bar(file_data['seats_count_data'])
        print('Bar with a maximum number of seats is:')
    else:
        longitude = float(input('Enter your longitude: '))
        latitude = float(input('Enter your latitude: '))

        bar_index = get_closest_bar(file_data['coordinates_data'],
                                    longitude, latitude)
        print('The closest bar is:')

    print_bar_data(file_data['bars_data'][bar_index])
