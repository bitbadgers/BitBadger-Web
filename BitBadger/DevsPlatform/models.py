from django.db import models
from django.contrib.auth.models import User


class FieldsOfSpecialisation(models.Model):
    Field_Name = models.CharField(("Field"), max_length=50, null = False, blank = False)
    Field_Description = models.TextField()
    
    def __str__(self):
        return self.Field_Name
    
class UserSpecialisation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    Area_Of_Specialisation = models.ForeignKey("FieldsOfSpecialisation", on_delete=models.CASCADE)
    
    class Meta:
        unique_together = [("user","Area_Of_Specialisation")]    

class Event(models.Model):
    event_name = models.CharField(("Event Name"), max_length=50)
    sheduled_date = models.DateField(("Sheduled Date"), auto_now=False, auto_now_add=False)
    sheduled_venue = models.CharField(("Venue"), max_length=50)
    sheduled_time = models.TimeField(("Sheduled Time"), auto_now=False, auto_now_add=False)
    event_topic = models.CharField(("Topic"), max_length=50)
    
    def __str__(self):
        return self.event_name + ' -> ' + self.event_topic 
    
class DevelopmentApproach(models.Model):
    aproach_name = models.CharField(max_length=50)
    aproach_description = models.TextField(null = True, blank = True)
    
    def __str__(self):
        return self.aproach_name

class Project(models.Model):
    project_name = models.CharField(max_length=50)
    project_field = models.ForeignKey("FieldsOfSpecialisation", on_delete=models.CASCADE)
    project_start = models.DateField(("Start time"), auto_now = False, auto_now_add=False)
    project_end = models.DateField(("Completion Time"), auto_now = False, auto_now_add=False)
    project_aproach = models.ForeignKey("DevelopmentApproach", verbose_name=("Development Approach"), on_delete=models.CASCADE, null = True, blank = True)
    project_head = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.project_name
    
class Team(models.Model):
    team_name = models.CharField(max_length=50, unique = True)
    team_field = models.ForeignKey("FieldsOfSpecialisation", on_delete = models.CASCADE)
    date_of_creation = models.DateField(auto_now=True, auto_now_add=False)
    goal = models.CharField(max_length=50, null = True, blank = True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, default = None )
    
    def __str__(self):
        return self.team_name
    
class TeamMember(models.Model):
    member_name = models.ForeignKey(User, on_delete=models.CASCADE)
    team = models.ForeignKey("Team", on_delete=models.CASCADE)
    MEMBER_ROLES = [
        (1,'Chair'),
        (2,'Vice-Chair'),
        (3,'Secretary'),
        (4,'Vice-Secretary'),
        (4,'Treasurer'),
        (5,'Other')
    ]
    member_role = models.IntegerField(choices = MEMBER_ROLES)

    class Meta:
        unique_together = [('member_name','team')]
        
    def __str__(self):
        return str(self.member_name) + " -> " + str(self.team)
        
class ProjectParticipant(models.Model):
    participant_name = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey("Project", on_delete=models.CASCADE)
    
    class Meta:
        unique_together = [('participant_name','project')]
        
    def __str__(self):
        return str(self.participant_name) + ' -> ' + str(self.project)
    
# class Message(models.Model):
#     sender = models.ForeignKey(User, on_delete=models.CASCADE)