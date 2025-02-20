from rest_framework import serializers

from airport.models import (
    Airport,
    Route,
    AirplaneType,
    Airplane,
    Crew,
    Flight,
    Order,
    Ticket
)


class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = ("name", "closest_big_city")


class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = ("source", "destination", "distance")


class AirplaneTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AirplaneType
        fields = ("name", )


class AirplaneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airplane
        fields = ("name", "rows", "seats_in_row", "airplane_type")


class CrewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crew
        fields = ("first_name", "last_name")


class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = ("route", "airplane", "crew", "departure_date", "arrival_date")


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ("created_at", "user")


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ("row", "seat", "flight", "order")
