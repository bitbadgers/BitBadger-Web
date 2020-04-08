from django import forms

class login(forms.Form):
    username = forms.EmailField()
    password = forms.CharField( widget= forms.PasswordInput)