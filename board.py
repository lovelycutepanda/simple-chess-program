import piece


class Board():
    def __init__(self):
        r1,r2 = piece.rook('white'),piece.rook('white')
        n1,n2 = piece.knight('white'),piece.knight('white')
        b1,b2 = piece.bishop('white'),piece.bishop('white')
        k = piece.king('white')
        q = piece.queen('white')
        p1,p2,p3,p4,p5,p6,p7,p8 = piece.pawn('white'),piece.pawn('white'),piece.pawn('white'),piece.pawn('white'),piece.pawn('white'),piece.pawn('white'),piece.pawn('white'),piece.pawn('white')
        R1,R2 = piece.rook('black'),piece.rook('black')
        N1,N2 = piece.knight('black'),piece.knight('black')
        B1,B2 = piece.bishop('black'),piece.bishop('black')
        K = piece.king('black')
        Q = piece.queen('black')
        P1,P2,P3,P4,P5,P6,P7,P8 = piece.pawn('black'),piece.pawn('black'),piece.pawn('black'),piece.pawn('black'),piece.pawn('black'),piece.pawn('black'),piece.pawn('black'),piece.pawn('black')
        self.position = [[r1,n1,b1,q,k,b2,n2,r2],[p1,p2,p3,p4,p5,p6,p7,p8],['ㅤ','ㅤ','ㅤ','ㅤ','ㅤ','ㅤ','ㅤ','ㅤ'],['ㅤ','ㅤ','ㅤ','ㅤ','ㅤ','ㅤ','ㅤ','ㅤ'],['ㅤ','ㅤ','ㅤ','ㅤ','ㅤ','ㅤ','ㅤ','ㅤ'],['ㅤ','ㅤ','ㅤ','ㅤ','ㅤ','ㅤ','ㅤ','ㅤ'],[P1,P2,P3,P4,P5,P6,P7,P8],[R1,N1,B1,Q,K,B2,N2,R2]]


    def print_board(self):
        print(' ','-' * 38)
        for i in range(8):
            print(8-i, end = ' ')
            for j in range(8):
                print('|', self.position[7-i][j], sep = ' ', end = ' ')
            print('|')
            print(' ','-' * 38)
        print('    Ａ   Ｂ   Ｃ   Ｄ   Ｅ   Ｆ   Ｇ   Ｈ')