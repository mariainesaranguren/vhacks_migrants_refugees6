from django.contrib import admin
from seekers.models import Seeker

class SeekerAdmin(admin.ModelAdmin):
    list_display = ('name',)

    def name(self, obj):
        return "%s %s" % (obj.first_name, obj.last_name)

admin.site.register(Seeker, SeekerAdmin)