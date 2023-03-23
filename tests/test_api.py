import os
from typing import Dict, Tuple

import pytest

from api.app import app
from api.exceptions import MBTAError


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_index(client):
    assert client.get("/").status_code == 200


def test_health(client):
    assert client.get("/v1/health").status_code == 200


def test_validation(client):
    test_payload: Dict[str, Tuple] = dict(
        IN_TRANSIT_TO=(0.01, 0.01, 0.0),
        INCOMING_AT=(0.01, 0.2, 0.0),
        STOPPED_AT=(0.0, 0.5, 0.0),
    )

    response = client.post(
        "/v1/train-mapping/leds",
        json=test_payload,
        headers={"Content-Type": "application/json", "X-Api-Key": os.getenv("LITEMAP_API_KEY")},
    )

    assert response.content_type == "application/json"
    assert response.status_code == 200

    bad_payload: Dict[str, Tuple] = dict(IN_TRANSIT_TO=(0.01, 0.01, 0.0))

    response = client.post(
        "/v1/train-mapping/leds",
        json=bad_payload,
        headers={"Content-Type": "application/json", "X-Api-Key": os.getenv("LITEMAP_API_KEY")},
    )

    assert response.status_code == 400


def test_custom_exception():
    with pytest.raises(MBTAError) as exc_info:

        def test_raise():
            raise MBTAError("Test MBTAError")

        test_raise()

    exception_raised = exc_info.value
    assert exception_raised.status_code == 500
    assert exception_raised.message == "Test MBTAError"
