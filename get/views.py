from get.forms import GameForm
from django.shortcuts import render
from django.views import generic
from django.core.files import File
import pandas as pd

from get import get_game
class GetView(generic.edit.FormView):
    template_name = 'get/get.html'
    form_class = GameForm
    success_url = '/host/'
    
    def form_valid(self, form):
        game = form.save(commit=False)
        game.name = get_game.get_from_url("http://www.j-archive.com/showgame.php?game_id=" + str(game.num))
        game.jeopardy_questions = pd.read_csv('/tmp/' + str(game.num) + '_jeopardy_game.csv')
        game.jeopardy_answers = pd.read_csv('/tmp/' + str(game.num) + '_jeopardy_game_answers.csv')
        game.double_jeopardy_questions = pd.read_csv('/tmp/' + str(game.num) + '_double_jeopardy_game.csv')
        game.double_jeopardy_answers = pd.read_csv('/tmp/' + str(game.num) + '_double_jeopardy_game_answers.csv')
        with open('/tmp/' + str(game.num) + "_final_jeopardy.txt", 'r') as f:
            s = f.read().split("\n")
            game.final_category = s[0]
            game.final_clue = s[1]
            game.final_answer = s[2]

        game.save()

        return super().form_valid(form)   
