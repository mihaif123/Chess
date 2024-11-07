import pygame
from pieces import Pawn, Rook, Queen, Bishop, Knight, King
from methods import is_check
import sys
import threading
import socket

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 150, 0)
BLUE = (0, 0, 200)
RED = (255, 0, 0)
YELLOW = (255,255,0)
LIGHT_BROWN = (181,101,29)
SOFT_BLUE = (173, 216, 230)
BIRCH = (222,212,184)
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800
SQUARE_SIZE = 70
BOARD_X = 100
BOARD_Y = 70

dotimg = pygame.image.load("chessimgs\dot.png")

knightimg = pygame.image.load("chessimgs\LightKnight.png")
bishopimg = pygame.image.load("chessimgs\LightBishop.png")
pawnimg = pygame.image.load("chessimgs\LightPawn.png")
queenimg = pygame.image.load("chessimgs\LightQueen.png")
rookimg = pygame.image.load("chessimgs\LightRook.png")
kingimg = pygame.image.load("chessimgs\LightKing.png")

dknightimg = pygame.image.load("chessimgs\DarkKnight.png")
dbishopimg = pygame.image.load("chessimgs\DarkBishop.png")
dpawnimg = pygame.image.load("chessimgs\DarkPawn.png")
dqueenimg = pygame.image.load("chessimgs\DarkQueen.png")
drookimg = pygame.image.load("chessimgs\DarkRook.png")
dkingimg = pygame.image.load("chessimgs\DarkKing.png")

bishopimg_resized = pygame.transform.scale(bishopimg, (SQUARE_SIZE,SQUARE_SIZE))
knightimg_resized = pygame.transform.scale(knightimg, (SQUARE_SIZE,SQUARE_SIZE))
pawnimg_resized = pygame.transform.scale(pawnimg, (SQUARE_SIZE,SQUARE_SIZE))
queenimg_resized = pygame.transform.scale(queenimg,(SQUARE_SIZE,SQUARE_SIZE))
rookimg_resized = pygame.transform.scale(rookimg,(SQUARE_SIZE,SQUARE_SIZE))
raux = rookimg_resized
kingimg_resized = pygame.transform.scale(kingimg, (SQUARE_SIZE,SQUARE_SIZE))

dbishopimg_resized = pygame.transform.scale(dbishopimg, (SQUARE_SIZE,SQUARE_SIZE))
dknightimg_resized = pygame.transform.scale(dknightimg, (SQUARE_SIZE,SQUARE_SIZE))
dpawnimg_resized = pygame.transform.scale(dpawnimg, (SQUARE_SIZE,SQUARE_SIZE))
dqueenimg_resized = pygame.transform.scale(dqueenimg, (SQUARE_SIZE,SQUARE_SIZE))
drookimg_resized = pygame.transform.scale(drookimg, (SQUARE_SIZE,SQUARE_SIZE))
dkingimg_resized = pygame.transform.scale(dkingimg, (SQUARE_SIZE,SQUARE_SIZE))

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Board Game")


def mouse_square(board):
    mouse_pos = pygame.Vector2(pygame.mouse.get_pos()) - (BOARD_X,BOARD_Y)
    auxX = mouse_pos.x / SQUARE_SIZE
    auxY = mouse_pos.y / SQUARE_SIZE
    x = -1
    y = -1
    if(auxX > 0):
        x = int(auxX)
    if(auxY > 0):
        y = int(auxY)

    if( x < 0 or y < 0 or x > 7 or y > 7):
        return (None, None, None)
    return (board[x][y],x,y)

def check_whiteWin(darkKing,whiteKing,board,last_move):
    for i in range(8):
        for j in range(8):
            p = board[i][j]
            if p and p.getColor() != whiteKing.getColor():
                has, moves = p.has_legal_move(i,j,darkKing,whiteKing,board,last_move)
                if has:
                    return False
    return True

def check_darkWin(darkKing,whiteKing,board,last_move):
    for i in range(8):
        for j in range(8):
            p = board[i][j]
            if p and p.getColor() != darkKing.getColor():
                has, moves = p.has_legal_move(i,j,darkKing,whiteKing,board,last_move)
                if has:
                    return False
    return True

def check_endgame(darkKing,whiteKing,board,last_move):
    if check_darkWin(darkKing,whiteKing,board,last_move) and is_check(whiteKing,board):
        return 1
    elif check_whiteWin(darkKing,whiteKing,board,last_move)and is_check(darkKing,board):
        return 2
    elif check_darkWin(darkKing,whiteKing,board,last_move) and not is_check(whiteKing,board):
        return 3
    elif check_whiteWin(darkKing,whiteKing,board,last_move) and not is_check(darkKing,board):
        return 3
    return 4

