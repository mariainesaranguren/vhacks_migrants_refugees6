from django.db import models
from skills.models import Skill
from jobs.models import Job

class Poster(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    facebook_id = models.BigIntegerField()
    jobs = models.ForeignKey(Job, on_delete=models.CASCADE)
