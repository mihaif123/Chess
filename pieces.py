from abc import ABC, abstractmethod

from methods import quick_check,rook_attack,bishop_attack,is_check



class Piece(ABC):

    def __init__(self,color):
        self.black = color
        super().__init__()


    @abstractmethod
    def move(self,x,y):
        
        pass

    @abstractmethod
    def draw(self,x,y): 
        pass

    @abstractmethod
    def can_attack(self,xi,yi,xk,yk,board):
        pass

    @abstractmethod
    def has_legal_move(self,xi,yi,darkKing,whiteKing,board):
        pass
    @abstractmethod
    def getShortName(self):
        pass


    def getColor(self):
        return self.black
            
class Knight(Piece):

    def getShortName(self):
        return "N"


    def has_legal_move(self, xi, yi,darkKing,whiteKing, board,last_move):
        
        movx = [-2 ,-2 ,-1 ,-1, 1, 1, 2, 2]
        movy = [-1, 1, -2 , 2, -2, 2, 1, -1]

        king = whiteKing
        if self.black == True:
            king = darkKing

        legal_moves = []

        for i in range(8):
            ax = xi + movx[i]
            ay = yi + movy[i]
            if ax < 0 or ax > 7 or ay < 0 or ay > 7:
                continue

            piece = board[ax][ay]
            if piece:
                if piece.getColor() == self.getColor():
                    continue
            aux = board[ax][ay]
            board[ax][ay] = board[xi][yi]
            board[xi][yi] = None
            if not is_check(king , board):
                board[xi][yi] = board[ax][ay]
                board[ax][ay] = aux
                legal_moves.append((ax,ay))
                continue
            board [xi][yi] = board[ax][ay]
            board[ax][ay] = aux

        if legal_moves:
            return True,legal_moves
        return False,legal_moves




    def move(self,xi,yi,x,y,board,last_move,darkKing,whiteKing):
     

        has,legal_moves = self.has_legal_move(xi,yi,darkKing,whiteKing,board,last_move)
        if not has or (x,y) not in legal_moves:
            return (None, None ,None, False)
        
        board[x][y] = board[xi][yi]
        board[xi][yi] = None

        print(self.__class__.__name__, " moves from ", xi, yi, " to " , x , y)   

        last_move = (self, x, y, True)
        return last_move

    def can_attack(self, xi,yi,xk, yk, board):
        if xk == xi - 2 or xk == xi + 2:
            if yk == yi - 1 or yk == yi + 1:
                return True
        if yk == yi - 2 or yk == yi + 2:
            if xk == xi - 1 or xk == xi + 1:
                return True
        return False


    def draw(self):
        return (self.black, 3)

class Bishop(Piece):

    def getShortName(self):
        return "B"

    def has_legal_move(self, xi, yi,darkKing,whiteKing, board,last_move):
        
        dx = [-1, 1, 1, -1]
        dy = [-1, -1, 1, 1]

        return quick_check(darkKing,whiteKing,board,dx,dy,xi,yi,self)


    def can_attack(self,xi,yi, xk, yk, board):
        return bishop_attack(xi,yi,xk,yk,board)
        


    def move(self,xi,yi,x,y,board,last_move,darkKing,whiteKing):


        has,legal_moves = self.has_legal_move(xi,yi,darkKing,whiteKing,board,last_move)
        if not has or (x,y) not in legal_moves:
            return(None, None, None, False)

        print(self.__class__.__name__, " moves from ", xi, yi, " to " , x , y)
        board[x][y] = board[xi][yi]
        board[xi][yi] = None
        last_move = (self,x,y,True)
        return last_move

    def draw(self):
        return((self.black,2))

class Rook(Piece):

    def getShortName(self):
        return "R"

    def __init__(self, color):
        super().__init__(color)
        self.firstMove = True
    
    def has_legal_move(self, xi, yi,darkKing,whiteKing, board,last_move):
        
        dx = [0, 0, -1 , 1]
        dy = [1, -1 , 0, 0]

        return quick_check(darkKing,whiteKing,board,dx,dy,xi,yi,self)
                


    def can_attack(self, xi, yi, xk, yk, board):
        return rook_attack(xi,yi,xk,yk,board)


    def move(self,xi ,yi ,x ,y ,board,last_move,darkKing,whiteKing):
        
        has,legal_moves = self.has_legal_move(xi,yi,darkKing,whiteKing,board,last_move)
        if not has or (x,y) not in legal_moves:
            return (None, None ,None, False)

        print(self.__class__.__name__, " moves from ", xi, yi, " to " , x , y)
        
        board[x][y] = board[xi][yi]
        board[xi][yi] = None
        last_move = (self,x,y,True)
        self.firstMove = False
        return last_move

    def draw(self):
        return((self.black,4))
