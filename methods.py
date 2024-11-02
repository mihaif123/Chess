def is_check(king, board):
    if king.pos == (None,None):
        return False
    king_x, king_y = king.pos
    clr = king.black
    
    #print(king.pos)

    for i in range(8) :
        for j in range(8):
            piece = board[i][j]
            if piece and piece.getColor() != clr:
                if piece.can_attack(i,j,king_x,king_y,board):
                    return True
                
    return False


def quick_check(darkKing,whiteKing,board,dx,dy,xi,yi,self):
    king = whiteKing
    if self.black == True:
            king = darkKing

    legal_moves = []

    for i in range (4):
        ax = xi
        ay = yi
        while ax + dx[i] >= 0 and ax + dx[i] < 8 and ay + dy[i] >= 0 and ay + dy[i]< 8:
            ax = ax + dx[i]
            ay = ay + dy[i]

            piece = board[ax][ay]
            if piece:
                if piece.getColor() == self.getColor():
                    break
                else:
                    legal_moves.append((ax,ay))
                    break
            
            aux = board[ax][ay]
            board[ax][ay] = board[xi][yi]
            board[xi][yi] = None
            if not is_check(king, board):
                board[xi][yi] = board[ax][ay]
                board[ax][ay] = aux
                legal_moves.append((ax,ay))
                continue
            
            board[xi][yi] = board[ax][ay]
            board[ax][ay] = aux
    if legal_moves:
        return True, legal_moves
    return False,legal_moves

def bishop_attack(xi,yi,xk,yk,board):
    if abs(xk - xi) != abs(yk - yi):
            return False
    if xk == xi and yk == yi:
        return False
    
    if xi < xk:
        if yi < yk :
            xaux = xi + 1
            yaux = yi + 1
            while xaux < xk:
                if board[xaux][yaux] != None:
                    return False
                xaux += 1
                yaux += 1
        else:
            xaux = xi + 1
            yaux = yi - 1
            while xaux < xk:
                if board[xaux][yaux] != None:
                    return False
                xaux +=1
                yaux -=1
    else:
        if yi < yk:
            xaux = xi - 1
            yaux = yi + 1
            while xaux > xk :
                if board[xaux][yaux] != None:
                    return False
                xaux -= 1
                yaux += 1
        else:
            xaux = xi - 1
            yaux = yi - 1
            while xaux > xk :
                if board[xaux][yaux] != None:
                    return False
                xaux -=1
                yaux -=1
    return True  
        

def rook_attack(xi,yi,xk,yk,board):
    if xi != xk and yi != yk:
        return False
       
    if xi == xk:
        if yi < yk :
            i = yi + 1
            while i < yk:
                if board[xk][i] != None:
                    return False
                i += 1
        else:
            i = yk + 1
            while i < yi:
                if board[xk][i] != None:
                    return False
                    
                i += 1
    else:
        if xi < xk:
            i = xi + 1
            while i < xk:
                if board[i][yk] != None:
                    return False    
                i += 1
        else:
            i = xk + 1
            while i < xi:
                if board[i][yk] != None:
                    return False    
                i += 1
    return True

