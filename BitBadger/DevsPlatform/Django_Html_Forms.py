from django import forms

from .models import UserSpecialisation, Project, ProjectParticipant, TeamMember, Team



class AreaOfSpecialisationForm(forms.ModelForm):
    class Meta:
        model = UserSpecialisation
        fields = ('Area_Of_Specialisation',)
        
class CreateProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['project_name','project_field','project_end','project_end','project_aproach','add_priviledge','maximum_members']
        widgets ={
                'project_end' : forms.widgets.DateInput(attrs={'type': 'date', 'format' : 'dd/mm/yyyy'}),
            }
        
class JoinProjectForm(forms.ModelForm):
    class Meta:
        model = ProjectParticipant
        fields =  ['project']
        
class AddToProjectForm(forms.ModelForm):
    class Meta:
        model = ProjectParticipant
        fields =  ['participant_name']
        
class JoinTeamForm(forms.ModelForm):
    class Meta:
        model = TeamMember
        fields = ['team']
        
class CreateTeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['team_name','team_field','goal','max_number']

class AddTeamMemberForm(forms.ModelForm):
    class Meta:
        model = TeamMember
        fields = ['member_name', 'member_role']
        
class MinifyForm(forms.Form):
    file = forms.FileField(label = "Upload JS/CSS file")
        
        