from django.shortcuts import render
import operator
import geocoder
import requests

from dateutil.parser import parse
from datetime import date
from rest_framework import viewsets, status
from rest_framework.response import Response
from jobs.models import Job
from seekers.models import Seeker
from posters.models import Poster
from skills.models import Skill
from job_history.models import JobHistory
from lavoro.utils import bounding_box, message_job, intersection

class JobHistoryViewSet(viewsets.ViewSet):

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

        past_seekers = JobHistory.filter(job = job).values_list('seeker__id', flat = True)

        potential_seekers = Seeker.objects.filter(**search_params).exclude(pk__in = past_seekers)
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

    def send_message_to_poster(self, poster, seeker, job):

        data = {
            "user_id": poster.facebook_id,
            "job_id": job.pk,
            "seeker_name": "%s %s" % (seeker.first_name, seeker.last_name),
            "seeker_skills": ", ".join(list(seeker.skills.all())),
            "language": poster.language,
        }

        requests.post('http://127.0.0.1:5000/lavoro-accept-job', data = data)

    def send_rejection(self, seeker):

        data = {
            "user_id": seeker.facebook_id,
            "language": seeker.language,
        }

        requests.post('http://127.0.0.1:5000/lavoro-reject-job', data = data)

    def send_connection(self, seeker):

        data = {
            "user_id": seeker.facebook_id,
            "language": seeker.language,
        }

        requests.post('http://127.0.0.1:5000/lavoro-new-connection', data = data)

    def create(self, request):
        data = request.POST
        job = data['job_id']
        open_history = JobHistory.objects.filter(job_id = job, status = "SA")
        if open_history.count() > 0:
        	open_history = open_history.first()
        	if data['accepted']: 
        		open_history.status = "C"	# Connected
        		open_history.save()

        		seeker = Seeker.objects.get(pk = data['user_id'])
        		seeker.last_job_accepted = date.today()
        		seeker.save()

        		job.seeker = seeker
        		job.accepted = True

        		self.send_connection(seeker)
        		return
        	else:
        		open_history.status = "PR"  # Poster Rejected
        		open_history.save()

        		self.send_rejection(seeker)

        else:
        	job = Job.objects.get(pk=job)
        	open_history = JobHistory(job = job)
        	open_history.seeker = Seeker.objects.get(data['user_id'])
        	if data['accepted']:
        		open_history.status = "SA"  # Seeker Accepted, Send message to Poster
        		open_history.save()
        		self.send_message_to_poster(job.poster, open_history.seeker, job)
        		return
        	else:
        		open_history.status = "SR"  # Seeker Rejected
        		open_history.save()


        self.find_seeker_for_job(job)

        return Response({}, status=status.HTTP_201_CREATED)
