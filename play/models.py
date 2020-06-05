import json
from django.db import models
from picklefield import fields

class Game(models.Model):
    num = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=150)
    played = models.BooleanField(default=False)
    jeopardy_questions = fields.PickledObjectField()
    jeopardy_answers = fields.PickledObjectField()
    double_jeopardy_questions = fields.PickledObjectField()
    double_jeopardy_answers = fields.PickledObjectField()
    final_category = models.CharField(max_length=250)
    final_clue = models.CharField(max_length=500)
    final_answer = models.CharField(max_length=500)

