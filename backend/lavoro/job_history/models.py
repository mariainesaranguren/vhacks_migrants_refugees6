from django.db import models
from jobs.models import Job
from seekers.models import Seeker

class JobHistory(models.Model):
    STATUS_CHOICES = (
        ("C", "Connected"),
        ("SA", "Seeker Accepted"),
        ("SR", "Seeker Rejected"),
        ("PR", "Posted Rejected"),
    )

    status = models.CharField(max_length=2, choices=STATUS_CHOICES)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    seeker = models.ForeignKey(Seeker, on_delete=models.CASCADE)