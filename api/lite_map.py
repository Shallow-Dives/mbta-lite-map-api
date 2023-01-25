from typing import Dict, List, Tuple

from pymbta3 import Stops, Vehicles

from .exceptions import InvalidStationName, MBTAError, MBTAUnreachable


def get_station_name(station_id: str, mbta_api_key: str) -> str:
    """
    Confirm that stations ids have not changed
    :param str station_id: Station id used to look up station details
    :param str mbta_api_key: Key for MBTA API
    :return str station_name: Station name matching id
    """
    request = Stops(mbta_api_key)
    try:
        stop = request.get(id=station_id)

        if "data" in stop:
            station_name = stop["data"][0]["attributes"]["description"]
            return station_name
        else:
            raise MBTAError(
                stop["errors"][0]["status"], ":", stop["errors"][0]["detail"], 500
            )

    except ConnectionError as e:
        raise MBTAUnreachable(e)


def get_redline_trains(mbta_api_key: str) -> Dict:
    """
    Get the list of in service Red Line trains with status from pymbta3
    Info: train data format at https://api-v3.mbta.com/docs/swagger/index.html
    :param str mbta_api_key: Key for MBTA API
    :return: trains: dict of trains currently operating on Red Line
    """
    request = Vehicles(mbta_api_key)
    try:
        trains = request.get(route="Red")

        if "data" in trains:
            return trains
        else:
            raise MBTAError(
                trains["errors"][0]["status"], ":", trains["errors"][0]["detail"], 500
            )

    except ConnectionError as e:
        raise MBTAUnreachable(e)


def map_train_leds(
    station_order: Tuple, state_overlay: Dict, mbta_api_key: str
) -> List[Tuple]:
    """
    Map list of Red Line trains into display format
    Info: train data format at https://api-v3.mbta.com/docs/swagger/index.html
    :param Tuple station_order: List of MBTA stations in display order
    :param Dict state_overlay: Brightness overlay to map train status to leds
    :param str mbta_api_key: Key for MBTA API
    :return: leds: list of led update values in station order representing train status
    """
    # Get the active train list from the MBTA API
    trains = get_redline_trains(mbta_api_key)

    leds: List[Tuple] = [(255, 0, 0)] * len(station_order)
    # Pad terminus stations for easy brightness overlay edge handling
    brightness_overlay: List[float] = [0.0] * (len(station_order) + 2)
    for train in trains["data"]:
        # Get the station description
        stop: dict = train["relationships"]["stop"]["data"]
        if not stop:
            continue  # Handle MBTA test/incomplete vehicle data
        station_id: str = stop["id"]
        station_name: str = get_station_name(station_id, mbta_api_key)

        # Look up the LED index by station id
        led_index = [
            i
            for i, station in enumerate(station_order)
            if station in station_name.split("-")[0]
        ]
        if len(led_index) != 1:
            raise InvalidStationName(
                f"LED Mapping Error: Station not found: {station_name}."
            )

        led_index = led_index[0] + 1  # account for overlay padding

        # Get status tuple in correct direction
        status: str = train["attributes"]["current_status"]
        flip: int = train["attributes"]["direction_id"]
        status_map: Tuple = (
            state_overlay[status][::-1] if flip else state_overlay[status]
        )

        # Apply to LED display brightness
        for i in range(len(status_map)):
            brightness_overlay[(led_index - 1) + i] += status_map[i]

    # Cap brightness values at 1
    brightness_overlay = [min(brightness, 1.0) for brightness in brightness_overlay]
    # Cut off end station padding and apply brightness value to led list
    leds = [
        (int(led[0] * brightness), 0, 0)
        for led, brightness in zip(leds, brightness_overlay[1:-1])
    ]

    return leds
