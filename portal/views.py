from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from django.contrib.auth.decorators import login_required
from django.forms import ModelForm
from django import forms
from .models import *
from .forms import *


# Login
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in  Test
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "portal/login.html", {
                "message": "Usuario e/ou senha inválida"
            })
    else:
        return render(request, "portal/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        numero = request.POST["numero"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "portal/registrar.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password, numero = numero)
            user.save()
        except IntegrityError:
            return render(request, "portal/registrar.html", {
                "message": "Nome de usuário já em uso"
            })
        login(request, user)
        return HttpResponseRedirect(reverse("editar_perfil"))
    else:
        return render(request, "portal/registrar.html")

#------

def index(request):
    return render(request, "portal/index.html", {
    })


def perfil(request, user_name):
    user_profile = User.objects.get(username=user_name)
    current_user = request.user
    editar_visivel = current_user.username == user_name

    return render(request, "portal/perfil.html", {
        'user_name': user_name,
        'numero': user_profile.numero,
        'descricao': user_profile.descricao,
        'editar_visivel': editar_visivel
    })

def editar_perfil(request, user_name):
    user_profile = User.objects.get(username=user_name)
    current_user = request.user
    if request.method == "POST":
        form = perfil_form(request.POST)
        if form.is_valid():
            numero = form.cleaned_data["numero"]
            descricao = form.cleaned_data["descricao"]
            user_profile.numero = numero
            user_profile.descricao = descricao
            user_profile.save()

        return HttpResponseRedirect(reverse('index'))
    else:  

        return render(request, "portal/editar_perfil.html", {
            'user_name': user_name,
            'numero': user_profile.numero,
            'descricao': user_profile.descricao,
            'perfil_form': perfil_form()
        })

def lista_categorias(request, grupo_id):
    return render(request, "portal/lista_categorias.html", {
        "grupo": Grupo.objects.get(id=grupo_id)
    })