import os

import googlemaps
from django.db import models
from django.core.validators import MinValueValidator


class Route(models.Model):
    start_point = models.CharField(max_length=255)
    start_lat = models.DecimalField(max_digits=9, decimal_places=6)
    start_long = models.DecimalField(max_digits=9, decimal_places=6)

    end_point = models.CharField(max_length=255)
    end_lat = models.DecimalField(max_digits=9, decimal_places=6)
    end_long = models.DecimalField(max_digits=9, decimal_places=6)

    _cached_maps_client = None

    def __str__(self):
        return f"From {self.start_point} to {self.end_point}"

    @classmethod
    def maps_client(cls):
        if not cls._cached_maps_client:
            google_key = os.getenv("GOOGLE_KEY")
            cls._cached_maps_client = googlemaps.Client(key=google_key)
        return cls._cached_maps_client

    # Response example:
    # {
    #   "destination_addresses": [
    #     "Unnamed Road, Latgales priekšpilsēta, Rīga, LV-1019, Latvia"
    #   ],
    #   "origin_addresses": [
    #     "Brīvības gatve 372, Vidzemes priekšpilsēta, Rīga, LV-1006, Latvia"
    #   ],
    #   "rows": [
    #     {
    #       "elements": [
    #         {
    #           "distance": { "text": "9.8 km", "value": 9802 },
    #           "duration": { "text": "19 mins", "value": 1151 },
    #           "status": "OK"
    #         }
    #       ]
    #     }
    #   ],
    #   "status": "OK"
    # }
    def measure(self):
        # origin = "56.982915,24.205900"  # Alfa
        # destination = "56.924397,24.172713"  # Akropole
        start = f"{self.start_lat},{self.start_long}"
        end = f"{self.end_lat},{self.end_long}"
        result = self._maps_client.distance_matrix(start, end)
        if not result["status"] == "OK":
            raise Exception(f'Unexpected status {result["status"]} in: \n{result}')
        plan = result["rows"][0]["elements"][0]
        if not plan["status"] == "OK":
            raise Exception(f'Unexpected status {plan["status"]} in: \n{result}')
        self.measurement_set.create(
            seconds=plan["duration"]["value"], meters=plan["distance"]["value"]
        )

    @property
    def _maps_client(self):
        return type(self).maps_client()


class Measurement(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    seconds = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    meters = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"#{self.id} {self.created_at.strftime('%d.%m.%Y %H:%M')}"
