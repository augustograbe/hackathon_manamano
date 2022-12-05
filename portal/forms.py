from django.forms import ModelForm
from django import forms

from .models import*

class perfil_form(forms.Form):
    numero = forms.CharField(label="whatsApp")
    descricao = forms.CharField(widget=forms.Textarea(attrs={'rows':'10', 'cols':'50'}))

class grupo_form(forms.Form):
    nome = forms.CharField(label="Nome do grupo")
    descricao = forms.CharField(label="Descrição do grupo")