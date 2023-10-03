from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.http import HttpResponseNotAllowed
from django.shortcuts import render, redirect

from .forms import CustomPasswordChangeForm, LoginForm, RegisterForm


def register(request):
    if request.method == 'GET':
        return render(request, 'register.html', {'form': RegisterForm()})
    elif request.method == 'POST':
        form = RegisterForm(request.POST)
        if not form.is_valid():
            messages.error(request, 'Popraw poniższe błędy:')
        elif User.objects.filter(email=form.cleaned_data['email']).exists():
            messages.error(request, 'Ten email jest już zajęty. Spróbuj ponownie.')
        else:
            try:
                user = User.objects.create_user(form.cleaned_data['username'], form.cleaned_data['email'],
                                                form.cleaned_data['password1'])
                messages.success(request, 'Użytkownik pomyślnie zarejestrowany.')
                return redirect('dashboard')
            except IntegrityError as e:
                messages.error(request, e)
        return render(request, 'register.html', {'form': form})
    else:
        return HttpResponseNotAllowed(permitted_methods=['GET', 'POST'])


def login_user(request):
    if request.method == 'GET':
        return render(request, 'login_user.html', {'form': LoginForm()})
    elif request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Błąd autentykacji.')
        else:
            messages.error(request, 'Popraw poniższe błędy.')
        return render(request, 'login_user.html', {'form': form})
    else:
        return HttpResponseNotAllowed(permitted_methods=['GET', 'POST'])


@login_required
def logout_user(request):
    logout(request)
    return redirect('home')


@login_required()
def change_password(request):
    if request.method == 'GET':
        form = CustomPasswordChangeForm(request.user)
        return render(request, 'change_password.html', {'form': form})
    elif request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            if form.cleaned_data['old_password'] != form.cleaned_data['new_password1']:
                user = form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Hasło zostało pomyślnie zaktualizowane.')
                return redirect('home')
            else:
                messages.error(request, 'Nowe hasło musi być różne od starego.')
        else:
            messages.error(request, 'Coś poszło nie tak. Popraw poniższe błędy.')
        return render(request, 'change_password.html', {'form': form})
    else:
        return HttpResponseNotAllowed(permitted_methods=['GET', 'POST'])
