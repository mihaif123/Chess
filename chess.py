import pygame
from pieces import Pawn, Rook, Queen, Bishop, Knight, King
from methods import is_check

import sys


# Initialize Pygame
pygame.init()

# Define constants
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 150, 0)
BLUE = (0, 0, 200)
RED = (255, 0, 0)
YELLOW = (255,255,0)
LIGHT_BROWN = (181,101,29)
BIRCH = (222,212,184)
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800
SQUARE_SIZE = 70
BOARD_X = 100
BOARD_Y = 50

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

# Create the game window
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

    #print((x,y))

    #print(board)
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
        print("Dark Won!")
        return 1
    elif check_whiteWin(darkKing,whiteKing,board,last_move)and is_check(darkKing,board):
        print("White Won!")
        return 2
    elif check_darkWin(darkKing,whiteKing,board,last_move) and not is_check(whiteKing,board):
        print("Stalemate!")
        return 3
    elif check_whiteWin(darkKing,whiteKing,board,last_move) and not is_check(darkKing,board):
        print("Stalemate!")
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



# Game loop
def game_loop():
    clock = pygame.time.Clock()
    running = True
    ok = True
    last_move = (None, None, None, False)

    square_x = BOARD_X
    square_y = BOARD_Y
    square_size = SQUARE_SIZE
    
            
    #Starting Board

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

    darkKing = board[4][0]
    whiteKing = board[4][7]


    selected_piece = (None,None,None)
    selected = False
    white_turn = True
    white_prom = False
    black_prom = False
    event = None

    
    while running:
        # Fill the background with white each frame
        screen.fill(WHITE)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False  # Set running to False to exit the loop

        # Update the display
        alternate = True

        for i in range(8):
            for j in range(4):
                if alternate == True :
                    pygame.draw.rect(screen, LIGHT_BROWN, (square_x,square_y,square_size,square_size))
                    square_x += square_size
                    j = j + 1
                    pygame.draw.rect(screen, BIRCH,(square_x,square_y,square_size,square_size))
                    square_x += square_size
                else:
                    pygame.draw.rect(screen, BIRCH, (square_x,square_y,square_size,square_size))
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
        
       
        piece, x , y = mouse_square(board)

        #print(piece)
        if(piece != None):
            select_rect = (BOARD_X + x * square_size, BOARD_Y + y * square_size, square_size,square_size)
            pygame.draw.rect(screen,(255, 0, 0 ,50), select_rect ,2)

        if(selected):
            select_rect = (BOARD_X + selected_piece[1] * square_size, BOARD_Y + selected_piece[2] * square_size,square_size,square_size)
            pygame.draw.rect(screen,(0,255,0,50),select_rect, 2)
            legal, moves = selected_piece[0].has_legal_move(selected_piece[1],selected_piece[2],darkKing,whiteKing,board,last_move)
            img = dotimg
            image_rect = img.get_rect()
            (x, y) = (BOARD_X, BOARD_Y)
            for move in moves:
                image_rect.topleft =(x + move[0] * square_size, y + move[1] * square_size)
                screen.blit(img,image_rect)
                



        
        if event and event.type == pygame.MOUSEBUTTONUP:
            ok = True

            
        if white_prom == True or black_prom == True:
            if white_prom == True :
                clr = False
            else:
                clr = True
            rect1 = pygame.draw.rect(screen, YELLOW,(BOARD_X ,BOARD_Y + 9 * SQUARE_SIZE,SQUARE_SIZE,SQUARE_SIZE))
            rect2 = pygame.draw.rect(screen, YELLOW,(BOARD_X + SQUARE_SIZE ,BOARD_Y + 9 * SQUARE_SIZE,SQUARE_SIZE,SQUARE_SIZE))
            rect3 = pygame.draw.rect(screen, YELLOW,(BOARD_X + 2 * SQUARE_SIZE, BOARD_Y + 9 * SQUARE_SIZE,SQUARE_SIZE,SQUARE_SIZE))
            rect4 = pygame.draw.rect(screen, YELLOW,(BOARD_X + 3 * SQUARE_SIZE,BOARD_Y + 9 * SQUARE_SIZE,SQUARE_SIZE,SQUARE_SIZE))
            pygame.draw.rect(screen,(0,255,0,50),(BOARD_X ,BOARD_Y + 9 * SQUARE_SIZE,SQUARE_SIZE,SQUARE_SIZE),2)
            pygame.draw.rect(screen,(0,255,0,50),(BOARD_X + SQUARE_SIZE ,BOARD_Y + 9 * SQUARE_SIZE,SQUARE_SIZE,SQUARE_SIZE),2)
            pygame.draw.rect(screen,(0,255,0,50),(BOARD_X + 2 * SQUARE_SIZE, BOARD_Y + 9 * SQUARE_SIZE,SQUARE_SIZE,SQUARE_SIZE),2)
            pygame.draw.rect(screen,(0,255,0,50),(BOARD_X + 3 * SQUARE_SIZE,BOARD_Y + 9 * SQUARE_SIZE,SQUARE_SIZE,SQUARE_SIZE),2)
            if white_prom:
                screen.blit(queenimg_resized,rect1)
                screen.blit(rookimg_resized,rect2)
                screen.blit(knightimg_resized,rect3)
                screen.blit(bishopimg_resized,rect4)
            else:
                screen.blit(dqueenimg_resized,rect1)
                screen.blit(drookimg_resized,rect2)
                screen.blit(dknightimg_resized,rect3)
                screen.blit(dbishopimg_resized,rect4)
            mouse_pos = pygame.Vector2(pygame.mouse.get_pos()) - (BOARD_X,BOARD_Y)
            
            if(mouse_pos.y >= 9 * square_size and mouse_pos.y <= 10 * square_size and event.type == pygame.MOUSEBUTTONDOWN):
                if mouse_pos.x >= 0 and mouse_pos.x <= square_size:
                    board[last_move[1]][last_move[2]] = Queen(clr)
                    white_prom = False
                    black_prom = False
                elif mouse_pos.x >= square_size and mouse_pos.x <= 2*square_size:
                    board[last_move[1]][last_move[2]] = Rook(clr)
                    white_prom = False
                    black_prom = False
                elif mouse_pos.x >= 2*square_size and mouse_pos.x <= 3*square_size:
                    board[last_move[1]][last_move[2]] = Knight(clr)
                    white_prom = False
                    black_prom = False
                elif mouse_pos.x >= 3*square_size and mouse_pos.x <= 4*square_size:
                    board[last_move[1]][last_move[2]] = Bishop(clr)
                    white_prom = False
                    black_prom = False
        
        
        end_code = check_endgame(darkKing,whiteKing,board,last_move)

        font = pygame.font.Font(None,74)
        match end_code:
            case 1:
                text = font.render("Black won!",True, WHITE)
            case 2:
                text = font.render("White won!",True, WHITE)
            case 3:
                text = font.render("Stalemate!",True,WHITE)
        if end_code != 4:
            text_rect = text.get_rect(center = (BOARD_X + 4 * SQUARE_SIZE, BOARD_Y + 4 *SQUARE_SIZE))
            screen.blit(text,text_rect)

            end_text = font.render("Play again",True, WHITE)
            end_rect = end_text.get_rect(center = (BOARD_X + 4 * SQUARE_SIZE, BOARD_Y + 5 * SQUARE_SIZE))
            mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
            if mouse_pos.x >= end_rect.x and mouse_pos.x <= end_rect.topright[0] and mouse_pos.y >= end_rect.y and mouse_pos.y <= end_rect.bottomleft[1]:
                pygame.draw.rect(screen,(0,255,0,0), (end_rect.x,end_rect.y,end_rect.topright[0] - end_rect.x,60),2)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    game_loop()
            screen.blit(end_text,end_rect)



        if white_turn == True:
            for i in range(8):
                for j in range(8):
                    p = board[i][j]
                    if p and isinstance(p,Pawn) and p.getColor() == False:
                        p.moved2 = False
        else:
            for i in range(8):
                for j in range(8):
                    p = board[i][j]
                    if p and isinstance(p,Pawn) and p.getColor() == True:
                        p.moved2 = False
        
        if(ok and event and event.type == pygame.MOUSEBUTTONDOWN):
            ok = False
            if(selected == False):
                selected_piece = mouse_square(board)
                check_turn = selected_piece[0]
                if check_turn != None:
                    if (check_turn.getColor() == False and white_turn ==  True) or (check_turn.getColor() == True and white_turn == False):
                        selected = True
            else:
                new_piece = mouse_square(board)
                np = board[selected_piece[1]][selected_piece[2]]

                if np :
                    last_move = np.move(selected_piece[1],selected_piece[2],new_piece[1],new_piece[2],board,last_move,darkKing,whiteKing)
                    

                    piece = last_move[0]
                    if piece :
                        if isinstance(piece,Pawn) and piece.getColor() == False and last_move[2] == 0:
                            white_prom = True
                        else:
                            if isinstance(piece,Pawn) and piece.getColor() == True and last_move[2] == 7:
                                black_prom = True
                    

                    if(last_move[3]):
                        white_turn = not white_turn
                
                selected = False
               
        

        
        
        
        
        pygame.display.flip()



        
        # Control the frame rate (30 FPS)
        clock.tick(30)

    # Quit pygame when done
    pygame.quit()
    sys.exit()

# Start the game loop
game_loop()
