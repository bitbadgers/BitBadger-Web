from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name = "index"),
    url(r'^register$', views.registeruser),
    url(r'^logout$', views.logoutUser, name = "logout")
]