
import pygame
import sys
import sqlite3
import time
import socket
import threading

from chess import game_loop

pygame.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_BROWN = (181, 101, 29)
DARK_BROWN = (150, 85, 25)
BIRCH = (222, 212, 184)
LIGHT_BLUE = (173, 216, 230)
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800

font = pygame.font.Font(None, 74)
button_font = pygame.font.Font(None, 50)

button_width, button_height = 200, 60

register_button_rect = pygame.Rect((WINDOW_WIDTH//2 - button_width//2, 350), (button_width, button_height))
login_button_rect = pygame.Rect((WINDOW_WIDTH//2 - button_width//2, 250), (button_width, button_height))
quit_button_rect = pygame.Rect((WINDOW_WIDTH//2 - button_width//2, 450), (button_width, button_height))

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
logged = False




def draw_button(text, rect, is_hovered):
    color = DARK_BROWN if is_hovered else LIGHT_BROWN
    pygame.draw.rect(screen, color, rect)
    text_surf = button_font.render(text, True, WHITE)
    text_rect = text_surf.get_rect(center=rect.center)
    screen.blit(text_surf, text_rect)

def draw_text_input(color, input_box, FONT_COLOR, text):
    pygame.draw.rect(screen, color, input_box, 2)

    txt_surface = button_font.render(text, True, FONT_COLOR)

    pygame.draw.rect(screen, BIRCH, (input_box.x + 1, input_box.y + 1, input_box.width - 2, input_box.height - 2))
    screen.blit(txt_surface, (input_box.x + 5, input_box.y + 8))

def is_empty(str):
    return not str

def register_db(user,password):
    if is_empty(user) or is_empty(password):
        print("invalid username or password")
        return

    conn = sqlite3.connect('players.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS players (id INTEGER PRIMARY KEY, user TEXT, password TEXT, rating INT)')
    cursor.execute("SELECT id, user, password, rating FROM players WHERE user = ?", (user,  ))
    result = cursor.fetchone()

    print(result)
    if result:
        print("username already registered")
    else:
        cursor.execute('INSERT INTO players (user, password,rating) VALUES (?, ?, ? )', (user, password, 800))
        print("user sucessfully registered")

    conn.commit()
    cursor.close()
    conn.close()


def all_users():
    conn =sqlite3.connect('players.db')
    cursor = conn.cursor()
    cursor.execute('select * from players')

    result = cursor.fetchall()
    for row in result:
        print(row)

def register_menu():
    all_users()
    screen.fill(BIRCH)
    title_text = font.render("REGISTER", True, LIGHT_BROWN)
    username = button_font.render("Username: ", True, LIGHT_BROWN)
    password = button_font.render("Password: ", True, LIGHT_BROWN)
    register2_button_rect = pygame.Rect((WINDOW_WIDTH//2 - button_width//2, 400), (button_width,button_height))
    back_button_rect = pygame.Rect((WINDOW_WIDTH//2 - button_width //2, 500) , (button_width,button_height))
    
    screen.blit(title_text, (WINDOW_WIDTH//2 - title_text.get_width()//2, 100))
    screen.blit(username, (100, 200, 400 ,50))
    screen.blit(password, (100, 300, 400, 50))

    username_box = pygame.Rect(300,195,400,50)
    password_box = pygame.Rect(300,295, 400 ,50)

    color_inactive = BLACK
    color_active = LIGHT_BROWN
    register = True

    username_text = ''
    password_text = ''

    user_active = False
    password_active = False

    user_color = color_inactive
    password_color = color_inactive

    while register:
       
        mouse_pos = pygame.mouse.get_pos()
        draw_button("Register", register2_button_rect,register2_button_rect.collidepoint(mouse_pos))
        draw_button("Back" ,back_button_rect,back_button_rect.collidepoint(mouse_pos))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                register = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if username_box.collidepoint(event.pos):
                    user_active = True
                else:
                    user_active = False

                if password_box.collidepoint(event.pos):
                    password_active = True
                else:
                    password_active = False
                

                if register2_button_rect.collidepoint(event.pos):
                    register_db(username_text,password_text)

                if back_button_rect.collidepoint(mouse_pos):
                    main_menu()
                    register = False
                user_color = color_active if user_active else color_inactive
                password_color = color_active if password_active else color_inactive
            
            if event.type == pygame.KEYDOWN:
                if user_active or password_active:
                    if event.key == pygame.K_BACKSPACE:
                        if user_active:
                            username_text = username_text[:-1]
                        else:
                            password_text = password_text[:-1]
                    else:
                        if event.key != pygame.K_RETURN:
                            if user_active:
                                username_text += event.unicode
                            else:
                                password_text += event.unicode  


        draw_text_input(user_color, username_box,BLACK,username_text)
        draw_text_input(password_color, password_box,BLACK,password_text)
        pygame.display.flip()

def login_db(user,password):

    conn = sqlite3.connect('players.db')
    cursor = conn.cursor()

    cursor.execute("SELECT id, user, password,rating FROM players WHERE user = ?", (user,  ))
    result = cursor.fetchone()


    cursor.close()
    conn.close()
    if not result :
        return 0,-1 #account not found
    else:
        if result[2] == password:
            return 1,result[3]  # correct account
        else:
            return -1,-1 # wrong pass

queue_event = threading.Event()

def in_queue(client):
    global logged
    client.settimeout(1.0)
    while queue_event.is_set():
        try:
            message = client.recv(1024).decode()
            if message.startswith("START"):
                parts = message.split(" ")
                color = parts[1]
                logged = False
                client.send("STARTING".encode())
                queue_event.clear()
                #game_loop()
                print(f"game starts with {color}")
        except socket.timeout:
            pass

in_queue_thread = None

def logged_in(user,rating):
    global logged
    screen.fill(BIRCH)
    pygame.draw.rect(screen,LIGHT_BROWN,((0,0),(WINDOW_WIDTH,50)))

    find_match_button = pygame.Rect((WINDOW_WIDTH//2 - button_width//2, 100), (button_width,button_height))
    cancel_button = pygame.Rect((WINDOW_WIDTH//2 - button_width//2, 200), (button_width,button_height))

    hello_font = pygame.font.Font(None,30)

    hello_title = hello_font.render("Hello, ", True, BLACK)
    username_text = hello_font.render(user, True, BLACK)
    rating_title = hello_font.render("Rating: ", True, BLACK)
    rating_text = hello_font.render(str(rating), True,BLACK)
    time_elapsed_title = hello_font.render("Time elapsed: ", True, BLACK)

    screen.blit(hello_title,(10, 20,30,50))
    screen.blit(username_text,(80, 20, 40 , 50))
    screen.blit(rating_title, (670, 20, 40, 50))
    screen.blit(rating_text,(750, 20 , 40 , 50))

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1',9999))
    send_message = f"FIRST:{user} {str(rating)}"
    client.send(send_message.encode())
    message = client.recv(1024).decode()
    print(message)
    if(message.__eq__("cc")):
        logged = False
    else:
        logged = True
    finding_match = False
    start_time = 0
    while logged:
        if finding_match:
            pygame.draw.rect(screen,BIRCH,(740,60, 50,50))
            screen.blit(time_elapsed_title,(600,60, 50, 50))
            mins = int(int((time.time() - start_time))/60)
            seconds = int((time.time() - start_time)) % 60

            elapsed_time = str(mins) + ":" + str(seconds)
            elapsed_time_text = hello_font.render(elapsed_time, True,BLACK)
            screen.blit(elapsed_time_text,(740,60, 50, 50))

        mouse_pos = pygame.mouse.get_pos()
        draw_button("Find Match", find_match_button,find_match_button.collidepoint(mouse_pos))
        draw_button("Cancel" , cancel_button,cancel_button.collidepoint(mouse_pos))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if finding_match:
                    client.send("CANCEL".encode())
                client.send("QUIT".encode())
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if find_match_button.collidepoint(mouse_pos) and not finding_match:
                    
                    finding_match = True
                    start_time = time.time()
                    queue_event.set()

                    in_queue_thread = threading.Thread(target=in_queue,args= (client, ))
                    in_queue_thread.start()
                    
                    client.send("QUEUE".encode())
                

                if cancel_button.collidepoint(mouse_pos):
                    if(finding_match):
                        finding_match = False
                        queue_event.clear()
                        client.send('CANCEL'.encode())
                        pygame.draw.rect(screen,BIRCH,(600,60,200,50))                
                


        pygame.display.flip()
    
    if in_queue_thread is not None:
        in_queue_thread.join()




def login_menu():
    screen.fill(BIRCH)
    title_text = font.render("LOGIN", True, LIGHT_BROWN)
    username = button_font.render("Username: ", True, LIGHT_BROWN)
    password = button_font.render("Password: ", True, LIGHT_BROWN)
    screen.blit(title_text, (WINDOW_WIDTH//2 - title_text.get_width()//2, 100))
    screen.blit(username, (100, 200, 400 ,50))
    screen.blit(password, (100, 300, 400, 50))
    login2_button_rect = pygame.Rect((WINDOW_WIDTH//2 - button_width//2, 400), (button_width,button_height))
    back_button_rect = pygame.Rect((WINDOW_WIDTH//2 - button_width //2, 500) , (button_width,button_height))

    username_box = pygame.Rect(300,195,400,50)
    password_box = pygame.Rect(300,295, 400 ,50)

    color_inactive = BLACK
    color_active = LIGHT_BROWN

    username_text = ''
    password_text = ''

    user_active = False
    password_active = False

    user_color = color_inactive
    password_color = color_inactive

    login = True

    while login:
        mouse_pos = pygame.mouse.get_pos()
        draw_button("Login", login2_button_rect,login2_button_rect.collidepoint(mouse_pos))
        draw_button("Back" ,back_button_rect,back_button_rect.collidepoint(mouse_pos))
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    login = False
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if username_box.collidepoint(event.pos):
                        user_active = True
                    else:
                        user_active = False

                    if password_box.collidepoint(event.pos):
                        password_active = True
                    else:
                        password_active = False
                
                    if back_button_rect.collidepoint(mouse_pos):
                        login = False
                        main_menu()
                    
                    if login2_button_rect.collidepoint(mouse_pos):
                        fill_rect = pygame.Rect((WINDOW_WIDTH//2 - 250, 600), (500, 60))
                        pygame.draw.rect(screen,BIRCH,fill_rect)
                        
                        res_text = ' '
                        result,rating = login_db(username_text,password_text)
                        if result == -1 :
                            res_text = font.render("Wrong password!", True, LIGHT_BROWN)
                        elif result == 0 :
                            res_text = font.render("Account not found", True, LIGHT_BROWN)
                        elif result == 1:
                            res_text = font.render("Logging in",True, LIGHT_BROWN)
                            login = False
                            logged_in(username_text,rating)
                        screen.blit(res_text, (WINDOW_WIDTH//2 - res_text.get_width()//2, 600))


                    user_color = color_active if user_active else color_inactive
                    password_color = color_active if password_active else color_inactive

                if event.type == pygame.KEYDOWN:
                    if user_active or password_active:
                        if event.key == pygame.K_BACKSPACE:
                            if user_active:
                                username_text = username_text[:-1]
                            else:
                                password_text = password_text[:-1]
                        else:
                            if event.key != pygame.K_RETURN:
                                if user_active:
                                    username_text += event.unicode
                                else:
                                    password_text += event.unicode  
                
        draw_text_input(user_color, username_box,BLACK,username_text)
        draw_text_input(password_color, password_box,BLACK,password_text)
        pygame.display.flip()



            
def main_menu(): 

    menu = True

    while menu:
        screen.fill(BIRCH)  # Set background color for the menu

        mouse_pos = pygame.mouse.get_pos()


        # Display title
        title_text = font.render("Chess Game", True, LIGHT_BROWN)
        screen.blit(title_text, (WINDOW_WIDTH//2 - title_text.get_width()//2, 100))

        # Draw buttons
        draw_button("Login", login_button_rect, login_button_rect.collidepoint(mouse_pos))
        draw_button("Register", register_button_rect, register_button_rect.collidepoint(mouse_pos))
        draw_button("Quit", quit_button_rect, quit_button_rect.collidepoint(mouse_pos))

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                
                if register_button_rect.collidepoint(mouse_pos):
                    menu = False
                    register_menu()
                elif login_button_rect.collidepoint(mouse_pos):
                    menu = False
                    login_menu()
                elif quit_button_rect.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()

main_menu()

