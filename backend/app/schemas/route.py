from pydantic import BaseModel, Field


class RouteFind(BaseModel):
    origin: str = Field(..., examples=["WH-A"])
    destination: str = Field(..., examples=["WH-C"])