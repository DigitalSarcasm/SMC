"""This app generates a a large region of weather data and sends the data to our data microservice"""
from enum import Enum
from random import randint, random
from model.database import Region
from json import dumps
import requests
import gzip

_NUMBER_OF_POINTS = 225
_SIZE_LIMIT_MIN = 50
_SIZE_LIMIT_MAX = 400


class GeneratorMode(Enum):
    ordered = 0
    random = 1
    mild = 2
    rough = 3


def generate_random_region(y, x):
    return Region(coord_long=y, coord_lat=x,
                  temperature=randint(-30, 50),
                  wind_speed=randint(0, 100),
                  humidity=randint(0, 100),
                  size=randint(_SIZE_LIMIT_MIN, _SIZE_LIMIT_MAX))


def generate_area(long_max, lat_max, mode=GeneratorMode.ordered):
    data = None
    if mode == GeneratorMode.ordered:
        data = generate_ordered(long_max, lat_max)
    elif mode == GeneratorMode.random:
        data = generate_random(long_max, lat_max)

    return data


def generate_random(long_max, lat_max):
    data = dict()
    meta = {"size_long": long_max, "size_lat": lat_max}
    data["metadata"] = meta
    area = list()

    unique_long = dict()

    for i in range(_NUMBER_OF_POINTS):
        unique = False
        # Keep trying to find unique cartesian points to avoid regions being on the same longitude and latitude
        while not unique:
            y = randint(0, long_max)
            x = randint(0, lat_max)
            # print(f"trying: {y} {x}")
            if y not in unique_long:
                unique_long[y] = dict()
                unique_long[y][x] = True
                unique = True
            else:
                if x not in unique_long[y]:
                    unique_long[y][x] = True
                    unique = True
                else:
                    continue

        sub_list = list()
        region = generate_random_region(y, x)
        sub_list.append(region.dict())
        area.append(sub_list)

    data["area"] = area
    return data


def generate_ordered(long_max, lat_max):
    data = dict()
    meta = {"size_long": long_max, "size_lat": lat_max}
    data["metadata"] = meta
    area = list()
    for x in range(long_max):
        cur_line = list()

        for y in range(lat_max):
            region = generate_random_region(y, x)
            cur_line.append(region.dict())

        area.append(cur_line)

    data["area"] = area
    return data


if __name__ == "__main__":
    # Generate map data with randomized method
    map_data = dumps(generate_area(50, 50, GeneratorMode.random))
    # Compress the data before saving and sending it out
    comp_data = gzip.compress(bytes(map_data, "utf-8"))

    print(f"Original size: {len(map_data)}.\tNew size {len(comp_data)}")

    # Write to file
    with open("data/map.data", "w") as f:
        f.write(str(comp_data))

    # Then send to data service
    try:
        resp = requests.post("http://127.0.0.1:8100/import_regions", data=comp_data)
        # Print Response from service
        print(resp.text)
    except requests.exceptions.ConnectionError:
        print(f"Failure: Connection error to data service")