class King(Piece):


    def getShortName(self):
        return "K"

    def __init__(self, xk,yk,color):
        super().__init__(color)
        self.firstMove = True
        self.pos = (xk,yk)

    def has_legal_move(self, xi, yi,darkKing,whiteKing, board,last_move):
        
        movx = [0, 1, 1, 1, 0, -1, -1, -1]
        movy = [-1, -1, 0, 1, 1, 1, 0, -1]

        king = whiteKing
        if self.black == True:
            king = darkKing        

        legal_moves = []


        for i in range(8):
            ax = xi + movx[i]
            ay = yi + movy[i]

            if ax < 0 or ay < 0 or ax > 7 or ay > 7:
                continue

            piece = board[ax][ay]
            if piece:
                if piece.getColor() == self.getColor():
                    continue
            
            aux = board[ax][ay]
            board[ax][ay] = board[xi][yi]
            board[xi][yi] = None
            self.pos = (ax,ay)
            if not is_check(king, board):
                board[xi][yi] = board[ax][ay]
                board[ax][ay] = aux
                self.pos = (xi,yi)
                legal_moves.append((ax,ay))
                continue
            board[xi][yi] = board[ax][ay]
            board[ax][ay] = aux
            self.pos = (xi,yi)

        if self.firstMove == True:
            #king side castle
            if board[xi + 1][yi] == None and board[xi + 2][yi] == None:
                ok = True
                for ii in range(8):
                    for jj in range(8):
                        p = board[ii][jj]
                        if p and p.getColor() != self.black:
                            if p.can_attack(ii, jj, xi + 1, yi,board) or p.can_attack(ii, jj , xi + 2,  yi, board):
                                ok = False



                rook = board[xi + 3][yi]
                
                if rook and rook.getColor() == self.getColor() and isinstance(rook, Rook):
                    if rook.firstMove == True:

                        board[xi + 2][yi] = board[xi][yi]
                        board[xi + 1][yi] = board[xi + 3][yi]
                        board[xi][yi] = None
                        board[xi + 3][yi] = None
                        if not is_check(self,board) and ok:
                            legal_moves.append((xi + 2,yi))

                        board[xi][yi] = board[xi + 2][yi]
                        board[xi + 3][yi] = board[xi + 1][yi]
                        board[xi + 2][yi] = None
                        board[xi + 1][yi] = None
            #queen side castle
            if board[xi - 1][yi] == None and board[xi - 2][yi] == None and board[xi - 3][yi] == None:

                ok = True
                for ii in range(8):
                    for jj in range(8):
                        p = board[ii][jj]
                        if p and p.getColor() != self.black:
                            if p.can_attack(ii, jj, xi - 1, yi,board) or p.can_attack(ii, jj , xi - 2,  yi, board) or p.can_attack(ii, jj, xi - 3, yi, board):
                                ok = False

                rook = board[xi - 4][yi]
                if rook and rook.getColor() == self.getColor() and isinstance(rook, Rook):
                    if rook.firstMove == True:
                        
                        board[xi - 2][yi] = board[xi][yi]
                        board[xi - 1][yi] = board[xi - 4][yi]
                        board[xi][yi] = None
                        board[xi - 4][yi] = None
                        if not is_check(self,board) and ok:
                            legal_moves.append((xi - 2, yi))
                        board[xi][yi] = board[xi - 2][yi]
                        board[xi - 4][yi] = board[xi - 1][yi]
                        board[xi - 2][yi] = None
                        board[xi - 1][yi] = None





        if legal_moves:
            return True, legal_moves
        return False,legal_moves




    def can_attack(self, xi, yi, xk, yk, board):
        return super().can_attack(xi, yi, xk, yk, board)
    def move(self,xi,yi ,x, y,board,last_move,darkKing,whiteKing):

        has,legal_moves = self.has_legal_move(xi,yi,darkKing,whiteKing,board,last_move)
        if not has or (x,y) not in legal_moves:
            return (None, None ,None, False)
                
        self.pos = (xi,yi)

        if xi == x + 1 or xi == x - 1 or xi == x:
            if yi == y - 1 or yi == y + 1 or yi == y:
                    board[x][y] = board[xi][yi]
                    board[xi][yi] = None
                    moved = True

        #king side castle
        if yi == y and xi == x - 2:
            rook = board[x+1][y]
            if board[x-1][y] == None and board[x][y] == None:
                if rook.firstMove == True and self.firstMove == True:
                    board[x][y] = board[xi][yi]
                    board[x-1][y] = rook
                    board[x+1][y] = None
                    board[xi][yi] = None
                    moved = True
        #queen side castle
        if yi == y and xi == x + 2:
            rook = board[x - 2][y]
            if board[x+1][y] == None and board[x][y] == None and board[x-1][y] == None:
                if rook.firstMove == True and self.firstMove == True:
                    board[x][y] = board[xi][yi]
                    board[x+1][y] = rook
                    board[x - 2][y] = None
                    board[xi][yi] = None
                    moved = True

        print(self.__class__.__name__, " moves from ", xi, yi, " to " , x , y)


        self.pos = (x,y)
        self.firstMove = False
        last_move = (self,x,y,moved)
        return last_move

    def draw(self):
       return ((self.black,0))

