from fastapi import HTTPException, status

from app.models import RouteStatus
from app.services.state import AppState


def process_event(state: AppState, event_type: str, payload: dict) -> dict:
    if event_type in {"ROAD_BLOCKED", "ROAD_CLEARED"}:
        route_id = payload.get("route_id")
        if route_id not in state.routes:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Route not found")
        route_status = RouteStatus.BLOCKED if event_type == "ROAD_BLOCKED" else RouteStatus.AVAILABLE
        state.set_route_status(route_id, route_status)
    elif event_type == "TRUCK_BREAKDOWN":
        truck_id = payload.get("truck_id")
        if truck_id not in state.trucks:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Truck not found")
        state.break_truck(truck_id)
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unsupported event type")
    return {"status": "processed", "event_type": event_type}