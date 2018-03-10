import requests
from math import sin, asin, cos, radians, degrees

LANGUAGE_CHOICES = (
    ("AR", "Arabic"),
    ("EN", "English"),
    ("FR", "French"),
    ("IT", "Italian"),
    ("ES", "Spanish"),
)

def bounding_box(lat, lon, distance = 10):
    dlat = distance / 6371.0
    dlon = asin(sin(dlat) / cos(radians(lat)))
    return degrees(dlat), degrees(dlon)

def message_job(seeker, job):

    data = {
        "user_id": seeker.facebook_id,
        "job_id": job.pk,
        "job_description": job.description,
        "language": seeker.language,
        "job_wage": job.wage
    }

    requests.post('localhost:5000/lavoro-new-job', data = data)

def intersection(a, b):
    return [x for x in a if (x in b)]