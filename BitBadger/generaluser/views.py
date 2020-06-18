from django.shortcuts import render, redirect
from .loginform import login
from django.http import HttpResponse, HttpResponseRedirect
# from loggeduser.models import UserDetails
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib import messages
from django.contrib import sessions

from DevsPlatform.models import FieldsOfSpecialisation

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
                # request.session['username'] = username
                request.session['context'] = {}
                messages.success(request, 'Successifully logged in!')
                return redirect('login-home')
            else:
                messages.error(request, "Invalid login!")
                return HttpResponseRedirect('')
        else:
            messages.error(request, "Invalid login!")
            return HttpResponseRedirect('')
    loginform = AuthenticationForm()
    registerform = UserCreationForm()
    context = {
        'loginform' : loginform,
        'registrationform' : registerform,
        'user' : request.session.get('username'),
        'fields_of_specialisation' : FieldsOfSpecialisation.objects.all(),
    }
    return render(request, 'generaluser/index.html', context)

def registeruser(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "User registration successful")
            return HttpResponseRedirect('')
        else:
            messages.error(request, "Password do not meet qualification")
            return HttpResponseRedirect('/')
    else:
        messages.error(request, "Password do not meet qualification")
        return HttpResponseRedirect('/')

