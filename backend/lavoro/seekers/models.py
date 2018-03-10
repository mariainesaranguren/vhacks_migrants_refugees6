from django.db import models
from skills.models import Skill
from datetime import date
from lavoro.utils import LANGUAGE_CHOICES

class Seeker(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    skills = models.ManyToManyField(Skill)
    location_lat = models.DecimalField(max_digits=9, decimal_places=6)
    location_lng = models.DecimalField(max_digits=9, decimal_places=6)
    location_text = models.CharField(max_length=200)
    facebook_id = models.BigIntegerField()
    language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES)
    last_job_accepted = models.DateField(default=date.min)