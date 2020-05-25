import json

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
    state = State()


class State:
    name = "new"
    clue = ""
    answer = ""
    cost = 0
    clue_shown = False
    answer_shown = False

    # A player is simple represented as a dictionary,
    # keyed by player names (to facilitate rejoining),
    # holding two pieces of info:
    # balance (bal) and connection (conn)
    players = {}
    selected_player = None
    host = None
    server = None

    can_buzz = False
    double = False

    def to_json():
        json_dict = {
            'state': name,
            'clue': clue,
            'answer': answer,
            'clue_shown': clue_shown,
            'answer_shown': answer_shown
            'players': players
            'player': selected_player
        }

        return json.dumps(json_dict)
