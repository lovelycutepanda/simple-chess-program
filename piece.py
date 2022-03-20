import board
import chess_game as chess


class pieces:
    def __init__(self, side):
        self.side = self.is_white(side)

    def is_white(self, side):
        return side == 'white'

        #red is white, green is black
        #valid move: whether a movement is possible, not considering the possibility of being checked
        #can see: all positions that the piece can reach


class rook(pieces):
    def __init__(self, side):
        super().__init__(side)

    def __str__(self):
        return '♖' if self.side else '♜'

    #valid move: vertical or horizontal line movement, no pieces between start and end
    def valid_move(self, chess, from_pos, to_pos):
        if from_pos[0] != to_pos[0] and from_pos[1] != to_pos[1]:
            return False
        if from_pos[0] == to_pos[0]:
            sgn = 1 if to_pos[1]-from_pos[1] > 0 else -1
            for i in range(from_pos[1]+sgn, to_pos[1], sgn):
                if chess.board.position[from_pos[0]][i] != 'ㅤ' and type(chess.board.position[from_pos[0]][i]) != ghost_pawn:
                    return False
        else:
            sgn = 1 if to_pos[0]-from_pos[0] > 0 else -1
            for i in range(from_pos[0]+sgn, to_pos[0], sgn):
                if chess.board.position[i][from_pos[1]] != 'ㅤ' and type(chess.board.position[i][from_pos[1]]) != ghost_pawn:
                    return False
        return True

    def can_see(self, chess, board, position, side):
        possible_move = []
        bot = position[0]
        top = position[0]
        left = position[1]
        right = position[1]
        while left>0 and (board[position[0]][left-1] == 'ㅤ' or type(board[position[0]][left-1]) == ghost_pawn or board[position[0]][left-1].side != side):
            left = left-1
            possible_move.append((position[0],left))
            if board[position[0]][left] != 'ㅤ' and type(board[position[0]][left]) != ghost_pawn:
                break
        while right<7 and (board[position[0]][right+1] == 'ㅤ' or type(board[position[0]][right+1]) == ghost_pawn or board[position[0]][right+1].side != side):
            right = right+1
            possible_move.append((position[0],right))
            if board[position[0]][right] != 'ㅤ' and type(board[position[0]][right]) != ghost_pawn:
                break
        while bot>0 and (board[bot-1][position[1]] == 'ㅤ' or type(board[bot-1][position[1]]) == ghost_pawn or board[bot-1][position[1]].side != side):
            bot = bot-1
            possible_move.append((bot,position[1]))
            if board[bot][position[1]] != 'ㅤ' and type(board[bot][position[1]]) != ghost_pawn:
                break
        while top<7 and (board[top+1][position[1]] == 'ㅤ' or type(board[top+1][position[1]]) == ghost_pawn or board[top+1][position[1]].side != side):
            top = top+1
            possible_move.append((top,position[1]))
            if board[top][position[1]] != 'ㅤ' and type(board[top][position[1]]) != ghost_pawn:
                break
        return possible_move

    def possible(self, chess, board, position, side):
        return self.can_see(chess, board, position, side)


class knight(pieces):
    def __init__(self, side):
        super().__init__(side)

    def __str__(self):    
        return '♘' if self.side else '♞'

    #valid move: 2 steps in one direction + 1 step in perpendicular direction
    def valid_move(self, chess, from_pos, to_pos):
        if not ((abs(from_pos[0]-to_pos[0]) == 2 and abs(from_pos[1]-to_pos[1]) == 1) or (abs(from_pos[0]-to_pos[0]) == 1 and abs(from_pos[1]-to_pos[1]) == 2)):
            return False
        return True


    def can_see(self, chess, board, position, side):
        possible_move = []
        move = [(position[0]-2,position[1]-1),(position[0]-1,position[1]-2),(position[0]+2,position[1]-1),(position[0]-1,position[1]+2),(position[0]-2,position[1]+1),(position[0]+1,position[1]-2),(position[0]+2,position[1]+1),(position[0]+1,position[1]+2)]
        for pos in move:
            if 0 <= pos[0] <= 7 and 0 <= pos[1] <= 7 and (board[pos[0]][pos[1]] == 'ㅤ' or type(board[pos[0]][pos[1]]) == ghost_pawn or board[pos[0]][pos[1]].side != side):
                possible_move.append(pos)
        return possible_move

    def possible(self, chess, board, position, side):
        return self.can_see(chess, board, position, side)


