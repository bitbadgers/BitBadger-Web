from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages, sessions
from datetime import datetime, date
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.http import Http404,HttpResponse
import mimetypes
import os
from contextlib import contextmanager

from .models import *
from .Django_Html_Forms import *
from .dev_tools import MinifyFile

def Home(request):
    loged_user = request.user
    if loged_user.is_authenticated:
        if request.method == 'POST':
            form = AreaOfSpecialisationForm(request.POST)
            field = form.save(commit = False)
            field.user = loged_user
            try:
                field.save()
                messages.success(request, "The field has been added successfully")
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
            print("am in")
            if form.is_valid():
                try:
                    partial_saved = form.save( commit = False)
                    partial_saved.project_head = request.user
                    partial_saved.project_start = datetime.today()
                    partial_saved.save()
                    saved_project = Project.objects.get(project_name = form.cleaned_data.get("project_name"))
                    participant = ProjectParticipant(participant_name = request.user, project = saved_project)
                    participant.save()
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

def ProjectDetails(request, project_id):
    if request.user.is_authenticated:
        project_info = get_object_or_404(Project, pk = project_id)
        return render(request, "DevsPlatform/project_details.html", 
                      ContextBuilder(
                          request,
                          project_details = project_info,
                          project_participants = ProjectParticipant.objects.filter(project = project_id),
                          participant_add_form = AddToProjectForm()
                        ))
    else:
        return redirect('index')
    
def ProjectUpdate(request, project_id):
    if request.user.is_authenticated:
        project = get_object_or_404(Project, pk = project_id)
        if request.method == "POST":
            form = CreateProjectForm(request.POST, instance = project)
            if form.is_valid():
                if DateValidator(form.cleaned_data.get('project_end')):
                    try:
                        form.save()
                        messages.success(request, "The project's details have been updated successifully")
                    except Exception as e:
                        messages.error(request, e)
                else:
                    messages.error(request, "The completion date must be realistic i.e greater than today")
            
            return redirect(request.META['HTTP_REFERER'])
                
        else:
            return render(request, 'DevsPlatform/project_update.html', 
                          ContextBuilder(
                              request,
                              project_update_form = CreateProjectForm(instance = project),
                              project_id = project_id
                          )
                          )
    else:
        return redirect('index')
    
def JoinProject(request, project_id = None):
    if request.user.is_authenticated:
        if request.method == 'POST':
            if project_id:
                form = AddToProjectForm(request.POST)
                if form.is_valid():
                    form_save = form.save(commit = False)
                    project = get_object_or_404(Project, pk = project_id)
                    form_save.project = project
                    try:
                        form_save.save()
                    except Exception as e:
                        messages.error(request, e)
        if project_id:
            project = get_object_or_404(Project, pk = project_id)
            new_participant = ProjectParticipant(participant_name = request.user, project = project)
            
            try:
                if project.add_priviledge == 3: #3 for free join
                    new_participant.save()
                    messages.success(request,"Joined the project successifuly")
                else:
                    raise Http404("Not authorised to join the project")
            except Exception as e:
                messages.error(request, e)
            
        return redirect(request.META['HTTP_REFERER'])
    else:
        return redirect('index')

def RemoveParticipant(request, participant_id = None,project_id = None):
    if request.user.is_authenticated:
        if(participant_id != request.user and participant_id):
            participant = get_object_or_404(ProjectParticipant, pk  = participant_id)
            participant.delete()
            messages.success(request, "Participant removed successifully")
        else:
            project = get_object_or_404(Project, pk = project_id)
            if request.user != project.project_head:
                print("Yes")
                participant = get_object_or_404(ProjectParticipant, project = project, participant_name = request.user)
                try:
                    participant.delete()
                    messages.success(request, "You left")
                except Exception as e:
                    messages.error(request, e)
            else:
                raise Http_404("Error")
        
        return redirect(request.META['HTTP_REFERER'])    
    else:
        return redirect("index")

