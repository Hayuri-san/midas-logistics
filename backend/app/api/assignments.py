from fastapi import APIRouter, HTTPException, status

from app.models import Assignment
from app.schemas import AssignmentCreate
from app.services.state import state

router = APIRouter(prefix="/api/assignments", tags=["assignments"])


@router.get("", response_model=list[Assignment])
def list_assignments() -> list[Assignment]:
    return state.list_assignments()


@router.post("", response_model=Assignment, status_code=status.HTTP_201_CREATED)
def create_assignment(payload: AssignmentCreate) -> Assignment:
    if payload.cargo_id not in state.cargo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cargo not found")
    if payload.truck_id not in state.trucks:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Truck not found")
    if payload.route_id is not None and payload.route_id not in state.routes:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Route not found")
    return state.add_assignment(payload.cargo_id, payload.truck_id, payload.route_id)