def get_img(black, id):
    if id == 0:
        if black == True:
            return dkingimg_resized
        return kingimg_resized
    elif id == 1:
        if black == True:
            return dpawnimg_resized
        return pawnimg_resized
    elif id == 2:
        if black == True:
            return dbishopimg_resized
        return bishopimg_resized
    elif id == 3:
        if black == True:
            return dknightimg_resized
        return knightimg_resized
    elif id == 4:
        if black == True:
            return drookimg_resized
        return rookimg_resized
    elif id == 5:
        if black == True:
            return dqueenimg_resized
        return queenimg_resized


def move_from_server(board, xi,yi, xx, yy,last_move,darkKing,whiteKing):
    board[xi][yi].move(xi,yi,xx,yy,board,last_move,darkKing,whiteKing)



def start_board():

    board = [[None for _ in range(8)] for _ in range(8)]


    for i in range(8):
        board[i][6] = Pawn(False)

    board[4][6] = Pawn(False)


    board[1][7] = Knight(False)
    board[6][7] = Knight(False)
    board[7][7] = Rook(False)
    board[0][7] = Rook(False)
    board[2][7] = Bishop(False)
    board[5][7] = Bishop(False)
    board[3][7] = Queen(False)
    board[4][7] = King(4,7,False)

    for i in range(8):
        board[i][1] = Pawn(True)

    board[4][6] = Pawn(False)
    
    board[0][0] = Rook(True)
    board[1][0] = Knight(True)
    board[2][0] = Bishop(True)
    board[3][0] = Queen(True)
    board[4][0] = King(4,0,True)
    board[5][0] = Bishop(True)
    board[6][0] = Knight(True)
    board[7][0] = Rook(True)
    return board

promoted = False
def render_board(board, square_size,user, rating, player_color,opponent, opponent_rating,end_text,end_rect,end_code):
    global promoted
    screen.fill(BIRCH)


    hello_font = pygame.font.Font(None,30)

    pygame.draw.rect(screen,LIGHT_BROWN,((0,0),(WINDOW_WIDTH,50)))
    pygame.draw.rect(screen,LIGHT_BROWN,((0,WINDOW_HEIGHT - 50),(WINDOW_WIDTH,50)))
    hello_title = hello_font.render("Hello, ", True, BLACK)
    username_text = hello_font.render(user, True, BLACK)
    rating_title = hello_font.render("Rating: ", True, BLACK)
    rating_text = hello_font.render(str(rating), True,BLACK)

    opponent_title = hello_font.render("Opponent: ", True, BLACK)
    opponent_text = hello_font.render(opponent, True,BLACK)
    opponent_rating_text = hello_font.render(str(opponent_rating), True, BLACK)

    if player_color == True:
        screen.blit(hello_title,(10, 20,30,50))
        screen.blit(username_text,(80, 20, 40 , 50))
        screen.blit(rating_title, (670, 20, 40, 50))
        screen.blit(rating_text,(750, 20 , 40 , 50))

        screen.blit(opponent_title, (10, WINDOW_HEIGHT - 20, 30 ,50))
        screen.blit(opponent_text, (150, WINDOW_HEIGHT - 20 , 30, 50))
        screen.blit(rating_title , (670, WINDOW_HEIGHT - 20, 40 ,50))
        screen.blit(opponent_rating_text, (750, WINDOW_HEIGHT - 20, 40 , 50))
    else:
        screen.blit(hello_title,(10, WINDOW_HEIGHT - 20,30,50))
        screen.blit(username_text,(80, WINDOW_HEIGHT - 20, 40 , 50))
        screen.blit(rating_title, (670, WINDOW_HEIGHT - 20, 40, 50))
        screen.blit(rating_text,(750, WINDOW_HEIGHT - 20 , 40 , 50))
        
        screen.blit(opponent_title,(10, 20, 30 ,50))
        screen.blit(opponent_text, (150, 20, 30, 50))
        screen.blit(rating_title, (670, 20, 40, 50))
        screen.blit(opponent_rating_text,(750, 20 , 40 , 50))


    if promoted:
        promotion()

    alternate = True
    square_x = BOARD_X
    square_y = BOARD_Y

    for i in range(8):
        for j in range(4):
            if alternate == True :
                pygame.draw.rect(screen, LIGHT_BROWN, (square_x,square_y,square_size,square_size))
                square_x += square_size
                j = j + 1
                pygame.draw.rect(screen, SOFT_BLUE,(square_x,square_y,square_size,square_size))
                square_x += square_size
            else:
                pygame.draw.rect(screen, SOFT_BLUE, (square_x,square_y,square_size,square_size))
                square_x += square_size
                j = j + 1
                pygame.draw.rect(screen, LIGHT_BROWN,(square_x,square_y,square_size,square_size))
                square_x += square_size
        square_y += square_size
        square_x = BOARD_X
        alternate = not alternate

    square_x = BOARD_X
    square_y = BOARD_Y

    

    for i in range(8):
        for j in range(8):
            piece = board[i][j]
            if piece:
                black, id = piece.draw()
                img = get_img(black,id)
                image_rect = img.get_rect()
                (x, y) = (BOARD_X,BOARD_Y)
                image_rect.topleft = (x + i * square_size, y + j * square_size)
                screen.blit(img,image_rect)

    if end_code != 4:
        screen.blit(end_text,end_rect)
    


