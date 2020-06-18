from django.shortcuts import render, redirect
from django.contrib import messages, sessions
from datetime import datetime
from django.contrib.auth import logout

from .models import FieldsOfSpecialisation, UserSpecialisation, Event, ProjectParticipant, Project, Team, TeamMember
from .Django_Html_Forms import AreaOfSpecialisationForm, CreateProjectForm

def Home(request):
    loged_user = request.user
    if loged_user.is_authenticated:
        if request.method == 'POST':
            form = AreaOfSpecialisationForm(request.POST)
            field = form.save(commit = False)
            field.user = loged_user
            try:
                field.save()
            except:
                messages.error(request, "The Area of specialisation must be unique")
            return redirect(request.META['HTTP_REFERER'])
        return render(request,'DevsPlatform/LoginHome.html', ContextBuilder(request))
    else:
        return redirect('index')
    
def CreateProject(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = CreateProjectForm(request.POST)
            if form.is_valid():
                try:
                    form.save()
                    messages.success(request, "The project has been created successfuly")
                except Exception as e:
                    messages.success(request, e)
                
                context = ContextBuilder(
                    request,
                    create_project_form = form
                )
                return render(request, 'DevsPlatform/createproject.html', context )
        else:
            context = ContextBuilder(
                request,
                create_project_form = CreateProjectForm()
            )
            return render(request, 'DevsPlatform/createproject.html', context )
    else:
        return redirect('index')
    
def JoinProject(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pass
    else:
        return redirect('index')
def UserLogout(request):
    logout(request)
    return redirect('index')

def ContextBuilder(request, **kwargs):
    context = {
        'user_fields' : UserSpecialisation.objects.filter(user = request.user),
        'user_specialisation_form' : AreaOfSpecialisationForm(),
        'upcoming_events' : Event.objects.filter(sheduled_date__gte = datetime.today()),
        'user_current_projects' : ProjectParticipant.objects.filter(participant_name = request.user, project__project_end__gte = datetime.today()),
        'user_completed_projects' : ProjectParticipant.objects.filter(participant_name = request.user, project__project_end__lt = datetime.today()),
        'user_teams' : TeamMember.objects.filter(member_name = request.user)
    }
    for key, value in kwargs.items():
        context[key] = value
        
    return context