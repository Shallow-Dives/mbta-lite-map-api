import os
from functools import wraps

from flask import Flask, Response, abort, request
from flask_pydantic import validate

from .errors import errors
from .lite_map import map_train_leds
from .schemas import Overlay
from .stations import station_order

app = Flask(__name__)
app.register_blueprint(errors)
from flask import abort, request


def require_apikey(view_function):
    @wraps(view_function)
    def decorated_function(*args, **kwargs):
        if request.headers.get('X-Api-Key') and request.headers.get('X-Api-Key') == os.environ.get(
            "LITEMAP_API_KEY"
        ):
            return view_function(*args, **kwargs)
        else:
            abort(401)

    return decorated_function


@app.route("/")
def index():
    return Response("MBTA Lite Map API", status=200)


@app.route("/v1/train-mapping/leds", methods=["POST"])
@validate()
@require_apikey
def assemble_map(body: Overlay):
    leds = map_train_leds(
        station_order=station_order,
        state_overlay=dict(body),
        mbta_api_key=os.environ.get("MBTA_API_KEY"),
    )
    return leds


@app.route("/v1/health")
def show_health():
    return Response("OK", status=200)
