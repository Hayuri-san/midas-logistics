from abc import ABC, abstractmethod

from app.models import Route, RouteStatus


class RoutingEngine(ABC):
    @abstractmethod
    def select_route(self, routes: list[Route], origin: str, destination: str) -> Route | None:
        raise NotImplementedError


class DefaultRoutingEngine(RoutingEngine):
    def select_route(self, routes: list[Route], origin: str, destination: str) -> Route | None:
        candidates = [
            route for route in routes
            if route.origin == origin
            and route.destination == destination
            and route.status == RouteStatus.AVAILABLE
        ]
        traffic_score = {"low": 0, "medium": 1, "high": 2}
        condition_score = {"good": 0, "fair": 1, "bad": 2}
        road_score = {"highway": 0, "local": 1}
        return min(
            candidates,
            key=lambda route: (
                traffic_score.get(route.traffic, 99),
                condition_score.get(route.condition, 99),
                road_score.get(route.road_type, 99),
                route.distance,
                route.id,
            ),
            default=None,
        )


_active_routing_engine: RoutingEngine = DefaultRoutingEngine()


def get_routing_engine() -> RoutingEngine:
    return _active_routing_engine


def set_routing_engine(engine: RoutingEngine) -> None:
    global _active_routing_engine
    _active_routing_engine = engine