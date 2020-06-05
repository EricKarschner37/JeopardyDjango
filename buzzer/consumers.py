import json
from channels.generic.websocket import WebsocketConsumer
from play.models import Game
from django.shortcuts import get_object_or_404
import pandas as pd

connections = set()
host = None
server = None
can_buzz = False
players = {}
double = False
game = None

"""
Messages are received as JSON strings.
Required:
    request=[request]
"""

class BuzzerConsumer(WebsocketConsumer):
    name = "new player" 
    """
    Required:
        request='buzz'
    """
    def buzz(self): 
        global can_buzz
        global host
        global server

        if not can_buzz:
            self.send(json.dumps({'message': 'buzz', 'result': 'failed'}))
            return

        can_buzz = False
        self.send(json.dumps({'message': 'buzz', 'result': 'success'}))

        if host:
            host.send(json.dumps({'message': 'buzz', 'player': self.name}))
        if server:
            server.send(json.dumps({'message': 'buzz', 'name': self.name}))

    """
    Required:
        request='register'
        name=[name]
    """
    def register(self, name):
        global server
        global players

        name = name.strip()
        self.name = name

        balance = 0
        if name in players:
            balance = players[name]['balance']
        players[name] = {'balance': balance, 'conn': self}

        show_player(name)
        self.send(json.dumps({'message': 'unbuzz'}))

    """
    Required:
        request='deregister'
    """
    def deregister(self):
        global players
        
#        del players[self.name]

    """
    Required:
        request='wager'
        amount=[amount]
    """
    def wager(self, amount, row, col):
        global server
        global can_buzz
        global double
        global game

        clue, answer = get_question(row, col)
        show_question(clue, answer, amount)

        can_buzz = True
        self.buzz()
       

    def connect(self):
        global connections

        connections.add(self)
        self.accept()

    def receive(self, text_data=None):
        global can_buzz

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

    def disconnect(self, close_code):
        global players
        global connections

        if self in connections:
            connections.remove(self)

class HostConsumer(WebsocketConsumer):

    """
    Requires:
        request='response'
        name=[name]
        correct=[True|False]
        question=[question]
            question.value=[value]
    """
    def playerResponse(self, name, cost, correct):
        global players


        if name in players:
            if correct:
                players[name]['balance'] += cost
            else:
                players[name]['balance'] = max(players[name]['balance'] - cost, 0)

        show_player(name)
        self.unbuzzPlayer(name)
        if correct:
            self.closeBuzzers()
        else:
            self.openBuzzers()

    def unbuzzPlayer(self, name):
        global players
        global server

        if name in players:
            players[name]['conn'].send(json.dumps({'message': 'unbuzz'}))
        if server:
            server.send(json.dumps({'message': 'unbuzz', 'name': name}))

    """
    Requires:
        request='open'
    """
    def openBuzzers(self):
        global can_buzz

        can_buzz = True
        self.send(json.dumps({'message': 'open'}))

    """
    Requires:
        request='close'
    """
    def closeBuzzers(self):
        global can_buzz

        can_buzz = False
        self.send(json.dumps({'message': 'close'}))

    def playerChosen(self, name, row, col):
        global players

        if name in players:
            players[name]['conn'].send(json.dumps({'message': 'wager', 'row': row, 'col': col}))

    def connect(self):
        global host
        global connections

        host = self
        connections.add(self)
        self.accept()
        self.send(json.dumps({'message': 'close'}))

    def disconnect(self, close_code):
        global host
        global connections

        host = None
        if self in connections:
            connections.remove(self)

    def receive(self, text_data=None):
        global connections
        global can_buzz

        try:
            data = json.loads(text_data)
        except:
            return

        if data['request'] == 'open':
            self.openBuzzers()
        if data['request'] == 'close':
            self.closeBuzzers()
        if data['request'] == 'response':
            self.playerResponse(data['name'], data['cost'], data['correct'])
        if data['request'] == 'player_choice':
            self.playerChosen(data['name'], data['row'], data['col'])

class ServerConsumer(WebsocketConsumer):
    def connect(self):
        global server
        global players

        server = self
        self.accept()

        for name in players:
            show_player(name)

    def receive(self, text_data=None):
        global connections
        global host
        global server
        global players

        try:
            data = json.loads(text_data)
        except:
            return

        print(text_data)

        if data['request'] == 'start_game':
            begin_game(data['game_num'])
        elif data['request'] == 'start_double':
            begin_double(data['game_num'])
        elif data['request'] == 'start_final':
            begin_final(data['category'], data['clue'], data['answer'])
        elif data['request'] == 'reveal':
            reveal(data['row'], data['col'])
        elif data['request'] == 'end':
            for connection in connections:
                connection.send(json.dumps({'message': 'end'}))
            connections = set()
            host = None
            server = None
            players = {}
            

def begin_game(game_id):
    global connections
    global players
    global server
    global game
    global double

    for conn in connections:
        conn.close()

    connections = set()

    players = {}
    game = get_object_or_404(Game, pk=game_id)

    if server:
        print(game.jeopardy_questions.columns.tolist())
        server.send(json.dumps({'message': 'categories', 'categories': game.jeopardy_questions.columns.tolist()}))
    double = False

def begin_double(game_id):
    global game
    global server
    global double

    game = get_object_or_404(Game, pk=game_id)
    if server:
        server.send(json.dumps({'message': 'categories', 'categories': game.double_jeopardy_questions.columns.tolist()}))
    double = True

def begin_final(category, clue, answer):
    global players
    global game
    global double

    double = False
    game = Game()
    game.jeopardy_questions = pd.DataFrame([clue,])
    game.jeopardy_answers = pd.DataFrame([answer,])
    for name in players:
        players[name]['conn'].send(json.dumps({'message': 'wager', 'row': 0, 'col': 0}))
    
def reveal(row, col):
    global double
    global game

    clue, answer = get_question(row, col)
    if 'Double Jeopardy:' in clue:
        show_daily_double(row, col)
    elif double:
        show_question(clue, answer, cost=(row+1)*400)
    else:
        show_question(clue, answer, cost=(row+1)*200)

def get_question(row, col):
    if not double:
        clue = game.jeopardy_questions.values.tolist()[row][col]
        answer = game.jeopardy_answers.values.tolist()[row][col]
        return clue, answer
    elif double:
        clue = game.double_jeopardy_questions.values.tolist()[row][col]
        answer = game.double_jeopardy_answers.values.tolist()[row][col]
        return clue, answer

def show_question(clue, answer, cost):
    global connections
    global host
    global server

    for connection in connections:
        connection.send(json.dumps({'message': 'question', 'clue': clue, 'answer': answer, 'cost': cost}))
    if host:
        host.send(json.dumps({'message': 'question', 'clue': clue, 'answer': answer, 'cost': cost}))
    if server:
        server.send(json.dumps({'message': 'question', 'clue': clue, 'answer': answer, 'cost': cost}))

def show_daily_double(row, col):
    global host
    global players
    global server

    if host:
        host.send(json.dumps({'message': 'daily_double', 'players': [name for name in players], 'row': row, 'col': col}))

    if server:
        server.send(json.dumps({'message': 'daily_double'}))

def show_player(name):
    global server
    global players

    if server and name in players:
        balance = players[name]['balance']
        server.send(json.dumps({'message': 'player', 'name': name, 'balance': balance}))
