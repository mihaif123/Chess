import socket
import threading
import sqlite3
import select
import random

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('0.0.0.0', 9999))

server.listen(5)

queue_active = False
users_queue = []
clients = {}
stop_event = threading.Event()
cancel_event = threading.Event()

def input_thread():
    while not stop_event.is_set():
        user_input = input(">")
        if user_input.lower() == "exit":
            stop_event.set()
            game_event.set()
            server.close()
        if user_input.lower() == "showq":
            print("Users_queue:", users_queue)
        if user_input.lower() == "showc":
            print("Clients: ", clients)
        if user_input.lower() == "showdb":
            showdb()
        if user_input.lower().startswith("setrating"):
            parts = user_input.split(" ")
            set_rating(parts[1], parts[2])

input_listener = threading.Thread(target=input_thread)
input_listener.start()
inqueue_listener = None

def set_rating(user,rating):
    conn = sqlite3.connect('players.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE players SET rating = ? WHERE user = ?', (rating,user))
    conn.commit()
    cursor.close()
    conn.close()

def showdb():
    conn = sqlite3.connect('players.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM players')
    result = cursor.fetchall()
    for row in result:
        print(row)
    cursor.close()
    conn.close()

def is_empty(myList):
    return len(myList) == 0

game_event = threading.Event()

def game(player1,player2):

    socket_obj1, (user1, rating1, player1addr) = player1
    socket_obj2, (user2, rating2, player2addr) = player2

    socket_obj1.setblocking(False)
    socket_obj2.setblocking(False)
    while not game_event.is_set():
        #print("reading")
        try:
            message1 = socket_obj1.recv(1024).decode()
            messages = message1.split("\n")
            for msg in messages:
                if msg.startswith('WIN'):
                    set_rating(player1[1][0],int(player1[1][1]) + 8)
                    set_rating(player2[1][0],int(player2[1][1]) - 8)
                    break
                elif msg.startswith('DRAW'):
                    break
                elif msg.startswith('LOSS'):
                    break
                else:
                    socket_obj2.send(msg.encode())
                    socket_obj1.send('message received'.encode())
        except BlockingIOError:
            pass
        except ConnectionAbortedError:
            print("broke connection1")
            del clients[socket_obj1]
            del clients[socket_obj2]
            break
        except ConnectionResetError:
            print("broke connection2")
            del clients[socket_obj1]
            del clients[socket_obj2]
            break
        try:
            message2 = socket_obj2.recv(1024).decode()
            messages = message2.split("\n")
            for msg in messages:
                if msg.startswith('WIN'):
                    set_rating(player2[1][0],int(player2[1][1]) + 8)
                    set_rating(player1[1][0],int(player1[1][1]) - 8)
                    break
                elif msg.startswith('DRAW'):
                    break
                elif msg.startswith('LOSS'):
                    break
                else:
                    socket_obj1.send(msg.encode())
                    socket_obj2.send('message received'.encode())
        except BlockingIOError:
            pass
        except ConnectionAbortedError:
            print("broke connection1")
            del clients[socket_obj1]
            del clients[socket_obj2]
            break
        except ConnectionResetError:
            print("broke connection2")
            del clients[socket_obj1]
            del clients[socket_obj2]
            break
def in_queue():
    global queue_active
    global users_queue
    while not stop_event.is_set():
        
        if(len(users_queue) == 0):
            queue_active = False
            continue
        if(len(users_queue) == 1):
            continue
        for user in users_queue:
            for user2 in users_queue:
                if user != user2 and abs(int(user[1]) - int(user2[1])) < 10:
                    
                    users_queue.remove(user)
                    users_queue.remove(user2)


                    players = []
                    for client in clients:
                        if (clients[client][0],clients[client][1]) == (user[0],user[1]) or (clients[client][0],clients[client][1]) == (user2[0],user2[1]):
                            players.append((client, clients[client]))

                    player1 = players[0]
                    player2 = players[1]

                    options = ["BLACK", "WHITE"]
                    random_choice = random.choice(options)

                    other = "BLACK"
                    if random_choice == "BLACK":
                        other = "WHITE"

                    player1[0].sendto(f"START {random_choice} {player2[1][0]} {player2[1][1]}".encode(),player1[1][2])
                    player2[0].sendto(f"START {other} {player1[1][0]} {player1[1][1]}".encode(),player2[1][2])

                    game_thread = threading.Thread(target=game, args=(player1,player2))
                    game_thread.start()
                            
inqueue_listener = threading.Thread(target=in_queue)
inqueue_listener.start()
            
def handle_buttons(client):
    global queue_active
    
    while not stop_event.is_set():

        msg = ' '
        client.settimeout(1.0)
        try:
            msg = client.recv(1024).decode()
        except socket.timeout:
            pass
        except ConnectionAbortedError:
            users_queue.remove(clients[client])
        except ConnectionResetError:
            users_queue.remove(clients[client])

        if msg.startswith("QUEUE"):
            print(f"{clients[client][0]} is now in queue...")
            users_queue.append(clients[client])
            if not queue_active:
                queue_active = True
                
        elif msg.startswith("CANCEL"):
            users_queue.remove(clients[client])
        elif msg.startswith("QUIT"):
            users_queue.remove(clients[client])
            del clients[client]
        elif msg.startswith("STARTING"):
            break



def handle_client(client,addr):

    message = client.recv(1024).decode()

    if message.startswith("FIRST:"):
        parts = message.split(":")
        ur = parts[1].split(" ")
        user = ur[0]
        rating = ur[1]
    
        values = clients.values()

        values = list(values)

        for value in values:
            if user in value[0]:
                client.sendto("cc".encode(),addr)
                return
        
        client.sendto("loggedin".encode(),addr)
        clients[client] = (user,rating,addr)

    handle_thread = threading.Thread(target=handle_buttons, args=(client,))
    handle_thread.start()



def main_server():
    while not stop_event.is_set():
        try:          
            client,addr = server.accept()

            handle_client_thread = threading.Thread(target=handle_client,args=(client,addr))
            handle_client_thread.start()

        except OSError:
            pass


main_server()
