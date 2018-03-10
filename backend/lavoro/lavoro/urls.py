from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^seekers/', include('seekers.urls')),
    url(r'^jobs/', include('jobs.urls')),
]
