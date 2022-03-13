from django import forms

from .models import Episodio, Serie, Temporada


class SerieForm(forms.Form):
    nome = forms.CharField(label="Nome da Série", max_length=70)


class TemporadaForm(forms.ModelForm):
    class Meta:
        model = Temporada
        fields = ['numero', 'serie']
