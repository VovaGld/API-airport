from django.db import transaction
from rest_framework import serializers

from airport.models import (
    Airport,
    Route,
    AirplaneType,
    Airplane,
    Crew,
    Flight,
    Order,
    Ticket,
)
from airport.validators import validate_ticket_seat, validate_route


class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = ("id", "name", "closest_big_city")


class RouteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Route
        fields = ("id", "source", "destination", "distance")

    def validate(self, data):
        validate_route(data["source"], data["destination"])
        return data


class RouteListSerializer(RouteSerializer):
    destination = source = serializers.StringRelatedField()


class AirplaneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airplane
        fields = ("id", "name", "rows", "seats_in_row", "airplane_type")


class AirplaneListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airplane
        fields = ("id", "name", "capacity")


class AirplaneTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AirplaneType
        fields = ("id", "name")


class AirplaneTypeRetrieveSerializer(serializers.ModelSerializer):
    airplanes = AirplaneListSerializer(many=True, read_only=True)

    class Meta:
        model = AirplaneType
        fields = ("name", "airplanes")


class CrewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crew
        fields = ("first_name", "last_name")


class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = ("id", "route", "airplane", "crew", "departure_date", "arrival_date")


class FlightListSerializer(FlightSerializer):
    route = serializers.SerializerMethodField()
    airplane = serializers.StringRelatedField()
    tickets_available = serializers.IntegerField(read_only=True)

    class Meta:
        model = Flight
        fields = (
            "id",
            "route",
            "airplane",
            "tickets_available",
            "departure_date",
            "arrival_date",
        )

    def get_route(self, obj):
        return f"{obj.route.source.closest_big_city} - {obj.route.destination.closest_big_city}"


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ("id", "row", "seat", "flight")

    def validate(self, data):
        validate_ticket_seat(data["row"], data["seat"], data["flight"])
        return data


class TicketListSerializer(TicketSerializer):
    flight = FlightListSerializer(read_only=True)


class TicketSeatsSerializer(TicketSerializer):
    class Meta:
        model = Ticket
        fields = ("row", "seat")


class FlightRetrieveSerializer(FlightListSerializer):
    crew = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="full_name"
    )
    taken_place = TicketSeatsSerializer(many=True, read_only=True, source="tickets")

    class Meta:
        model = Flight
        fields = (
            "id",
            "route",
            "airplane",
            "crew",
            "departure_date",
            "arrival_date",
            "taken_place",
        )


class OrderSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(many=True)

    class Meta:
        model = Order
        fields = ("id", "tickets", "created_at")

    def create(self, validated_data):
        with transaction.atomic():
            tickets_data = validated_data.pop("tickets")
            order = Order.objects.create(**validated_data)
            tickets = [Ticket(order=order, **ticket_data) for ticket_data in tickets_data]
            Ticket.objects.bulk_create(tickets)


class OrderListSerializer(OrderSerializer):
    tickets = TicketListSerializer(many=True, read_only=True)
