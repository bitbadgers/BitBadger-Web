from django.urls import path
from . import views

urlpatterns = [
    path("Home/", views.Home, name = "login-home"),
    path("logout/", views.UserLogout, name = "logout"),
    path("create-project/", views.CreateProject, name="create-project"),
]
