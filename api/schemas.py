from typing import Tuple

from pydantic import BaseModel


class Overlay(BaseModel):
    IN_TRANSIT_TO: Tuple[float, float, float]
    INCOMING_AT: Tuple[float, float, float]
    STOPPED_AT: Tuple[float, float, float]