def credits(end_code,player_color,client):
    
    match end_code:
        case 1:
            if player_color:
                client.send("\nWIN".encode())
            else:
                client.send('\nLOSS'.encode())
        case 2:
            if not player_color:
                client.send('\nWIN'.encode())
            else:
                client.send('\nLOSS'.encode())
        case 3:
            client.send('\nDRAW'.encode())

def final_print(end_code,player_color):
    font = pygame.font.Font(None,74)
    if end_code == 1 and player_color:
        text = font.render("You Won!", True, WHITE)
    if end_code == 2 and not player_color:
        text = font.render("You Won!", True, WHITE)
    if end_code == 3:
        text = font.render("Draw!", True, WHITE)
    if end_code == 1 and not player_color:
        text = font.render("You Lost!", True, WHITE)
    if end_code == 2 and player_color:
        text = font.render("You Lost!", True, WHITE)       
    if end_code != 4:
        text_rect = text.get_rect(center = (BOARD_X + 4 * SQUARE_SIZE, BOARD_Y + 4 *SQUARE_SIZE))
        screen.blit(text,text_rect)
    
white_prom = False
black_prom = False

def promotion():
    global white_prom
    global black_prom
    PROM_X = WINDOW_WIDTH // 2 - 2 * SQUARE_SIZE
    PROM_Y = WINDOW_HEIGHT - 150

    rect1 = pygame.draw.rect(screen, YELLOW,(PROM_X, PROM_Y ,SQUARE_SIZE,SQUARE_SIZE))
    rect2 = pygame.draw.rect(screen, YELLOW,(PROM_X + SQUARE_SIZE ,PROM_Y,SQUARE_SIZE,SQUARE_SIZE))
    rect3 = pygame.draw.rect(screen, YELLOW,(PROM_X + 2 * SQUARE_SIZE,PROM_Y,SQUARE_SIZE,SQUARE_SIZE))
    rect4 = pygame.draw.rect(screen, YELLOW,(PROM_X + 3 * SQUARE_SIZE,PROM_Y,SQUARE_SIZE,SQUARE_SIZE))
    pygame.draw.rect(screen,(0,255,0,50),(PROM_X ,PROM_Y,SQUARE_SIZE,SQUARE_SIZE),2)
    pygame.draw.rect(screen,(0,255,0,50),(PROM_X + SQUARE_SIZE ,PROM_Y,SQUARE_SIZE,SQUARE_SIZE),2)
    pygame.draw.rect(screen,(0,255,0,50),(PROM_X + 2 * SQUARE_SIZE,PROM_Y,SQUARE_SIZE,SQUARE_SIZE),2)
    pygame.draw.rect(screen,(0,255,0,50),(PROM_X + 3 * SQUARE_SIZE,PROM_Y,SQUARE_SIZE,SQUARE_SIZE),2)
    if white_prom:
        screen.blit(queenimg_resized,rect1)
        screen.blit(rookimg_resized,rect2)
        screen.blit(knightimg_resized,rect3)
        screen.blit(bishopimg_resized,rect4)
    elif black_prom:
        screen.blit(dqueenimg_resized,rect1)
        screen.blit(drookimg_resized,rect2)
        screen.blit(dknightimg_resized,rect3)
        screen.blit(dbishopimg_resized,rect4)

def check_pawn2(player_color,board):
    for i in range(8):
        for j in range(8):
            p = board[i][j]
            if p:
                if isinstance(p,Pawn) and p.getColor() == player_color:
                    p.moved2 = False


