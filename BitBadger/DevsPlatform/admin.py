from django.contrib import admin

from .models import FieldsOfSpecialisation, UserSpecialisation, Event, Project, ProjectParticipant ,Team, TeamMember, DevelopmentApproach

admin.site.register(FieldsOfSpecialisation)
admin.site.register(UserSpecialisation)
admin.site.register(Event)
admin.site.register(DevelopmentApproach)
admin.site.register(Project)
admin.site.register(ProjectParticipant)
admin.site.register(Team)
admin.site.register(TeamMember)
# Register your models here.
