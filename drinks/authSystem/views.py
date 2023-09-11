from django.db import IntegrityError
from django.shortcuts import render
from .forms import RegisterForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseNotAllowed

def temp_home(request):
    return render(request, 'temp_home.html')

def register(request):
    if request.method == 'GET':
        return render(request,'register.html', {'form': RegisterForm()})
    elif request.method == 'POST':
        form = RegisterForm(request.POST)
        if not form.is_valid():
            error = form.errors
        #TODO: Remove email validation when user model has unique email and handle it in IntegrityError.
        elif User.objects.filter(email=form.cleaned_data['email']).exists():
            error = 'This email is already taken. Try again.'
        else:
            try:
                user = User.objects.create_user(form.username, form.email, form.password1)
                return render(request, 'temp_home.html')
            except IntegrityError as e:
                # if 'UNIQUE constraint failed: auth_user.email' in e.args:
                #     error = 'This user already exists.'
                # else:
                error = e
        return render(request, 'register.html', {'error': error, 'form': RegisterForm()})
    else:
        return HttpResponseNotAllowed(permitted_methods=['GET', 'POST'])


def login_user(request):
    if request.method == 'GET':
        return render(request, 'login_user.html', {'form': AuthenticationForm()})
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return render(request, 'temp_home.html')
        else:
            usernameExist = User.objects.filter(username=username).exists()
            if usernameExist:
                error = 'Incorrect password.'
            else:
                error = 'No such user in database.'
            return render(request, 'login_user.html', {'error': error, 'form': AuthenticationForm()})
    else:
        return HttpResponseNotAllowed(permitted_methods=['GET', 'POST'])