class bishop(pieces):
    def __init__(self, side):
        super().__init__(side)

    def __str__(self):    
        return '♗' if self.side else '♝'

    #valid move: diagonal line movement, no piece between start and end
    def valid_move(self, chess, from_pos, to_pos):
        if abs(from_pos[0]-to_pos[0]) != abs(from_pos[1]-to_pos[1]):
            return False
        upwards = 1 if to_pos[0]-from_pos[0] == to_pos[1]-from_pos[1] else -1
        sgn = 1 if to_pos[0]-from_pos[0] > 0 else -1
        for i in range(sgn, to_pos[0]-from_pos[0], sgn):
            if chess.board.position[from_pos[0]+i][from_pos[1]+upwards*i] != 'ㅤ' and type(chess.board.position[from_pos[0]+i][from_pos[1]+upwards*i]) != ghost_pawn:
                return False
        return True

    def can_see(self, chess, board, position, side):
        possible_move = []
        a1 = [position[0],position[1]]
        a2 = [position[0],position[1]]
        a3 = [position[0],position[1]]
        a4 = [position[0],position[1]]
        while a1[0]>0 and a1[1]>0 and (board[a1[0]-1][a1[1]-1] == 'ㅤ' or type(board[a1[0]-1][a1[1]-1]) == ghost_pawn or board[a1[0]-1][a1[1]-1].side != side):
            a1[0] = a1[0]-1
            a1[1] = a1[1]-1
            possible_move.append((a1[0],a1[1]))
            if board[a1[0]][a1[1]] != 'ㅤ' and type(board[a1[0]][a1[1]]) != ghost_pawn:
                break
        while a2[0]<7 and a2[1]<7 and (board[a2[0]+1][a2[1]+1] == 'ㅤ' or type(board[a2[0]+1][a2[1]+1]) == ghost_pawn or board[a2[0]+1][a2[1]+1].side != side):
            a2[0] = a2[0]+1
            a2[1] = a2[1]+1
            possible_move.append((a2[0],a2[1]))
            if board[a2[0]][a2[1]] != 'ㅤ' and type(board[a2[0]][a2[1]]) != ghost_pawn:
                break
        while a3[0]>0 and a3[1]<7 and (board[a3[0]-1][a3[1]+1] == 'ㅤ' or type(board[a3[0]-1][a3[1]+1]) == ghost_pawn or board[a3[0]-1][a3[1]+1].side != side):
            a3[0] = a3[0]-1
            a3[1] = a3[1]+1
            possible_move.append((a3[0],a3[1]))
            if board[a3[0]][a3[1]] != 'ㅤ' and type(board[a3[0]][a3[1]]) != ghost_pawn:
                break
        while a4[0]<7 and a4[1]>0 and (board[a4[0]+1][a4[1]-1] == 'ㅤ' or type(board[a4[0]+1][a4[1]-1]) == ghost_pawn or board[a4[0]+1][a4[1]-1].side != side):
            a4[0] = a4[0]+1
            a4[1] = a4[1]-1
            possible_move.append((a4[0],a4[1]))
            if board[a4[0]][a4[1]] != 'ㅤ' and type(board[a4[0]][a4[1]]) != ghost_pawn:
                break
        return possible_move

    def possible(self, chess, board, position, side):
        return self.can_see(chess, board, position, side)
        

