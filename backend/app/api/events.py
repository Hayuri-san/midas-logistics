from fastapi import APIRouter

from app.schemas import EventCreate
from app.services.events import process_event
from app.services.state import state

router = APIRouter(prefix="/api/events", tags=["events"])


@router.post("")
def create_event(payload: EventCreate) -> dict:
    return process_event(state, payload.event_type, payload.payload)