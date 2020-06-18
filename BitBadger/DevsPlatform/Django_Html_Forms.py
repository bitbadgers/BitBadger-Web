from django import forms

from .models import UserSpecialisation, Project, ProjectParticipant



class AreaOfSpecialisationForm(forms.ModelForm):
    class Meta:
        model = UserSpecialisation
        fields = ('Area_Of_Specialisation',)
        
class CreateProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = '__all__'
        
class JoinProjectForm(forms.ModelForm):
    class Meta:
        model = ProjectParticipant
        fields =  ['project']
        
        
        