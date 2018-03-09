from django.db import models
from skills.models import Skill

class Job(models.Model):
    skills = models.ManyToManyField(Skill)
    date = models.DateField()
    name = models.CharField(max_length=300)
    description = models.TextField()
    wage = models.DecimalField(max_digits=6, decimal_places=2)
    location_lat = models.DecimalField(max_digits=9, decimal_places=6)
    location_lng = models.DecimalField(max_digits=9, decimal_places=6)
    location_text = models.CharField(max_length=200)