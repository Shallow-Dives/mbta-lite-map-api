import os

from flask import Flask, Response
from flask_pydantic import validate

from .errors import errors
from .lite_map import map_train_leds
from .schema import OverlaySchema
from .stations import station_order

app = Flask(__name__)
app.register_blueprint(errors)


@app.route("/")
def index():
    return Response("MBTA Lite Map API", status=200)


@app.route("/v1/train-mapping/leds", methods=["POST"])
@validate()
def assemble_map(body: OverlaySchema):
    leds = map_train_leds(
        station_order=station_order,
        state_overlay=dict(body),
        mbta_api_key=os.environ.get("MBTA_API_KEY"),
    )
    return leds


@app.route("/v1/health")
def show_health():
    return Response("OK", status=200)
