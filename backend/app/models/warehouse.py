from pydantic import BaseModel, Field


class Warehouse(BaseModel):
    id: str = Field(..., examples=["WH-A"])
    name: str = Field(..., examples=["Warehouse A"])