import os

from django.core.mail import EmailMessage
from django.db.models import F, Count
from drf_spectacular.utils import extend_schema, OpenApiParameter
from fpdf import FPDF
from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from airport.models import Airport, Route, AirplaneType, Crew, Flight, Order, Airplane
from airport.serializers import (
    AirportSerializer,
    RouteSerializer,
    AirplaneSerializer,
    AirplaneTypeSerializer,
    CrewSerializer,
    FlightSerializer,
    OrderSerializer,
    AirplaneListSerializer,
    AirplaneTypeRetrieveSerializer,
    FlightListSerializer,
    FlightRetrieveSerializer,
    OrderListSerializer,
    RouteListSerializer,
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


class FlightViewSet(viewsets.ModelViewSet):
    queryset = (
        Flight.objects.select_related(
            "route", "route__source", "route__destination", "airplane"
        )
        .prefetch_related("crew")
        .annotate(
            tickets_available=(
                F("airplane__rows") * F("airplane__seats_in_row") - Count("tickets")
            )
        )
    )

    def get_queryset(self):
        source = self.request.query_params.get("source")
        destination = self.request.query_params.get("destination")
        airplane = self.request.query_params.get("airplane")

        queryset = self.queryset
        if source:
            queryset = queryset.filter(
                route__source__closest_big_city__icontains=source
            )

        if destination:
            queryset = queryset.filter(
                route__destination__closest_big_city__icontains=destination
            )

        if airplane:
            queryset = queryset.filter(airplane__name__icontains=airplane)

        return queryset.distinct()

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "source",
                type={"type": "list", "items": {"type": "number"}},
                description="Filter by source city (ex. ?source=New York)",
            ),
            OpenApiParameter(
                "destination",
                type={"type": "list", "items": {"type": "number"}},
                description="Filter by destination city (ex. ?destination=New York)",
            ),
            OpenApiParameter(
                "airplane",
                type=str,
                description="Filter by airplane name (ex. ?airplane=Boeing)",
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

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
    queryset = Order.objects.prefetch_related(
        "tickets__flight__route",
        "tickets__flight__airplane",
    )

    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "list":
            return OrderListSerializer

        return OrderSerializer

    def perform_create(self, serializer):
        order = serializer.save(user=self.request.user)
        file_path = self.generate_ticket_pdf(order)

        email_message = EmailMessage(
            subject="Your Ticket Confirmation",
            body="Your ticket is attached.",
            from_email="no-reply@example.com",
            to=[self.request.user.email],
        )

        with open(file_path, "rb") as file:
            email_message.attach(
                f"ticket_order_{order.id}.pdf", file.read(), "application/pdf"
            )

        email_message.send()
        os.remove(file_path)

    def generate_ticket_pdf(self, order) -> str:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Your Ticket", ln=True, align="C")

        for ticket in order.tickets.all():
            pdf.cell(
                200,
                10,
                txt=f"Flight: {ticket.flight}",
                ln=True,
                align="L"
            )
            pdf.cell(
                200,
                10,
                txt=f"Row: {ticket.row}, Seat: {ticket.seat}",
                ln=True,
                align="L",
            )

        file_path = f"ticket_order_{order.id}.pdf"
        pdf.output(file_path)

        return file_path
