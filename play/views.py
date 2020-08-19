from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views import generic
from .models import Game
from play import buzzer_server

import pandas as pd


class IndexView(generic.ListView):
    template_name = 'play/index.html'
    context_object_name = 'games_list'
    queryset = Game.objects.filter(played=False)


def game(request, game_num):
    return render(request, 'play/play.html', {'game_num': game_num})


def double(request, game_num):
    return render(request, 'play/play.html', {'game_num': game_num, 'double': True})


def final(request, game_num):
    game = get_object_or_404(Game, pk=game_num)
    game.played = True
    game.save()
    return render(request, 'play/final.html',
                  {'category': game.final_category, 'clue': game.final_clue, 'answer': game.final_answer})
