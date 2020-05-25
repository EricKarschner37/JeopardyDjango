from websocket_server import WebsocketServer
import threading
import sys

can_buzz = False
lock = threading.Lock()
connections = {}
host = None

def accept_connection(client, server):
    global connections
    print("New connection!")

    connections[client['id']] = client

def handle_message(client, server, message):
    global can_buzz
    global lock
    global connections
    global host

    tokens = message.split(" ")
    if tokens[0] == 'ANSWER':
        server.send_message(host, message)
        return
    print('Received: ' + message)
    if tokens[0] == 'CLUE':
        server.send_message(host, message)
        for client_id in connections:
            server.send_message(connections[client_id], message)
    if tokens[0] == 'HOST':
        connections[client['id']]['type'] = 'host'
        host = connections[client['id']]
    if tokens[0] == 'PLAYER':
        connections[client['id']]['type'] = 'player'
        connections[client['id']]['name'] = message[7:]
    if tokens[0] == 'SERVER':
        connections[client['id']]['type'] = 'server'
    lock.acquire()
    try:
        if tokens[0] == 'OPEN' and connections[client['id']]['type'] == 'host':
            can_buzz = True
        if tokens[0] == 'BUZZ' and can_buzz:
            can_buzz = False
            server.send_message(host, 'BUZZ ' + connections[client['id']]['name'])
            server.send_message(client, 'BUZZ SUCCESS')
        if tokens[0] == 'CLOSE':
            can_buzz = False
            for client_id in connections:
                server.send_message(connections[client_id], 'CLOSE')
    except:
        print("Error!")
    finally:
        lock.release()

def remove_connection(client, server):
    print("Removing connection: " + connections[client['id']]['type'])
    del connections[client['id']]

def start_server():
    server = WebsocketServer(10001, host='0.0.0.0')
    server.set_fn_new_client(accept_connection) 
    server.set_fn_message_received(handle_message)
    server.set_fn_client_left(remove_connection)
    thread = threading.Thread(target=server.run_forever)
    thread.start()

if __name__ == '__main__':
    start_server()
