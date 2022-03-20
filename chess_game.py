import piece
import board
from copy import deepcopy


class Chess():
    def __init__(self):
        self.board = board.Board()
        self.current = "white"
        self.side = True
        self.white_k_moved = False
        self.white_lr_moved = False
        self.white_sr_moved = False
        self.black_k_moved = False
        self.black_lr_moved = False
        self.black_sr_moved = False
        self.white_pieces_pos = [(0,i) for i in range(8)] + [(1,i) for i in range(8)]
        self.white_king_pos = (0,4)
        self.black_pieces_pos = [(7,i) for i in range(8)] + [(6,i) for i in range(8)]
        self.black_king_pos = (7,4)

    def swap_player(self):
        self.current = "black" if self.current == "white" else "white"
        self.side = not self.side

    def move_piece(self, from_pos, to_pos, side):
        en_passant = True if type(self.board.position[to_pos[0]][to_pos[1]]) == piece.ghost_pawn else False

        #update position list
        if side:
            self.white_pieces_pos.remove((from_pos[0], from_pos[1]))
            self.white_pieces_pos.append((to_pos[0], to_pos[1]))
            if self.board.position[to_pos[0]][to_pos[1]] != 'ㅤ' and type(self.board.position[to_pos[0]][to_pos[1]]) != piece.ghost_pawn:
                self.black_pieces_pos.remove((to_pos[0], to_pos[1]))
        else:
            self.black_pieces_pos.remove((from_pos[0], from_pos[1]))
            self.black_pieces_pos.append((to_pos[0], to_pos[1]))
            if self.board.position[to_pos[0]][to_pos[1]] != 'ㅤ' and type(self.board.position[to_pos[0]][to_pos[1]]) != piece.ghost_pawn:
                self.white_pieces_pos.remove((to_pos[0], to_pos[1]))

        self.board.position[to_pos[0]][to_pos[1]] = self.board.position[from_pos[0]][from_pos[1]]
        self.board.position[from_pos[0]][from_pos[1]] = 'ㅤ'

        #update moved if moves involve rook/king
        if (from_pos[0] == 0 and from_pos[1] == 0) or (to_pos[0] == 0 and to_pos[1] == 0):
            self.white_lr_moved = True
        if (from_pos[0] == 0 and from_pos[1] == 4) or (to_pos[0] == 0 and to_pos[1] == 4):
            self.white_k_moved = True
        if (from_pos[0] == 0 and from_pos[1] == 7) or (to_pos[0] == 0 and to_pos[1] == 7):
            self.white_sr_moved = True
        if (from_pos[0] == 7 and from_pos[1] == 0) or (to_pos[0] == 7 and to_pos[1] == 0):
            self.black_lr_moved = True
        if (from_pos[0] == 7 and from_pos[1] == 4) or (to_pos[0] == 7 and to_pos[1] == 4):
            self.black_k_moved = True
        if (from_pos[0] == 7 and from_pos[1] == 7) or (to_pos[0] == 7 and to_pos[1] == 7):
            self.black_sr_moved = True

        if type(self.board.position[to_pos[0]][to_pos[1]]) == piece.pawn:

            #en-passant case
            if en_passant:
                if side:
                    self.board.position[to_pos[0]-1][to_pos[1]] = 'ㅤ'
                    self.black_pieces_pos.remove((to_pos[0]-1,to_pos[1]))
                else:
                    self.board.position[to_pos[0]+1][to_pos[1]] = 'ㅤ'
                    self.white_pieces_pos.remove((to_pos[0]+1, to_pos[1]))

            #create ghosts if pawn move 2 steps
            if to_pos[0]-from_pos[0] == 2:
                self.board.position[to_pos[0]-1][to_pos[1]] = piece.ghost_pawn('white')
            elif to_pos[0]-from_pos[0] == -2:
                self.board.position[to_pos[0]+1][to_pos[1]] = piece.ghost_pawn('black')

        if type(self.board.position[to_pos[0]][to_pos[1]]) == piece.king:
            if side:
                self.white_king_pos = (to_pos[0],to_pos[1])
            else:
                self.black_king_pos = (to_pos[0],to_pos[1])

            #castle case
            #short side
            if to_pos[1]-from_pos[1] > 1:
                if side:
                    self.white_pieces_pos.remove((0,7))
                    self.white_pieces_pos.append((0,to_pos[1]-1))
                else:
                    self.black_pieces_pos.remove((7,7))
                    self.black_pieces_pos.append((7,to_pos[1]-1))
                self.board.position[to_pos[0]][to_pos[1]-1] = self.board.position[to_pos[0]][7]
                self.board.position[to_pos[0]][7] = 'ㅤ'
            #long side
            elif to_pos[1]-from_pos[1] < -1:
                if self.side:
                    self.white_pieces_pos.remove((0,0))
                    self.white_pieces_pos.append((0,to_pos[1]+1))
                else:
                    self.black_pieces_pos.remove((7,0))
                    self.black_pieces_pos.append((7,to_pos[1]+1))
                self.board.position[to_pos[0]][to_pos[1]+1] = self.board.position[to_pos[0]][0]
                self.board.position[to_pos[0]][0] = 'ㅤ'

        #clear ghosts of previous player
        if side:
            for i in range(8):
                if type(self.board.position[5][i]) == piece.ghost_pawn:
                    self.board.position[5][i] = 'ㅤ'
        else:
            for i in range(8):
                if type(self.board.position[2][i]) == piece.ghost_pawn:
                    self.board.position[2][i] = 'ㅤ'

    #return whether the king can be moved there
    def available(self, position, side):
        all_from = []
        all_to = []
        if side:
            for pos in self.black_pieces_pos:
                for i in self.board.position[pos[0]][pos[1]].can_see(self, self.board.position, pos, False):
                    all_from.append(pos)
                    all_to.append(i)
        else:
            for pos in self.white_pieces_pos:
                for i in self.board.position[pos[0]][pos[1]].can_see(self, self.board.position, pos, True):
                    all_from.append(pos)
                    all_to.append(i)
            return all_from, all_to
        if position in all_to:
            return False
        return True

    #return all possible moves
    def all_possible_move(self, side):
        all_from = []
        all_to = []
        if side:
            for pos in self.white_pieces_pos:
                for i in self.board.position[pos[0]][pos[1]].possible(self, self.board.position, pos, True):
                    all_from.append(pos)
                    all_to.append(i)
            return all_from, all_to
        else:
            for pos in self.black_pieces_pos:
                for i in self.board.position[pos[0]][pos[1]].possible(self, self.board.position, pos, False):
                    all_from.append(pos)
                    all_to.append(i)
            return all_from, all_to

    #for simplicity, only consider checkmate and stalemate
    def terminate(self):
        start, to = self.all_possible_move(self.side)
        from_pos, to_pos = self.all_possible_move(not self.side)
        for i in range(len(to_pos)):
            if not check_mate(self, from_pos[i], to_pos[i], not self.side):
                return [False, 0]
        if self.side:
            if self.black_king_pos in to:
                print("Checkmate.")
                return [True, 1]
            else:
                print("Stalemate.")
                return [True, 0]
        else:
            if self.white_king_pos in to:
                print("Checkmate.")
                return [True, -1]
            else:
                print("Stalemate.")
                return [True, 0]


