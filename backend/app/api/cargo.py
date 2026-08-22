from fastapi import APIRouter, status

from app.models import Cargo
from app.schemas import CargoCreate
from app.services.state import state

router = APIRouter(prefix="/api/cargo", tags=["cargo"])


@router.get("", response_model=list[Cargo])
def list_cargo() -> list[Cargo]:
    return state.list_cargo()


@router.post("", response_model=Cargo, status_code=status.HTTP_201_CREATED)
def create_cargo(payload: CargoCreate) -> Cargo:
    """Create a cargo request. Does NOT trigger matching or assignment yet —
    that's a later milestone."""
    return state.add_cargo(
        company=payload.company,
        origin=payload.origin,
        destination=payload.destination,
        quantity=payload.quantity,
    )
