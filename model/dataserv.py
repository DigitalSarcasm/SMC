# This is the main flask micro service that handles data services by other micro services
from flask import Flask, Blueprint, jsonify, request
from model.database import initialize_db, get_all_regions, Region, add_region_obj, delete_all_regions
import json
import gzip

_DATASERV_PORT = 8100

# we will outline all the /api/data procedures here

data_service = Blueprint("data service", __name__)


@data_service.route("/")
def data_serv_home():
    page = ""
    page += "<a href=" + request.url + "get_regions>All regions\n"
    page += "<a href=" + request.url + "clear_regions>clear regions\n"


    return page

@data_service.route("/get_regions")
def get_regions():
    regions = get_all_regions()
    # region_map = {regions[i].id : regions[i].dict() for i in range(len(regions))}
    # make into a list of region dicts
    region_map = [x.dict() for x in regions]
    # print(region_map)
    return jsonify(region_map)


@data_service.route("/add_region", methods=["POST"])
def add_region():
    """add region using post."""
    # All the data should be sent in the post data as json
    pass # todo

@data_service.route("/clear_regions")
def clear_regions():
    delete_all_regions()
    ret = {"code":"success"}
    return jsonify(ret)

@data_service.route("/import_regions", methods=["POST"])
def import_regions():
    # decompress the data
    data = gzip.decompress(request.data)

    data = json.loads(data)
    # print(data)
    # print(f"{long_max} {lat_max}")
    for line in data["area"]:
        for cur_reg in line:
            reg = Region(coord_long=cur_reg["longitude"],
                         coord_lat=cur_reg["latitude"],
                         temperature=cur_reg["temperature"],
                         wind_speed=cur_reg["wind_speed"],
                         humidity=cur_reg["humidity"],
                         size=cur_reg["size"])
            # print(reg)
            add_region_obj(reg)

    return "SUCCESSFUL"

# todo make form that allows us to add regions with the above call, use WTForms


def create_app():
    """Initializes the database and creates and returns the app"""
    application = Flask(__name__)
    initialize_db()
    application.register_blueprint(data_service)
    return application


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=_DATASERV_PORT)