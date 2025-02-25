from django.urls import path, include
from rest_framework.routers import DefaultRouter

from airport.views import AirportViewSet, RouteViewSet, AirplaneTypeViewSet, AirplaneViewSet, CrewViewSet, \
    FlightViewSet, OrderViewSet

router = DefaultRouter()
router.register("airports", AirportViewSet, basename="airports")
router.register("routes", RouteViewSet)
router.register("airplane-types", AirplaneTypeViewSet)
router.register("airplanes", AirplaneViewSet)
router.register("crews", CrewViewSet)
router.register("flights", FlightViewSet)
router.register("orders", OrderViewSet)

urlpatterns = [
    path("", include(router.urls)),
]

app_name = "airport"