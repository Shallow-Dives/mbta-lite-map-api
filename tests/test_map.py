import os

from dotenv import load_dotenv

from api.lite_map import map_train_leds

from .rpi_configuration import overlay, station_order

load_dotenv()


def test_led_response():
    leds = map_train_leds(
        station_order=station_order,
        state_overlay=overlay,
        mbta_api_key=os.getenv("MBTA_API_KEY"),
    )

    assert leds
    assert len(leds) == len(station_order)
    assert any(
        led_value != (255, 0, 0) for led_value in leds
    )  # At least one active station
