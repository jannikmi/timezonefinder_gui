from django.db import models
from django.db.models import F


class TimezoneStatistics(models.Model):
    # null has to be allowed as well, because failing queries should also be counted
    tz_name = models.CharField(null=True, max_length=50)
    api_hits = models.BigIntegerField(default=0)
    geometry_hits = models.BigIntegerField(default=0)
    info_hits = models.BigIntegerField(default=0)

    # # actually api is called every time (geometry<info<api)
    # def total_hits(self):
    #     return self.geometry_hits + self.api_hits

    def increment_api_hits(self):
        self.api_hits = F('api_hits') + 1
        self.save()

    def increment_geometry_hits(self):
        self.geometry_hits = F('geometry_hits') + 1
        self.save()

    def increment_info_hits(self):
        self.info_hits = F('info_hits') + 1
        self.save()

    def __str__(self):
        return self.tz_name


def register_api_hit(tz_name):
    try:
        TimezoneStatistics.objects.get(tz_name=tz_name).increment_api_hits()
    except TimezoneStatistics.DoesNotExist:
        TimezoneStatistics.objects.create(tz_name=tz_name).increment_api_hits()


def register_geometry_hit(tz_name):
    try:
        TimezoneStatistics.objects.get(tz_name=tz_name).increment_geometry_hits()
    except TimezoneStatistics.DoesNotExist:
        TimezoneStatistics.objects.create(tz_name=tz_name).increment_geometry_hits()


def register_info_hit(tz_name):
    try:
        TimezoneStatistics.objects.get(tz_name=tz_name).increment_info_hits()
    except TimezoneStatistics.DoesNotExist:
        TimezoneStatistics.objects.create(tz_name=tz_name).increment_info_hits()
