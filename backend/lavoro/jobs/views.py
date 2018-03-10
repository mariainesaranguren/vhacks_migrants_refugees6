import operator
import geocoder

from dateutil.parser import parse
from rest_framework import viewsets, status
from rest_framework.response import Response
from jobs.models import Job
from seekers.models import Seeker
from posters.models import Poster
from skills.models import Skill
from lavoro.utils import bounding_box, message_job, intersection

class JobsViewSet(viewsets.ViewSet):

    def find_seeker_for_job(self, job):
        lat = job.location_lat
        lng = job.location_lng
        dlat, dlng = bounding_box(lat, lng)

        search_params = {
            "location_lat__lte": lat + dlat,
            "location_lat__gte": lat - dlat,
            "location_lng__lte": lng + dlng,
            "location_lng__gte": lng - dlng,
        }

        potential_seekers = Seeker.objects.filter(**search_params)
        job_skills = job.skills.all()
        max_score = 0
        max_seekers = []

        for seeker in potential_seekers:
            seeker_skills = seeker.skills.all()
            score = len(intersection(job_skills, seeker_skills))/float(len(job_skills))
            if score > max_score:
                max_score = score
                max_seekers = [seeker]
            elif score == max_score:
                max_seekers.append(seeker)

        max_seekers = sorted(max_seekers, key=lambda seeker: seeker.last_job_accepted)

        if len(max_seekers) > 0:
            seeker = max_seekers[0]
            message_job(seeker, job)

    def create(self, request):
        data = request.POST
        facebook_id = data['facebook_id']
        poster = Poster.objects.filter(facebook_id=facebook_id)

        if poster.count() == 0:
            poster = Poster()
        else:
            poster = poster[0]
        poster.first_name = data['first_name']
        poster.last_name = data['last_name']
        poster.language = data['language']
        poster.facebook_id = data['facebook_id']
        poster.save()

        job = Job()
        job.poster = poster
        job.date = parse(data['job_date'])
        job.name = data['job_name']
        job.description = data['job_description']
        job.wage = data['job_wage']

        g = geocoder.google(data['location'])
        (lat,lng) = g.latlng

        job.location_lat = lat
        job.location_lng = lng
        job.location_text = data['location']
        job.save()
        
        for x in data.getlist('skills'):
            job.skills.add(Skill.objects.get(name=x))

        self.find_seeker_for_job(job)

        return Response({}, status=status.HTTP_201_CREATED)