class queen(pieces):
    def __init__(self, side):
        super().__init__(side)

    def __str__(self):    
        return '♕' if self.side else '♛'

    #valid move: vertical or horizontal or diagonal line movement, no piece between start and end
    def valid_move(self, chess, from_pos, to_pos):
        if from_pos[0] != to_pos[0] and from_pos[1] != to_pos[1] and abs(from_pos[0]-to_pos[0]) != abs(from_pos[1]-to_pos[1]):
            return False
        if from_pos[0] == to_pos[0]:
            sgn = 1 if to_pos[1]-from_pos[1] > 0 else -1
            for i in range(from_pos[1]+sgn, to_pos[1], sgn):
                if chess.board.position[from_pos[0]][i] != 'ㅤ' and type(chess.board.position[from_pos[0]][i]) != ghost_pawn:
                    return False
        elif from_pos[1] == to_pos[1]:
            sgn = 1 if to_pos[0]-from_pos[0] > 0 else -1
            for i in range(from_pos[0]+sgn, to_pos[0], sgn):
                if chess.board.position[i][from_pos[1]] != 'ㅤ' and type(chess.board.position[i][from_pos[1]]) != ghost_pawn:
                    return False
        else:
            upwards = 1 if to_pos[0]-from_pos[0] == to_pos[1]-from_pos[1] else -1
            sgn = 1 if to_pos[0]-from_pos[0] > 0 else -1
            for i in range(sgn, to_pos[0]-from_pos[0], sgn):
                if chess.board.position[from_pos[0]+i][from_pos[1]+upwards*i] != 'ㅤ' and type(chess.board.position[from_pos[0]+i][from_pos[1]+upwards*i]) != ghost_pawn:
                    return False
        return True

    def can_see(self, chess, board, position, side):
        possible_move = []
        bot = position[0]
        top = position[0]
        left = position[1]
        right = position[1]
        a1 = [position[0], position[1]]
        a2 = [position[0], position[1]]
        a3 = [position[0], position[1]]
        a4 = [position[0], position[1]]
        while left>0 and (board[position[0]][left-1] == 'ㅤ' or type(board[position[0]][left-1]) == ghost_pawn or board[position[0]][left-1].side != side):
            left = left-1
            possible_move.append((position[0],left))
            if board[position[0]][left] != 'ㅤ' and type(board[position[0]][left]) != ghost_pawn:
                break
        while right<7 and (board[position[0]][right+1] == 'ㅤ' or type(board[position[0]][right+1]) == ghost_pawn or board[position[0]][right+1].side != side):
            right = right+1
            possible_move.append((position[0],right))
            if board[position[0]][right] != 'ㅤ' and type(board[position[0]][right]) != ghost_pawn:
                break
        while bot>0 and (board[bot-1][position[1]] == 'ㅤ' or type(board[bot-1][position[1]]) == ghost_pawn or board[bot-1][position[1]].side != side):
            bot = bot-1
            possible_move.append((bot,position[1]))
            if board[bot][position[1]] != 'ㅤ' and type(board[bot][position[1]]) != ghost_pawn:
                break
        while top<7 and (board[top+1][position[1]] == 'ㅤ' or type(board[top+1][position[1]]) == ghost_pawn or board[top+1][position[1]].side != side):
            top = top+1
            possible_move.append((top,position[1]))
            if board[top][position[1]] != 'ㅤ' and type(board[top][position[1]]) != ghost_pawn:
                break
        while a1[0]>0 and a1[1]>0 and (board[a1[0]-1][a1[1]-1] == 'ㅤ' or type(board[a1[0]-1][a1[1]-1]) == ghost_pawn or board[a1[0]-1][a1[1]-1].side != side):
            a1[0] = a1[0]-1
            a1[1] = a1[1]-1
            possible_move.append((a1[0],a1[1]))
            if board[a1[0]][a1[1]] != 'ㅤ' and type(board[a1[0]][a1[1]]) != ghost_pawn:
                break
        while a2[0]<7 and a2[1]<7 and (board[a2[0]+1][a2[1]+1] == 'ㅤ' or type(board[a2[0]+1][a2[1]+1]) == ghost_pawn or board[a2[0]+1][a2[1]+1].side != side):
            a2[0] = a2[0]+1
            a2[1] = a2[1]+1
            possible_move.append((a2[0],a2[1]))
            if board[a2[0]][a2[1]] != 'ㅤ' and type(board[a2[0]][a2[1]]) != ghost_pawn:
                break
        while a3[0]>0 and a3[1]<7 and (board[a3[0]-1][a3[1]+1] == 'ㅤ' or type(board[a3[0]-1][a3[1]+1]) == ghost_pawn or board[a3[0]-1][a3[1]+1].side != side):
            a3[0] = a3[0]-1
            a3[1] = a3[1]+1
            possible_move.append((a3[0],a3[1]))
            if board[a3[0]][a3[1]] != 'ㅤ' and type(board[a3[0]][a3[1]]) != ghost_pawn:
                break
        while a4[0]<7 and a4[1]>0 and (board[a4[0]+1][a4[1]-1] == 'ㅤ' or type(board[a4[0]+1][a4[1]-1]) == ghost_pawn or board[a4[0]+1][a4[1]-1].side != side):
            a4[0] = a4[0]+1
            a4[1] = a4[1]-1
            possible_move.append((a4[0],a4[1]))
            if board[a4[0]][a4[1]] != 'ㅤ' and type(board[a4[0]][a4[1]]) != ghost_pawn:
                break
        return possible_move

    def possible(self, chess, board, position, side):
        return self.can_see(chess, board, position, side)
        

