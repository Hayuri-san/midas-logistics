from typing import Any

from pydantic import BaseModel, Field


class EventCreate(BaseModel):
    event_type: str = Field(..., examples=["ROAD_BLOCKED"])
    source: str = Field(..., examples=["SimulationEngine"])
    payload: dict[str, Any] = Field(default_factory=dict)