class Queen(Piece):


    def getShortName(self):
        return "Q"

    def has_legal_move(self, xi, yi,darkKing,whiteKing, board,last_move):
        

        legal_moves = []
        #bishopMoves

        dx = [-1, 1, 1, -1]
        dy = [-1, -1, 1, 1]

        t1,legals = quick_check(darkKing,whiteKing,board,dx,dy,xi,yi,self)
        legal_moves = legal_moves + legals

        #rookMoves

        dx = [-1, 0, 1, 0]
        dy = [0, -1, 0 ,1]

        t2,legals = quick_check(darkKing,whiteKing,board,dx,dy,xi,yi,self)
        legal_moves = legal_moves + legals
        #kingMoves

        movx = [0, 1, 1, 1, 0, -1 ,-1 ,-1]
        movy = [-1, -1, 0, 1, 1, 1, 0, -1]


        king = whiteKing
        if self.black == True:
            king = darkKing

        for i in range(7):
            ax = xi + movx[i]
            ay = yi + movy[i]
            if ax < 0 or ax > 7 or ay < 0 or ay > 7:
                continue

            piece = board[ax][ay]
            if piece:
                if piece.getColor() == self.getColor():
                    continue
            aux = board[ax][ay]
            board[ax][ay] = board[xi][yi]
            board[xi][yi] = None
            if not is_check(king , board):
                board[xi][yi] = board[ax][ay]
                board[ax][ay] = aux
                legal_moves.append((ax,ay))
                continue
            board [xi][yi] = board[ax][ay]
            board[ax][ay] = aux
        
        if legal_moves:
            return True, legal_moves
        return False,legal_moves




    def can_attack(self, xi, yi, xk, yk, board):
        if xi == xk + 1 or xi == xk - 1 or xi == xk:
            if yi == yk - 1 or yi == yk + 1 or yi == yk:
                return True
        
        if rook_attack(xi,yi,xk,yk,board):
            return True
        if bishop_attack(xi,yi,xk,yk,board):
            return True
        return False

    def move(self,xi,yi,x,y,board,last_move,darkKing,whiteKing):
        
        
        has,legal_moves = self.has_legal_move(xi,yi,darkKing,whiteKing,board,last_move)
        if not has or (x,y) not in legal_moves:
            return (None, None ,None, False)      

        print(self.__class__.__name__, " moves from ", xi, yi, " to " , x , y)
        
        board[x][y] = board[xi][yi]
        board[xi][yi] = None
        last_move = (self,x,y, True)
        return last_move



    def draw(self):
        return ((self.black,5))
