import operator
import geocoder
import requests

from rest_framework import viewsets, status
from rest_framework.response import Response
from jobs.models import Job
from seekers.models import Seeker
from skills.models import Skill
from lavoro.utils import bounding_box, intersection, message_job

class SeekerViewSet(viewsets.ViewSet):

    def find_job_for_seeker(self, seeker):
        lat = seeker.location_lat
        lng = seeker.location_lng
        dlat, dlng = bounding_box(lat, lng)

        search_params = {
            "location_lat__lte": lat + dlat,
            "location_lat__gte": lat - dlat,
            "location_lng__lte": lng + dlng,
            "location_lng__gte": lng - dlng,
        }

        seeker_skills = seeker.skills.all()
        potential_jobs = Job.objects.filter(**search_params)
        best_fit = potential_jobs.first()
        inst = intersection(best_fit.skills.all(), seeker_skills)
        best_perc = len(intersection(best_fit.skills.all(), seeker_skills)) / float(len(best_fit.skills.all()))

        for job in potential_jobs[1:]:
            job_skills = job.skills.all()
            fit_perc = len(intersection(job_skills, seeker_skills)) / float(len(job_skills))
            if fit_perc > best_perc:
                best_perc = fit_perc
                best_fit = job

        if best_perc > 0:
            message_job(seeker, best_fit)
            return

    def create(self, request):
        data = request.POST
        facebook_id = data['facebook_id']
        seeker = Seeker.objects.filter(facebook_id=facebook_id)
        if seeker.count() == 0:
            seeker = Seeker(facebook_id=facebook_id)
        else:
            seeker = seeker[0]

        seeker.first_name = data['first_name']
        seeker.last_name = data['last_name']
        seeker.language = data['language']

        g = geocoder.google(data['location'])
        (lat,lng) = g.latlng

        seeker.location_lat = lat
        seeker.location_lng = lng
        seeker.location_text = data['location']

        seeker.save()

        for x in data.getlist('skills'):
            seeker.skills.add(Skill.objects.get(name=x))

        self.find_job_for_seeker(seeker)

        return Response({}, status=status.HTTP_201_CREATED)
