from django.forms import ModelForm
from django import forms

from .models import*

class perfil_form(forms.Form):
    numero = forms.CharField(label="Title")
    descricao = forms.CharField(widget=forms.Textarea(attrs={'rows':'10', 'cols':'50'}))