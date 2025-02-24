from django.db.models import F, Count
from django.shortcuts import render
from rest_framework import viewsets, mixins
from rest_framework.viewsets import GenericViewSet

from airport.models import (
    Airport,
    Route,
    AirplaneType,
    Crew,
    Flight,
    Order,
    Ticket,
    Airplane
)
from airport.serializers import (
    AirportSerializer,
    RouteSerializer,
    AirplaneSerializer,
    AirplaneTypeSerializer,
    CrewSerializer,
    FlightSerializer,
    OrderSerializer,
    TicketSerializer,
    AirplaneListSerializer,
    AirplaneTypeRetrieveSerializer,
    FlightListSerializer, FlightRetrieveSerializer, OrderListSerializer, RouteListSerializer
)


class AirportViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer


class RouteViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    queryset = Route.objects.select_related("source", "destination")

    def get_serializer_class(self):
        if self.action == "list":
            return RouteListSerializer

        return RouteSerializer


class AirplaneViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    queryset = Airplane.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return AirplaneListSerializer
        return AirplaneSerializer


class AirplaneTypeViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet,
):
    queryset = AirplaneType.objects.all()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return AirplaneTypeRetrieveSerializer
        return AirplaneTypeSerializer


class CrewViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    queryset = Crew.objects.all()
    serializer_class = CrewSerializer


class FlightViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet,
):
    queryset = (
        Flight.objects.select_related(
            "route", "route__source", "route__destination", "airplane"
        )
        .prefetch_related("crew")
        .annotate(
            tickets_available=(
                    F("airplane__rows") * F("airplane__seats_in_row")
                    - Count("tickets")
            )
        )
    )

    def get_serializer_class(self):
        if self.action == "list":
            return FlightListSerializer
        elif self.action == "retrieve":
            return FlightRetrieveSerializer
        return FlightSerializer


class OrderViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    GenericViewSet,
):
    queryset = Order.objects.all()

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "list":
            return OrderListSerializer

        return OrderSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

