from django.db import models
from skills.models import Skill
from lavoro.utils import LANGUAGE_CHOICES

class Poster(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    facebook_id = models.BigIntegerField()
    language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES)