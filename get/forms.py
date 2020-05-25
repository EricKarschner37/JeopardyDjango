from django import forms
from play.models import Game

class GameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ['num']
        labels = {'num': 'Game number'}
