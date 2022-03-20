import piece
import chess_game


if __name__ == "__main__":
    chess = chess_game.Chess()
    chess.board.print_board()
    finished = [False, 0]

    while True:
        if chess.side:
            print("Current player: White")
        else:
            print("Current player: Black")
        start = input("From: ")
        if start == "resign":
            finished = [True, 1] if chess.side else [True, -1]
            break
        if start == "draw":
            draw = input("Draw offered. Do you accept? (y/n) ")
            if draw == "y":
                finished = [True, 0]
                break
            start = input("Offer declined. From: ")
        to = input("To: ")
        while not chess_game.valid(chess,start,to,chess.side):
            start = input("From: ")
            if start == "resign":
                finished = [True, 1] if chess.side else [True, -1]
                break
            if start == "draw":
                draw = input("Draw offered. Do you accept? (y/n) ")
                if draw == "y":
                    finished = [True, 0]
                    break
                start = input("Offer declined. From: ")
            to = input("To: ")

        if finished[0]:
            break
        from_pos = (int(start[1])-1, ord(start[0])-ord('A'))
        to_pos = (int(to[1])-1, ord(to[0])-ord('A'))
        chess.move_piece(from_pos, to_pos, chess.side)

        # promotion case
        if type(chess.board.position[to_pos[0]][to_pos[1]]) == piece.pawn and (to_pos[0] == 0 or to_pos[0] == 7):
            upgrade = input("Please pick which piece to promote to (q(queen), r(rook), n(knight), b(bishop)): ")
            while upgrade not in {'q', 'r', 'n', 'b'}:
                print("Invalid piece! Please input again.")
                upgrade = input("Please pick which piece to promote to (q(queen), r(rook), n(knight), b(bishop)): ")
            if upgrade == 'q':
                chess.board.position[to_pos[0]][to_pos[1]] = piece.queen('white') if chess.side else piece.queen('black')
            elif upgrade == 'r':
                chess.board.position[to_pos[0]][to_pos[1]] = piece.rook('white') if chess.side else piece.rook('black')
            elif upgrade == 'n':
                chess.board.position[to_pos[0]][to_pos[1]] = piece.knight('white') if chess.side else piece.knight('black')
            else:
                chess.board.position[to_pos[0]][to_pos[1]] = piece.bishop('white') if chess.side else piece.bishop('black')

        chess.board.print_board()
        print()
        finished = chess.terminate()
        if finished[0]:
            break
        chess.swap_player()

    if finished[1] == 1:
        print("White won the game!")
    elif finished[1] == 0:
        print("It is a draw.")
    else:
        print("Black won the game!")