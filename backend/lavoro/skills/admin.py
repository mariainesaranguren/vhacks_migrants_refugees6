from django.contrib import admin
from skills.models import Skill

class SkillAdmin(admin.ModelAdmin):
    fields = ('name',)

admin.site.register(Skill, SkillAdmin)