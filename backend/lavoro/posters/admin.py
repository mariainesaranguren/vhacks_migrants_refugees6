from django.contrib import admin
from posters.models import Poster

class PosterAdmin(admin.ModelAdmin):
    list_display = ('name',)

    def name(self, obj):
        return "%s %s" % (obj.first_name, obj.last_name)

admin.site.register(Poster, PosterAdmin)
