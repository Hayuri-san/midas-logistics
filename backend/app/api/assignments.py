from fastapi import APIRouter

from app.models import Assignment
from app.services.state import state

router = APIRouter(prefix="/api/assignments", tags=["assignments"])


@router.get("", response_model=list[Assignment])
def list_assignments() -> list[Assignment]:
    return state.list_assignments()
