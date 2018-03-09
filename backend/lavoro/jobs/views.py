from rest_framework import viewsets

class JobsViewSet(viewsets.ViewSet):

	def bounding_box(self, lat, lon, distance = 10):
	    dlat = distance / 6371.0
	    dlon = asin(sin(dlat) / cos(radians(lat)))
	    return degrees(dlat), degrees(dlon)


	def find_seeker_for_job(self, job):
		lat = lob.location_lat
		lng = job.location_lng
		dlat, dlng = self.bounding_box(lat, lng)

		search_params = {
			"location_lat__lte": lat + dlat,
			"location_lat__gte": lat - dlat,
			"location_lng__lte": lng + dlng,
			"location_lng__gte": lng - dlng,
		}

		# user_id, job_id, job_description


    def create(self, request):
    	data = request.POST
    	facebook_id = data['facebook_id']
    	poster = Poster.objects.filter(facebook_id=facebook_id)

    	if poster.count == 0:
    		poster = Poster()
    		poster.first_name = data['first_name']
    		poster.last_name = data['last_name']
    		poster.phone_number = data['phone_number']
    		poster.facebook_id = data['facebook_id']
    		poster.save()

    	job = Job()
    	job.date = data['job_date']
    	job.name = data['job_name']
    	job.description = data['job_descriptions']
    	job.wage = data['job_wage']
    	job.location_lat = data['location_lat']
    	job.location_lng = data['location_lng']
    	job.location_text = data['location_text']

    	# Add skills, make sure you query the object

    	job.save()

        return Response({}, status=status.HTTP_201_CREATED)