class Pawn(Piece):


    def getShortName(self):
        return "P"

    def __init__(self,color):
        super().__init__(color)
        self.firstMove = True
        self.moved2 = False

        
    def has_legal_move(self, xi, yi,darkKing,whiteKing, board,last_move):
        

        legal_moves = []
      
        king = whiteKing
        if self.black == True:
            king = darkKing

        movy = -1
        if self.black:
            movy = 1 

        #en passant check
        if xi > 1:
            p = board[xi - 1][yi]
            if p:
                if isinstance(p, Pawn) and p.getColor() != self.getColor() and p.moved2:
                    legal_moves.append((xi - 1, yi + movy))
        if xi < 7:
            p = board[xi + 1][yi]
            if p:
                if isinstance(p, Pawn) and p.getColor() != self.getColor() and p.moved2:
                    legal_moves.append((xi + 1, yi + movy))

                    
        if self.firstMove == True:
            movy = -2
            if self.black == True:
                movy = 2
            

            if board[xi][yi + movy] == None:
                board[xi][yi + movy] = board[xi][yi]
                board[xi][yi] = None
                if not is_check(king,board):
                    board[xi][yi] = board[xi][yi + movy]
                    board[xi][yi + movy] = None
                    legal_moves.append((xi,yi + movy))
                else:
                    board[xi][yi] = board[xi][yi + movy]
                    board[xi][yi + movy] = None

        movy = -1
        if self.black == True:
            movy = 1

        if board[xi][yi + movy] == None:
            board[xi][yi + movy] = board[xi][yi]
            board[xi][yi] = None
            if not is_check(king,board):
                board[xi][yi] = board[xi][yi + movy]
                board[xi][yi + movy] = None
                legal_moves.append((xi,yi + movy))
            else:    
                board[xi][yi] = board[xi][yi + movy]
                board[xi][yi + movy] = None
        

        if xi - 1 >= 0 :
            piece = board[xi - 1][yi + movy]
            if piece:
                if piece.getColor() != self.getColor():
                    aux = board[xi - 1][yi + movy]
                    board[xi - 1][yi + movy] = board[xi][yi]
                    board[xi][yi] = None
                    if not is_check(king ,board):
                        board[xi][yi] = board[xi - 1][yi + movy]
                        board[xi - 1][yi + movy] = aux
                        legal_moves.append((xi - 1, yi + movy))
                    else:
                        board[xi][yi] = board[xi - 1][yi + movy]
                        board[xi - 1][yi + movy] = aux

        if xi + 1 < 8:
            piece = board[xi + 1][yi + movy]
            if piece:
                if piece.getColor() != self.getColor():
                    aux = board[xi + 1][yi + movy]
                    board[xi + 1][yi + movy] = board[xi][yi]
                    board[xi][yi] = None
                    if not is_check(king ,board):
                        board[xi][yi] = board[xi + 1][yi + movy]
                        board[xi + 1][yi + movy] = aux
                        legal_moves.append((xi + 1,yi + movy))
                    else:
                        board[xi][yi] = board[xi + 1][yi + movy]
                        board[xi + 1][yi + movy] = aux
        
        if legal_moves:
            return True, legal_moves
        return False,legal_moves
    
    def can_attack(self, xi, yi, xk, yk, board):
        
        if self.black:
            return (yk == yi + 1 and (xk == xi - 1 or xk == xi + 1))
        else:
            return (yk == yi - 1 and (xk == xi - 1 or xk == xi + 1))
        

    def move(self,xi,yi,x,y,board,last_move,darkKing,whiteKing):

        
        has,legal_moves = self.has_legal_move(xi,yi,darkKing,whiteKing,board,last_move)
        if not has or (x,y) not in legal_moves:
            return (None, None ,None, False)

        movy = -1 
        if self.black == True:
            movy = 1

        if x == xi - 1 and y == yi + movy:
            p = board[x][y]
            if p:
                board[x][y] = board[xi][yi]
                board[xi][yi] = None
            else:
                board[xi - 1][yi] = None
                board[x][y] = board[xi][yi]
                board[xi][yi] = None
        elif x == xi + 1 and y == yi + movy:
            p = board[x][y]
            if p:
                board[x][y] = board[xi][yi]
                board[xi][yi] = None
            else:
                board[xi + 1][yi] = None
                board[x][y] = board[xi][yi]
                board[xi][yi] = None
        else:
            board[x][y] = board[xi][yi]
            board[xi][yi] = None

        self.firstMove = False
        if abs(y - yi) == 2:
            self.moved2 = True
        else:
            self.moved2 = False


        print(self.__class__.__name__ ," moves from ", xi,yi, " to ", x ,y)
        last_move = (self, x, y,True)
        return last_move
    
    def draw(self):
        return ((self.black,1))

