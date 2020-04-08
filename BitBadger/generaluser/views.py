from django.shortcuts import render
from .loginform import login
from django.http import HttpResponse, HttpResponseRedirect
from loggeduser.models import UserDetails
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib import messages

def index(request):
    if request.method  == 'POST':
        form = AuthenticationForm(request, data = request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(username = username, password = password)
            print(user)
            if user is not None:
                login(request, user)
                messages.info(request, f"Logged in succesfully as {username} ")
                return HttpResponseRedirect('')
            else:
                messages.error(request, "Invalid login", fail_silently= False)
        else:
            messages.error(request, "Invalid login", fail_silently= False)
        
    loginform = AuthenticationForm()
    registerform = UserCreationForm()
    context = {
        'loginform' : loginform,
        'registrationform' : registerform,
    }
    return render(request, 'generaluser/index.html', context)
# Create your views here.