last_move = (None, None, None, False)  
no_more_moves = threading.Event()
opponent_promotion = False
def check_move(client,board,darkKing,whiteKing,player_color):
    global last_move
    global white_turn
    global opponent_promotion
    while not no_more_moves.is_set():
        try:
            message = client.recv(1024).decode()
            if message.startswith("MOVE:"):
                parts = message.split(" ")
                white_turn = not white_turn
                print(message)
                move_from_server(board,int(parts[2]),int(parts[3]),int(parts[4]),int(parts[5]),last_move, darkKing,whiteKing)
            if message.startswith("PROMOTED"):
                opponent_promotion = False
                parts = message.split(' ')
                newx = int(parts[1])
                newy = 0
                if player_color == False:
                    newy = 7
                if parts[2] == 'Q':
                    board[newx][newy] = Queen(not player_color)
                if parts[2] == 'B':
                    board[newx][newy] = Bishop(not player_color)
                if parts[2] == 'R':
                    board[newx][newy] = Rook(not player_color)
                if parts[2] == 'N':
                    board[newx][newy] = Knight(not player_color)
            if message.startswith("PROMOTION:"):
                parts = message.split(" ")
                white_turn = not white_turn
                print(message)
                opponent_promotion = True
                move_from_server(board,int(parts[2]),int(parts[3]),int(parts[4]),int(parts[5]),last_move, darkKing,whiteKing)
        except BlockingIOError:
            pass
        except ConnectionAbortedError:
            print("server died :(")
            break
        except ConnectionResetError:
            print("server died :(")
            pass


promoted_x = None

def check_promotion(board):
    global white_prom
    global black_prom
    global promoted_x
    for i in range(8) :
        p = board[i][0]
        if p and isinstance(p,Pawn) and p.getColor() == False:
            white_prom = True
            promoted_x = i
            return True
        p2 = board[i][7]
        if p2 and isinstance(p,Pawn) and p2.getColor() == True:
            black_prom = True
            promoted_x = i
            return True




white_turn = True




