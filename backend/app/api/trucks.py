from fastapi import APIRouter

from app.models import Truck
from app.services.state import state

router = APIRouter(prefix="/api/trucks", tags=["trucks"])


@router.get("", response_model=list[Truck])
def list_trucks() -> list[Truck]:
    return state.list_trucks()
