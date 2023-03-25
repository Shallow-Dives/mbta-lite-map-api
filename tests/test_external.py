import os

from pymbta3 import Stops, Vehicles


def test_red_line_responsive():
    request = Vehicles(os.getenv("MBTA_API_KEY"))
    trains = request.get(route="Red")
    assert "data" in trains


def test_stop_id_lookup():
    request = Stops(os.getenv("MBTA_API_KEY"))
    stop = request.get(id="70070")
    assert "data" in stop
