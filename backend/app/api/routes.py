from fastapi import APIRouter, HTTPException, status

from app.models import Route
from app.schemas import RouteFind
from app.services import routing
from app.services.state import state

router = APIRouter(prefix="/api/routes", tags=["routes"])


@router.get("", response_model=list[Route])
def list_routes() -> list[Route]:
    return state.list_routes()


@router.post("/find", response_model=Route)
def find_route(payload: RouteFind) -> Route:
    route = routing.get_routing_engine().select_route(
        state.list_routes(), payload.origin, payload.destination
    )
    if route is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No available route found")
    return route