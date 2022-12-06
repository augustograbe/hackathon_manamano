from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.db.models import Q

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

@login_required
def index(request):
    current_user = request.user
    grupos = Grupo.objects.filter(Q(usuarios = current_user) | Q(admin = current_user) ).distinct()
    categorias = Categoria.objects.filter(grupo__in=grupos).distinct()
    publicacoes = Post.objects.filter(categoria__in=categorias).distinct()
    #publicacoes = Post.objects.all()
    return render(request, "portal/index.html", {
        'publicacoes': publicacoes
    })

@login_required
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

@login_required
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

@login_required
def lista_categorias(request, grupo_id):
    grupo = Grupo.objects.get(id=grupo_id)
    return render(request, "portal/lista_categorias.html", {
        'grupo': grupo
    })

@login_required
def categoria(request, grupo_id, categoria_id):
    categoria = Categoria.objects.get(id=categoria_id)
    return render(request, "portal/categoria.html", {
        'categoria': categoria,
        'grupoid': grupo_id
    })

@login_required
def lista_grupos(request):
    current_user = request.user
    grupos = Grupo.objects.filter(Q(usuarios = current_user) | Q(admin = current_user) )
    return render(request, "portal/lista_grupos.html", {
        'usuario': current_user.username,
        'grupos': grupos
    })

@login_required
def grupo(request, grupo_id):
    grupo = Grupo.objects.get(id=grupo_id)
    categorias = grupo.categorias.all()
    posts = Post.objects.filter(categoria__in=categorias).distinct()
    return render(request, "portal/grupo.html", {
        'grupo': grupo,
        'posts': posts
    })

@login_required
def sobre(request, grupo_id):
    grupo = Grupo.objects.get(id=grupo_id)
    return render(request, "portal/sobre.html", {
        'grupo': grupo
    })

@login_required
def config_grupo(request, grupo_id):
    grupo = Grupo.objects.get(id=grupo_id)
    return render(request, "portal/config_grupo.html", {
        'grupo': grupo
    })

@login_required
def salvos(request):
    current_user = request.user
    posts = current_user.salvos
    return render(request, "portal/salvos.html", {
        'posts': posts
    })

@login_required
def publicar(request):
    return render(request, "portal/publicar.html", {
        
    })

@login_required
def post(request, post_id):
    post = Post.objects.get(id=post_id)
    return render(request, "portal/post.html", {
        'post': post
    })

@login_required
def criar_grupo(request):
    if request.method == "POST":
        form = grupo_form(request.POST)
        if form.is_valid():
            nome = form.cleaned_data["nome"]
            descricao = form.cleaned_data["descricao"]
            admin = request.user
            novo_grupo = Grupo.objects.create(nome = nome, descricao = descricao)
            novo_grupo.admin.add(admin)

        return HttpResponseRedirect(reverse('index'))
    else:  

        return render(request, "portal/criar_grupo.html", {
            'grupo_form': grupo_form()
        })

@login_required
def criar_categoria(request, grupo_id):
    grupo = Grupo.objects.get(id=grupo_id)
    if request.method == "POST":
        nome = request.POST["nome"]
        nova_categoria = Categoria.objects.create(nome = nome)
        grupo.categorias.add(nova_categoria)

        return HttpResponseRedirect(reverse('index'))
    else:  

        return render(request, "portal/criar_categoria.html", {
            'grupo': grupo
        })
