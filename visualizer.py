"""This application will generate an image representing the weather system"""
from PIL import Image, ImageDraw
import json
from requests import get
import gzip

# todo make an output image for windspeed and humidity and find way to make them accessible to the webservice
# todo data service still doesn't send compressed data, only receives compressed data

_TRANSPARENCY = 200
_MAP_SIZE = 50 * 100

def temperature_to_colour(temp):
    transparency = _TRANSPARENCY
    if temp <= -20:
        return 0, 0, 255, transparency #dark blue
    elif -20 < temp <= -10:
        return 0, 128, 255, transparency # blue
    elif -10 < temp <= 0:
        return 0, 255, 255, transparency #cyan
    elif 0 < temp <= 10:
        return 0, 255, 128, transparency # light green
    elif 10 < temp <= 20:
        return 0, 255, 0, transparency # green
    elif 20 < temp <= 30:
        return 128, 255, 0, transparency # green yellow
    elif 30 < temp <= 40:
        return 255, 255, 0, transparency # yellow
    elif 40 < temp <= 50:
        return 255, 0, 0, transparency # red
    else:
        return 255, 255, 255, transparency


def nav_to_pixels(long, lat, size):
    long = long * 100
    lat = lat * 100
    return (long - size, lat - size, long + size, lat + size)


def generate_map_data(json_file):
    """Generate map data from a json file"""
    data = json.loads(json_file)
    return data["area"]


def generate_temperature_map(map_data):
    """This function will generate a map based on a temperature data"""
    img = Image.new("RGB",
                    (_MAP_SIZE, _MAP_SIZE),
                    color="white")
    drawer = ImageDraw.Draw(img, "RGBA")

    for region in map_data:
        draw_surface = nav_to_pixels(region["longitude"], region["latitude"], region["size"])
        color = temperature_to_colour(region["temperature"])
        drawer.ellipse(draw_surface, color)

    return img


if __name__ == "__main__":
    data = ""
    # with open("data/map.data", "r") as f:
    #     line = f.readline()
    #     while line:
    #         data = data + line
    #         line = f.readline()

    resp = get("http://127.0.0.1:8100/get_regions")
    data = resp.text
    print(data)

    data = json.loads(data)

    visual = generate_temperature_map(data)
    visual.show()
    visual.save("data/map.png", "PNG")
