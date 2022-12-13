from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.db.models import Q
from django.shortcuts import redirect

from django.contrib.auth.decorators import login_required
from django.forms import ModelForm
from django import forms
from .models import *
from .forms import *

from itertools import chain


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
                "message": "As senhas devem ser iguais."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password, numero = numero)
            user.save()
        except IntegrityError:
            return render(request, "portal/registrar.html", {
                "message": "Nome de usuário já em uso"
            })
        grupo_manamano = Grupo.objects.get(id=1)
        grupo_manamano.usuarios.add(user)
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
    publicacoes = Post.objects.filter(categoria__in=categorias).distinct().order_by('-importante','-data')
    #publicacoes = Post.objects.all().order_by('-importante','-data')
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
def editar_perfil(request):
    #user_profile = User.objects.get(username=user_name)
    current_user = request.user
    user_profile = current_user 
    if request.method == "POST":
        numero = request.POST["numero"]
        descricao = request.POST["descricao"]
        user_profile.numero = numero
        user_profile.descricao = descricao
        user_profile.save()

        return HttpResponseRedirect(reverse('index'))
    else:  

        return render(request, "portal/editar_perfil.html", {
            'user_name': current_user.username,
            'numero': user_profile.numero,
            'descricao': user_profile.descricao
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
    grupos = Grupo.objects.filter(Q(usuarios = current_user) | Q(admin = current_user) ).distinct()
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
    if request.method == 'POST':
        nome_usuario = request.POST["usuario"]
        usuario = User.objects.get(username = nome_usuario)
        if 'toggle_Admins' in request.POST:
            if usuario in grupo.admin.all():
                grupo.admin.remove(usuario)
                grupo.usuarios.add(usuario)
            else:
                grupo.admin.add(usuario)
                grupo.usuarios.remove(usuario)
        elif 'remover_do_grupo' in request.POST:
            grupo.admin.remove(usuario)
            grupo.usuarios.remove(usuario)
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
    novo_post = None
    if request.method == "POST":
        form = post_form(request.POST)
        print("Passou")
        if form.is_valid():
            print("Valido 1")
            titulo = form.cleaned_data["titulo"]
            publicacao = form.cleaned_data["texto"]
            print("Valido 2")
            autor = request.user
            novo_post = Post.objects.create(titulo = titulo, publicacao = publicacao, autor = autor )
            print("Passou")
        else:
            print(form.errors)
        if novo_post is not None:
            return redirect('escolher_grupo', post_id = novo_post.id)
        else:
            return redirect('index')
    else:

        return render(request, "portal/publicar.html", {
            'post_form': post_form()
        })

@login_required
def escolher_grupo(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.method == "POST":
        categoria_inputs = request.POST.getlist("categoria_inputs")
        for categoria_nome in categoria_inputs:
            categoria_selecionada = Categoria.objects.get(nome = categoria_nome)
            categoria_selecionada.posts.add(post)
        return HttpResponseRedirect(reverse('index'))
    else:
        current_user = request.user
        grupos = Grupo.objects.filter(Q(usuarios = current_user) | Q(admin = current_user) ).distinct()
        return render(request, 'portal/escolher_grupo.html', {
            'grupos': grupos,
            'post_id': post_id
        })


@login_required
def post(request, post_id):
    current_user = request.user
    post = Post.objects.get(id=post_id)
    if request.method == 'POST':
        if 'salvar' in request.POST:
            if post in current_user.salvos.all():
                # Deletar o post de salvos do usuário
                current_user.salvos.remove(post)
            else:
                # Adicionar o post em salvos do usuário
                current_user.salvos.add(post)
        else:
            post.importante = not post.importante
            post.save()
        
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

@login_required
def pesquisar(request, grupo_id):
    if grupo_id=="-1":
        print("entrei")
        termo = request.POST["termo"]
        grupos = Grupo.objects.filter(nome__contains=termo)
        usuarios = User.objects.filter(username__contains=termo)
        posts = Post.objects.filter(Q(titulo__contains=termo) | Q(publicacao__contains=termo)).order_by('-importante', '-data')
        return render(request, "portal/pesquisa.html", {
            'grupos': grupos,
            'usuarios': usuarios,
            'posts': posts,
            'pesquisa': termo
        })
    else:
        termo = request.POST["termo"]
        grupo = Grupo.objects.get(id=grupo_id)
        usuariosComuns = grupo.usuarios.all().filter(username__contains=termo)
        admins = grupo.admin.all().filter(username__contains=termo)
        usuarios = list(chain(usuariosComuns,admins))
        categorias = grupo.categorias.all()
        posts = Post.objects.filter(Q(Q(titulo__contains=termo) | Q(publicacao__contains=termo)) & Q(categoria__in = categorias)).order_by('-importante', '-data')
        return render(request, "portal/pesquisa.html", {
            'usuarios': usuarios,
            'posts': posts,
            'pesquisa': termo
        })

@login_required
def postsAutor(request,autor_id):
    posts = Post.objects.filter(autor=autor_id)
    return render(request, "portal/pesquisa.html", {
        'posts': posts,
    })

