from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    numero = models.CharField(max_length=10, unique=True)
    descricao = models.TextField(blank = True)
    salvos = models.ManyToManyField("Post", blank = True)
    #foto
    # ja tem username, password e email

class Post(models.Model):
    id = models.AutoField(primary_key=True)
    autor = models.ForeignKey(User, on_delete=models.PROTECT)
    titulo = models.CharField(max_length=100)
    data = models.DateTimeField(auto_now_add=True)
    publicacao = models.TextField()

class Categoria(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    posts = models.ManyToManyField(Post, blank = True)

class Grupo(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    categorias = models.ManyToManyField(Categoria, blank = True)
    usuarios = models.ManyToManyField(User, related_name='grupo_usuarios')
    admin = models.ManyToManyField(User, related_name='grupo_admin')
    #aberto = models.BooleanField(default=True)
    #codigo = 
    #foto 

