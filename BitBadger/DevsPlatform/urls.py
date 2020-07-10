from django.urls import path
from . import views

app_name = 'DevsPlatform'

urlpatterns = [
    path("home/", views.Home, name = "login-home"),
    path("logout/", views.UserLogout, name = "logout"),
    
    path("User-Specialisation/<int:area_id>/leave", views.LeaveSpecialisation, name = "leave-specialisation"),
    
    path("team/join", views.JoinTeam, name = 'join_team'),
    path("team/create/", views.CreateTeam, name="create-team"),
    path("team/<int:team_id>/details/", views.TeamDetails, name = "view-team-details"),
    path("team/<int:team>/member/<int:user_id>/remove", views.RemoveTeamMember, name = "remove-team-member"),
    path("team/<int:team_id>/Member/Add", views.AddTeamMember, name = "add-team-member"),
    path("team/<int:team_id>/update/", views.AlterTeamDetails, name = "update-team-details"),
    
    path("project/<int:project_id>/details", views.ProjectDetails, name = "project-detail-view"),
    path("project/<int:project_id>/update", views.ProjectUpdate, name = "project-detail-update"),
    path("project/participant/<int:participant_id>/remove", views.RemoveParticipant, name = "project-remove-participant"),
    path("project/participant/<int:project_id>/add", views.JoinProject, name = "project-participant-add"),
    path("project/<int:project_id>participant/leave", views.RemoveParticipant, name = "project-participant-leave"),
    path("project/create/", views.CreateProject, name="create-project"),
    
    path("Dev-Tools/Minify", views.FileMinifier, name = "minify-file"),
    path("Dev-Tools/Minify/Download/<str:filename>/", views.download_file, name = "download-minified"),
]
