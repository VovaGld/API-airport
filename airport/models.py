from django.conf import settings
from django.db import models



class Airport(models.Model):
    name = models.CharField(max_length=255)
    closest_big_city = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ["name", "closest_big_city"]


class Route(models.Model):
    source = models.ForeignKey(
        Airport,
        on_delete=models.CASCADE,
        related_name="routes"
    )
    destination = models.ForeignKey(
        Airport,
        on_delete=models.CASCADE,
        related_name="routes"
    )
    distance = models.IntegerField()

    def __str__(self):
        return f"{self.source.closest_big_city} - {self.destination.closest_big_city}"


class AirplaneType(models.Model):
    name = models.CharField(max_length=255, unique=True)
    def __str__(self):
        return self.name


class Airplane(models.Model):
    name = models.CharField(max_length=255)
    rows = models.IntegerField()
    seats_in_row = models.IntegerField()
    airplane_type = models.ForeignKey(
        AirplaneType,
        on_delete=models.CASCADE,
        related_name="airplanes"
    )

    def __str__(self):
        return self.name

    @property
    def capacity(self):
        return self.rows * self.seats_in_row


class Crew(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class Flight(models.Model):
    route = models.ForeignKey(
        Route,
        on_delete=models.CASCADE,
        related_name="flights"
    )
    airplane = models.ForeignKey(
        Airplane,
        on_delete=models.CASCADE,
        related_name="flights"
    )
    departure_date = models.DateTimeField()
    arrival_date = models.DateTimeField()

    def __str__(self):
        return f"{self.airplane.name} ({self.route.source} - {self.route.destination})"

