from fastapi import APIRouter

from app.models import Warehouse
from app.services.state import state

router = APIRouter(prefix="/api/warehouses", tags=["warehouses"])


@router.get("", response_model=list[Warehouse])
def list_warehouses() -> list[Warehouse]:
    return state.list_warehouses()