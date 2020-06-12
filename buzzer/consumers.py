from channels.generic.websocket import WebsocketConsumer
from play.models import Game
from django.shortcuts import get_object_or_404
import pandas as pd
import json

game = None

"""
Messages are received as JSON strings.
Required:
    request=[request]
"""

def update_state():
    global game

    send_all(game.state.to_json())

def send_all(msg):
    global game

    players = game.state.players.copy()
    for name in players:
        if players[name]['conn']:
            players[name]['conn'].send(msg)
    if game.state.host:
        game.state.host.send(msg)
    if game.state.server:
        game.state.server.send(msg)
        print(game.state.name)
        print(game.state.clue)
        print(game.state.answer)

class BuzzerConsumer(WebsocketConsumer):
    name = "new player" 
    """
    Required:
        request='buzz'
    """
    def buzz(self): 
        global game

        if not game.state.can_buzz:
            return

        game.state.can_buzz = False
        game.state.name = "buzzed"
        game.state.selected_player = self.name

        update_state()

    """
    Required:
        request='register'
        name=[name]
    """
    def register(self, name):
        global game

        if not game:
            return

        name = name.strip()
        self.name = name

        balance = 0
        if name in game.state.players:
            balance = game.state.players[name]['balance']
        game.state.players[name] = {'balance': balance, 'conn': self}

        update_state()

    """
    Required:
        request='deregister'
    """
    def deregister(self):
        global game
        
#        del players[self.name]

    """
    Required:
        request='wager'
        amount=[amount]
    """
    def wager(self, amount):
        global game

        game.state.clue_shown = True
        game.state.name = "buzzed"
       

    """
    This function is called when a connection is established
    """
    def connect(self):
        self.accept()

    """
    This function is called when a message is received
    """
    def receive(self, text_data=None):
        try:
            data = json.loads(text_data or "")
        except:
            return

        if data['request'] == 'buzz':
            self.buzz()
        elif data['request'] == 'register':
            self.register(data['name'])
        elif data['request'] == 'wager':
            self.wager(data['amount'], data['row'], data['col'])

    """
    This function is called when a client disconnects
    """
    def disconnect(self, close_code):
        global game

        if game and self.name in game.state.players:
            game.state.players[self.name]['conn'] = None

class HostConsumer(WebsocketConsumer):
    """
    Requires:
        request='response'
        name=[name]
        correct=[True|False]
        question=[question]
            question.value=[value]
    """
    def playerResponse(self, correct):
        global game


        if game.state.selected_player in game.state.players:
            if correct:
                game.state.players[game.state.selected_player]['balance'] += game.state.cost
            else:
                game.state.players[game.state.selected_player]['balance'] -= game.state.cost

        game.state.selected_player = None

        # An update_state() call is made
        # in each of the function calls below,
        # and thus is not necessary here

        if correct:
            game.state.name = "question"
            self.closeBuzzers()
        else:
            game.state.name = "question"
            self.openBuzzers()

    """
    Requires:
        request='open'
    """
    def openBuzzers(self):
        global game

        game.state.can_buzz = True
        update_state()

    """
    Requires:
        request='close'
    """
    def closeBuzzers(self):
        global game

        game.state.can_buzz = False
        update_state()

    def playerChosen(self, name):
        global game

        if name in players:
            game.state.selected_player = name
            game.state.name = "wager"
            update_state()

    def connect(self):
        global game

        if game and game.state.host is None:
            game.state.host = self
            self.accept()
            self.send(game.state.to_json())

    def disconnect(self, close_code):
        global game

        if game:
            game.state.host = None

    def receive(self, text_data=None):

        try:
            data = json.loads(text_data)
        except:
            return

        if data['request'] == 'open':
            self.openBuzzers()
        if data['request'] == 'close':
            self.closeBuzzers()
        if data['request'] == 'response':
            self.playerResponse(data['correct'])
        if data['request'] == 'player_choice':
            self.playerChosen(data['name'])

class ServerConsumer(WebsocketConsumer):
    def connect(self):
        global game

        self.accept()

        if game:
            game.state.server = self

    def receive(self, text_data=None):
        global game

        try:
            data = json.loads(text_data)
        except:
            return

        if data['request'] == 'start_game':
            begin_game(data['game_num'], self)
        elif data['request'] == 'start_double':
            begin_double(data['game_num'])
        elif data['request'] == 'start_final':
            begin_final(data['category'], data['clue'], data['answer'])
        elif data['request'] == 'reveal':
            reveal(data['row'], data['col'])
        elif data['request'] == 'answer':
            game.state.name = 'answer'
            update_state()
        elif data['request'] == 'idle':
            game.state.name = 'idle'
            update_state()
        elif data['request'] == 'end':
            game.state.host = None
            game.state.server = None
            game.state.players = {}
            

def begin_game(game_id, server):
    global game

    game = get_object_or_404(Game, pk=game_id)
    game.state.server = server

    for name in game.state.players:
        if game.state.players[name]['conn']:
            game.state.players[name]['conn'].close()

    game.state.players = {}

    print(game.jeopardy_questions.columns.tolist())

    if game.state.server:
        game.state.server.send(json.dumps({'message': 'categories', 'categories': game.jeopardy_questions.columns.tolist()}))
        print(game.jeopardy_questions.columns.tolist())

    game.state.double = False

def begin_double(game_id):
    global game

    game = get_object_or_404(Game, pk=game_id)
    if game.state.server:
        game.state.server.send(json.dumps({'message': 'categories', 'categories': game.double_jeopardy_questions.columns.tolist()}))
        game.state.server.send(game.state.to_json())
    game.state.double = True

def begin_final(category, clue, answer):
    global game

    game.state.double = False
    game = Game()
    game.jeopardy_questions = pd.DataFrame([clue,])
    game.jeopardy_answers = pd.DataFrame([answer,])
    
def reveal(row, col):
    global game

    clue, answer = get_question(row, col)
    game.state.clue = clue
    game.state.answer = answer
    game.state.name = "question"

    if 'Double Jeopardy:' in clue:
        show_daily_double(row, col)
    elif game.state.double:
        game.state.cost = cost=(row+1)*400
    else:
        game.state.cost = cost=(row+1)*200

    print(game.state)
    update_state()

def get_question(row, col):
    global game

    if not game.state.double:
        clue = game.jeopardy_questions.values.tolist()[row][col]
        answer = game.jeopardy_answers.values.tolist()[row][col]
        return clue, answer
    elif game.state.double:
        clue = game.double_jeopardy_questions.values.tolist()[row][col]
        answer = game.double_jeopardy_answers.values.tolist()[row][col]
        return clue, answer

def show_daily_double(row, col):
    global game

    game.state.name = "daily_double"

    if game.state.host:
        game.state.host.send(json.dumps({'message': 'daily_double', 'players': [name for name in players], 'row': row, 'col': col}))

    if game.state.server:
        game.state.server.send(json.dumps({'message': 'daily_double'}))

