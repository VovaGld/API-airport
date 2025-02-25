from django.core.exceptions import ValidationError
from airport.models import Ticket, Flight, Airport, Route


def validate_ticket_seat(row: int, seat: int, flight: Flight) -> None:
    airplane = flight.airplane

    if not (1 <= row <= airplane.rows):
        raise ValidationError(f"Row {row} exceeds the airplane's limits (1-{airplane.rows}).")

    if not (1 <= seat <= airplane.seats_in_row):
        raise ValidationError(f"Seat {seat} exceeds the airplane's limits (1-{airplane.seats_in_row}).")

    if Ticket.objects.filter(flight=flight, row=row, seat=seat).exists():
        raise ValidationError(f"Seat {seat} in row {row} is already occupied.")


def validate_route(source: Airport, destination: Airport) -> None:
    if source.name == destination.name:
        raise ValidationError("You can`t create this route.")

    if Route.objects.filter(source=source, destination=destination).exists():
        raise ValidationError("This route already exists.")
