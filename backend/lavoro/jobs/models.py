from django.db import models
from skills.models import Skill
from seekers.models import Seeker
from posters.models import Poster

class Job(models.Model):
    seeker = models.ForeignKey(Seeker, on_delete=models.CASCADE, null=True)
    poster = models.ForeignKey(Poster, on_delete=models.CASCADE)
    skills = models.ManyToManyField(Skill)
    date = models.DateField()
    name = models.CharField(max_length=300)
    description = models.TextField()
    wage = models.DecimalField(max_digits=6, decimal_places=2)
    location_lat = models.DecimalField(max_digits=9, decimal_places=6)
    location_lng = models.DecimalField(max_digits=9, decimal_places=6)
    location_text = models.CharField(max_length=200)
    assigned = models.BooleanField(default=False)