def JoinTeam(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = JoinTeamForm(request.POST)
            if form.is_valid():
                form_save = form.save(commit= False)
                form_save.member_name = request.user
                try:
                    form_save.save()
                    messages.success(request, "You successifuly registered to the team")
                except Exception as e:
                    messages.error(request, e)
            
            return redirect(request.META['HTTP_REFERER'])
        else:
            return redirect('login-home')
    else:
        return redirect('index')
    
def CreateTeam(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = CreateTeamForm(request.POST)
            if form.is_valid():
                form_save = form.save(commit=False)                
                form_save.date_of_creation = datetime.today()
                form_save.creator = request.user
                
                try:
                    form_save.save()
                    team_name = form.cleaned_data['team_name']
                    
                    team_obj = Team.objects.get(team_name = team_name)
                    user_team = TeamMember(team = team_obj, member_name = request.user, member_role = 'Chair')
                    user_team.save()
                    messages.success(request, "team added successifuly")
                except Exception as e:
                    print(e)
                    messages.success(request, e)
                    
            return render(request, 'DevsPlatform/create_team.html', ContextBuilder(request, create_team_form = form ))
        
        else:
            return render(request, 'DevsPlatform/create_team.html', ContextBuilder(request, create_team_form = CreateTeamForm() ))
    else:
        return redirect('index')

def TeamDetails(request, team_id = None):
    if request.user.is_authenticated:
        if request.method == "POST":
            pass
        else:
            if team_id:
                member_team = get_object_or_404(TeamMember,member_name = request.user, team = team_id)
                members = TeamMember.objects.filter(team = team_id)
                return render(request, 'DevsPlatform/teams_details.html', 
                              ContextBuilder(
                                  request, team_details = member_team,
                                  member_list = members,
                                  add_team_member_form = AddTeamMemberForm()
                                )
                            )
            else:
                pass
    else:
        return redirect('index')

def AddTeamMember(request, team_id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = AddTeamMemberForm(request.POST)
            if form.is_valid():
                form_save = form.save(commit = False)
                try:
                    form_save.team = Team.objects.get(pk = team_id)
                    form_save.save()
                except Exception as e:
                    messages.error(request, e)
            return redirect(request.META['HTTP_REFERER'])
    else:
        return redirect('index')

def RemoveTeamMember(request, user_id, team):
    if request.user.is_authenticated:
        member = TeamMember.objects.filter(member_name = request.user, team = team)
        if user_id != request.user.id or (user_id == request.user.id and member[0].member_role != 'Chair'):
            if member:
                member_role = member[0].member_role
                if member_role == 'Chair' or (user_id == request.user.id and member[0].member_role != 'Chair'):
                    TeamMember.objects.get(member_name = user_id, team = team).delete()
                if user_id == request.user.id and member[0].member_role != 'Chair':
                    messages.success(request, "Left the team successifully")
                    return redirect('DevsPlatform:login-home')
        return redirect(request.META['HTTP_REFERER'])
    else:
        return redirect('index')
    
def AlterTeamDetails(request, team_id = None):
    if request.user.is_authenticated:
        team = get_object_or_404(Team, pk = team_id)
        if request.method == 'POST':
            form = CreateTeamForm(request.POST, instance = team)
            if form.is_valid():
                form.save()
                messages.success(request, "Details updated successfuly")
            return redirect(request.META['HTTP_REFERER'])
        else:
            team_update_form = CreateTeamForm(instance = team)
            return render(request, 'DevsPlatform/update_team.html', 
                          ContextBuilder(request,
                                            update_team_form = team_update_form,
                                            team_id = team_id
                                         )
                          )
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
        'user_teams' : TeamMember.objects.filter(member_name = request.user),
        'join_team_form' : JoinTeamForm(),
        'projects' : Project.objects.filter(project_end__gte = datetime.today()),
    }
    for key, value in kwargs.items():
        context[key] = value
        
    return context

def LeaveSpecialisation(request, area_id):
    if request.user.is_authenticated:
        area = get_object_or_404(FieldsOfSpecialisation, pk = area_id)
        user_specialisation = get_object_or_404(UserSpecialisation, user = request.user , Area_Of_Specialisation = area)
        try:
            user_specialisation.delete()
        except Exception as e:
            messages.error(request, e)
        
        return redirect(request.META['HTTP_REFERER'])
    else:
        return redirect('index')

def FileMinifier(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = MinifyForm(request.POST, request.FILES)
            if form.is_valid():
                if request.FILES:
                    file = request.FILES['file']
                else:
                    messages.error(request, "Please upload a file")
                    return redirect(request.META['HTTP_REFERER'])
                
                minify_obj = MinifyFile(file)
                path = minify_obj.Minify()
                return render(request, "DevsPlatform/minify_tools.html",
                              ContextBuilder(
                                  request,
                                  filename = str(path['filename']),
                                  upload_minify_form = MinifyForm(initial = {
                                    'file' : file  
                                  })
                              ))
            
            return redirect(request.META['HTTP_REFERER'])
        else:
            return render(request, "DevsPlatform/minify_tools.html", 
                          ContextBuilder(
                              request,
                              upload_minify_form = MinifyForm()
                          )
                          )
    else:
        return redirect('index')


def download_file(request,filename):
    fl = open(filename)
    mime_type, _ = mimetypes.guess_type(filename)
    response = HttpResponse(fl, content_type=mime_type)
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    return response

def DateValidator(testing_date):
    #This funcion ensures that the date selected is not less than today
    if testing_date >= date.today():
        return True
    else:
        return False