class king(pieces):
    def __init__(self, side):
        super().__init__(side)

    def __str__(self):    
        return '♔' if self.side else '♚'

    #move within 8 neighbours, or castle
    def valid_move(self, chess, from_pos, to_pos):
        if abs(to_pos[0]-from_pos[0]) < 2 and abs(to_pos[1]-from_pos[1]) < 2:
            return True
        if from_pos[0] == to_pos[0]:
            if chess.board.position[to_pos[0]][to_pos[1]] != 'ㅤ':
                return False
            if to_pos[1] == 6:
                if (chess.side and not chess.white_k_moved and not chess.white_sr_moved) or (not chess.side and not chess.black_k_moved and not chess.black_sr_moved):
                    if chess.board.position[from_pos[0]][5] == 'ㅤ':
                        if chess.available((from_pos[0],5),chess.side):
                            return True
            elif to_pos[1] == 2:
                if (chess.side and not chess.white_k_moved and not chess.white_lr_moved) or (not chess.side and not chess.black_k_moved and not chess.black_lr_moved):
                    if chess.board.position[from_pos[0]][3] == 'ㅤ':
                        if chess.available((from_pos[0],3),chess.side):
                            return True
            elif to_pos[1] == 1:
                if (chess.side and not chess.white_k_moved and not chess.white_lr_moved) or (not chess.side and not chess.black_k_moved and not chess.black_lr_moved):
                    if chess.board.position[from_pos[0]][3] == 'ㅤ' and chess.board.position[from_pos[0]][2] == 'ㅤ':
                        if chess.available((from_pos[0],3),chess.side) and chess.available((from_pos[0],2),chess.side):
                            return True
        return False

    def can_see(self, chess, board, position, side):
        possible_move = []
        for i in range(-1,2):
            for j in range(-1,2):
                if 0 <= position[0]+i <= 7 and 0 <= position[1]+j <= 7 and (board[position[0]+i][position[1]+j] == 'ㅤ' or type(board[position[0]+i][position[1]+j]) == ghost_pawn or board[position[0]+i][position[1]+j].side != side):
                    possible_move.append((position[0]+i,position[1]+j))
        return possible_move

    def possible(self, chess, board, position, side):
        possible_move = self.can_see(chess, board, position, side)
        row = 0 if side else 7
        if (side and not chess.white_k_moved and not chess.white_sr_moved) or (
                not side and not chess.black_k_moved and not chess.black_sr_moved):
            if chess.board.position[row][5] == 'ㅤ' and chess.board.position[row][6] == 'ㅤ':
                if chess.available((row, 5), chess.side) and chess.available((row, 6), chess.side):
                    possible_move.append((row, 6))
        if (side and not chess.white_k_moved and not chess.white_lr_moved) or (
                not side and not chess.black_k_moved and not chess.black_lr_moved):
            if chess.board.position[row][3] == 'ㅤ' and chess.board.position[row][2] == 'ㅤ':
                if chess.available((row, 3), chess.side) and chess.available((row, 2), chess.side):
                    possible_move.append((row, 2))
                    if chess.board.position[row][1] == 'ㅤ' and chess.available((row, 1), chess.side):
                        possible_move.append((row, 1))
        return possible_move
        

