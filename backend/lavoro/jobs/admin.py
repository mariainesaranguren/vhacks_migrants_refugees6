from django.contrib import admin
from jobs.models import Job

class JobAdmin(admin.ModelAdmin):
    list_display = ('name',)

    def name(self, obj):
        return "%s %s" % (obj.first_name, obj.last_name)

admin.site.register(Job, JobAdmin)