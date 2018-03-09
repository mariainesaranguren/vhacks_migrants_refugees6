from django.db import models
from skills.models import Skill
from jobs.models import Job

class Seeker(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    skills = models.ManyToManyField(Skill)
    location_lat = models.DecimalField(max_digits=9, decimal_places=6)
    location_lng = models.DecimalField(max_digits=9, decimal_places=6)
    location_text = models.CharField(max_length=200)
    facebook_id = models.BigIntegerField()
    jobs = models.ForeignKey(Job, on_delete=models.CASCADE)