class pawn(pieces):
    def __init__(self, side):
        super().__init__(side)

    def __str__(self):    
        return '♙' if self.side else '♟'

    def valid_move(self, chess, from_pos, to_pos):
        if self.side:
            if from_pos[0] == 1 and to_pos[0] == 3 and from_pos[1] == to_pos[1] and chess.board.position[2][from_pos[1]] == 'ㅤ' and chess.board.position[3][from_pos[1]] == 'ㅤ':
                return True
            if to_pos[0] == from_pos[0]+1 and to_pos[1] == from_pos[1] and chess.board.position[to_pos[0]][from_pos[1]] == 'ㅤ':
                return True
            if to_pos[0] == from_pos[0]+1 and abs(to_pos[1]-from_pos[1]) == 1 and chess.board.position[to_pos[0]][to_pos[1]] != 'ㅤ' and not chess.board.position[to_pos[0]][to_pos[1]].side:
                return True
        else:
            if from_pos[0] == 6 and to_pos[0] == 4 and from_pos[1] == to_pos[1] and chess.board.position[5][from_pos[1]] == 'ㅤ' and chess.board.position[4][from_pos[1]] == 'ㅤ':
                return True
            if to_pos[0] == from_pos[0]-1 and to_pos[1] == from_pos[1] and chess.board.position[to_pos[0]][from_pos[1]] == 'ㅤ':
                return True
            if to_pos[0] == from_pos[0]-1 and abs(to_pos[1]-from_pos[1]) == 1 and chess.board.position[to_pos[0]][to_pos[1]] != 'ㅤ' and chess.board.position[to_pos[0]][to_pos[1]].side:
                return True
        return False

    def can_see(self, chess, board, position, side):
        possible_move = []
        if side:
            if board[position[0]+1][position[1]] == 'ㅤ':
                possible_move.append((position[0]+1,position[1]))
            if position[0] == 1 and board[2][position[1]] == 'ㅤ' and board[3][position[1]] == 'ㅤ':
                possible_move.append((3,position[1]))
            for i in [-1,1]:
                if 0 <= position[1]+i <= 7 and board[position[0]+1][position[1]+i] != 'ㅤ' and not board[position[0]+1][position[1]+i].side:
                    possible_move.append((position[0]+1, position[1]+i))
        else:
            if board[position[0]-1][position[1]] == 'ㅤ':
                possible_move.append((position[0]-1,position[1]))
            if position[0] == 6 and board[5][position[1]] == 'ㅤ' and board[4][position[1]] == 'ㅤ':
                possible_move.append((4,position[1]))
            for i in [-1,1]:
                if 0 <= position[1]+i <= 7 and board[position[0]-1][position[1]+i] != 'ㅤ' and board[position[0]-1][position[1]+i].side:
                    possible_move.append((position[0]-1, position[1]+i))
        return possible_move

    def possible(self, chess, board, position, side):
        return self.can_see(chess, board, position, side)


#for the en-passant case only, cannot be printed or move
class ghost_pawn(pieces):
    def __init__(self, side):
        super().__init__(side)

    def __str__(self):
        return 'ㅤ'

    def valid_move(self, chess, from_pos, to_pos):
        return False

    def can_see(self, chess, board, position, side):
        return []