def game_loop(client, player_color, user, rating,opponent, opponent_rating):

    global white_prom
    global black_prom
    global selected
    global selected_piece
    global white_turn
    global last_move
    global promoted
    global opponent_promotion
    global promoted_x

    print(f"STARTING AS {player_color}")
    pygame.init()

    if player_color == "BLACK": #BLACK = TRUE  | WHITE = FALSE
        player_color = True
    else:
        player_color = False

    client.setblocking(False)
    board = start_board()
    darkKing = board[4][0]
    whiteKing = board[4][7]
    clock = pygame.time.Clock()
    font = pygame.font.Font(None,74)
    end_text = font.render("Back",True, WHITE)
    end_rect = end_text.get_rect(center = (BOARD_X + 4 * SQUARE_SIZE, BOARD_Y + 5 * SQUARE_SIZE))
    white_prom = False
    black_prom = False
    running = True
    selected_piece = (None,None,None)
    selected = False
    PROM_X = WINDOW_WIDTH//2 - 2 * SQUARE_SIZE
    PROM_Y = WINDOW_HEIGHT - 150    
    end_code = 4
    move_thread = threading.Thread(target=check_move, args=(client,board,darkKing,whiteKing,player_color))
    move_thread.start()

    while running:
        
        mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
        if end_code != 4 and mouse_pos.x >= end_rect.x and mouse_pos.x <= end_rect.topright[0] and mouse_pos.y >= end_rect.y and mouse_pos.y <= end_rect.bottomleft[1]:
            pygame.draw.rect(screen,(0,255,0,0), (end_rect.x,end_rect.y,end_rect.topright[0] - end_rect.x,60),2)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                no_more_moves.set()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if end_code != 4:
                    running = False

                if promoted:
                    mouse_pos_x,mouse_pos_y = pygame.mouse.get_pos()
                    obj = None
                    if PROM_X < mouse_pos_x < PROM_X + SQUARE_SIZE and PROM_Y < mouse_pos_y < PROM_Y + SQUARE_SIZE:
                        #queen
                        if white_prom:
                            board[promoted_x][0] = Queen(False)
                        else:
                            board[promoted_x][7] = Queen(True)
                        obj = 'Q'
                    if PROM_X + SQUARE_SIZE < mouse_pos_x < PROM_X + 2 * SQUARE_SIZE and PROM_Y < mouse_pos_y < PROM_Y + SQUARE_SIZE:
                        #rook
                        if white_prom:
                            board[promoted_x][0] = Rook(False)
                        else:
                            board[promoted_x][7] = Rook(True)
                        obj = 'R'
                    if PROM_X + 2 * SQUARE_SIZE < mouse_pos_x < PROM_X + 3 * SQUARE_SIZE and PROM_Y < mouse_pos_y < PROM_Y + SQUARE_SIZE:
                        #knight
                        if white_prom:
                            board[promoted_x][0] = Knight(False)
                        else:
                            board[promoted_x][0] = Knight(True)
                        obj = 'N'
                    if PROM_X + 3 * SQUARE_SIZE < mouse_pos_x < PROM_X + 4 * SQUARE_SIZE and PROM_Y < mouse_pos_y < PROM_Y + SQUARE_SIZE:
                        #bishop
                        if white_prom:
                            board[promoted_x][0] = Bishop(False)
                        else:
                            board[promoted_x][7] = Bishop(True)
                        obj = 'B'
                    promoted = False
                    client.send(f"PROMOTED: {promoted_x} {obj}".encode())


                if not selected:
                    p = mouse_square(board)
                    if p[0]:
                        if (p[0].getColor() == (player_color)) and (player_color == (not white_turn)) and (not opponent_promotion):
                            selected = True
                            selected_piece = p
                else:#selected
                    p = mouse_square(board)
                    
                    if p[0]:

                        if (p[0].getColor() == (player_color)) and (player_color == (not white_turn)): 
                            selected_piece = True
                            selected_piece = p
                        else:
                            check_pawn2(player_color,board)
                            last_move = selected_piece[0].move(selected_piece[1],selected_piece[2],p[1],p[2],board,last_move,darkKing,whiteKing)
                            if last_move:
                                if last_move[3]:
                                    sending = f"MOVE: {selected_piece[0].getShortName()} {str(selected_piece[1])} {str(selected_piece[2])} {str(p[1])} {str(p[2])}"
                                    print(sending)
                                    promoted = check_promotion(board)
                                    if promoted:
                                        sending = f"PROMOTION: {selected_piece[0].getShortName()} {str(selected_piece[1])} {str(selected_piece[2])} {str(p[1])} {str(p[2])}"
                                    client.send(sending.encode())
                                    
                                    white_turn = not white_turn
                            selected = False
                            selected_piece = (None, None, None)
                    else:
                        check_pawn2(player_color,board)
                        last_move = selected_piece[0].move(selected_piece[1],selected_piece[2],p[1],p[2],board,last_move,darkKing,whiteKing)
                        if last_move:
                            if last_move[3]:
                                
                                sending = f"MOVE: {selected_piece[0].getShortName()} {str(selected_piece[1])} {str(selected_piece[2])} {str(p[1])} {str(p[2])}"
                                print(sending)
                                client.send(sending.encode())
                                
                                white_turn = not white_turn
                        selected = False
                        selected_piece = (None, None, None)
                    if(isinstance(last_move[0],Pawn) and last_move[0].getColor() == False and last_move[2] == 0):
                        white_prom = True
                    if(isinstance(last_move[0], Pawn) and last_move[0].getColor() == True and last_move[2] == 7):
                        black_prom = True

        render_board(board,SQUARE_SIZE, user, rating, player_color,opponent, opponent_rating,end_text,end_rect,end_code)

        piece, x , y = mouse_square(board)

        if(piece != None):
            select_rect = (BOARD_X + x * SQUARE_SIZE, BOARD_Y + y * SQUARE_SIZE, SQUARE_SIZE,SQUARE_SIZE)
            pygame.draw.rect(screen,(255, 0, 0 ,50), select_rect ,2)

        if(selected):
            select_rect = (BOARD_X + selected_piece[1] * SQUARE_SIZE, BOARD_Y + selected_piece[2] * SQUARE_SIZE,SQUARE_SIZE,SQUARE_SIZE)
            pygame.draw.rect(screen,(0,255,0,50),select_rect, 2)
            legal, moves = selected_piece[0].has_legal_move(selected_piece[1],selected_piece[2],darkKing,whiteKing,board,last_move)
            img = dotimg
            image_rect = img.get_rect()
            (x, y) = (BOARD_X, BOARD_Y)
            for move in moves:
                image_rect.topleft =(x + move[0] * SQUARE_SIZE, y + move[1] * SQUARE_SIZE)
                screen.blit(img,image_rect)
                
        end_code = check_endgame(darkKing,whiteKing,board,last_move)
        credits(end_code,player_color, client)
        final_print(end_code,player_color)
        pygame.display.flip()

        clock.tick(30)

    pygame.quit()
    sys.exit()