#validate the move
def valid(chess,start,to,player):

    if len(start)!=2 or len(to)!=2:
        print("Input should be of length 2. Please try again.")
        return False

    if start[0]<'A' or start[0]>'H' or to[0]<'A' or to[0]>'H':
        print("Input out of range.")
        return False

    if start[1]<'1' or start[1]>'8' or to[1]<'1' or to[1]>'8':
        print("Input out of range.")
        return False

    from_pos = (int(start[1])-1, ord(start[0])-ord('A'))
    to_pos = (int(to[1])-1, ord(to[0])-ord('A'))
    piece_from = chess.board.position[from_pos[0]][from_pos[1]]
    piece_to = chess.board.position[to_pos[0]][to_pos[1]]

    if piece_from == 'ㅤ' or type(piece_from) == piece.ghost_pawn:
        print("There is no piece in the from position.")
        return False

    if piece_from.side != (chess.current == "white"):
        print("You cannot select opponent's pieces.")
        return False

    if not piece_from.valid_move(chess, from_pos, to_pos):
        print("Invalid move of the piece.")
        return False

    if piece_to != 'ㅤ' and (piece_from.side == piece_to.side):
        print("You cannot capture your own pieces.")
        return False

    if check_mate(chess, from_pos, to_pos, player):
        print("Potential check/being checked right now.")
        return False
    #check if the move will cause check

    return True


#checks whether the move will cause a check
def check_mate(chess, from_pos, to_pos, side):
    new_chess = deepcopy(chess)
    new_chess.move_piece(from_pos, to_pos, side)
    if side:
        all_from, all_to = new_chess.all_possible_move(not side)
        if new_chess.white_king_pos in all_to:
            return True
    else:
        all_from, all_to = new_chess.all_possible_move(not side)
        if new_chess.black_king_pos in all_to:
            return True
    return False