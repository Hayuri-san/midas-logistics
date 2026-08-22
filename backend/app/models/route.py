from enum import Enum

from pydantic import BaseModel, Field


class RouteStatus(str, Enum):
    AVAILABLE = "available"
    BLOCKED = "blocked"


class Route(BaseModel):
    id: str = Field(..., examples=["ROUTE-01"])
    origin: str = Field(..., examples=["WH-A"])
    destination: str = Field(..., examples=["WH-C"])
    road_type: str = Field(..., examples=["highway"])
    traffic: str = Field(..., examples=["low"])
    condition: str = Field(..., examples=["good"])
    distance: float = Field(..., gt=0, examples=[120])
    status: RouteStatus = RouteStatus.AVAILABLE