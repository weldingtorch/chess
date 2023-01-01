max_id = -1
boards = []


class Board:
    def __init__(self, id, w=8, h=8) -> None:
        global max_id
        max_id += 1
        self.id = max_id

        (self.w, self.h) = (w, h)

        self.board = [[None for _ in range(w)] for _ in range(h)]
        
        boards.append(self)

    def fill(self):
        #rkbQKbkr
        #PPPPPPPP
        #________ X 4
        #PPPPPPPP
        #rkbQKbkr
        pass

    def rotate(self):
        list(map(lambda l: l.reverse(), self.board))
        self.board.reverse()
        # maybe will add team swap

    def make_move(self, team, x1, y1, x2, y2):
        piece = self.board[y1][x1]
        if piece.team == team and piece.check_move(x2, y2):
            pass


class Piece:
    def __init__(self, board_id, team, x, y) -> None:
        self.board_id = board_id
        self.team = team
        self.x = x
        self.y = y

    def check_move(self, x2, y2):
        board = boards[self.board_id].board
        new_cell = board[y2][x2]

        if x2 < 0 or x2 > board.w or x2 < 0 or y2 > board.h:
            return None
        
        if new_cell is not None and new_cell.team == self.team:
            return None
        
        return [((self.x, self.y),(x2, y2))]


class Pawn(Piece):
    def __init__(self, board_id, team, x, y) -> None:
        super().__init__(board_id, team, x, y)
        self.moved = False
        self.double_moved = False

    def check_move(self, x2, y2):
        self_move = super().check_move(x2, y2)
        if self_move is None:
            return None

        self_move = self_move[0]
        dx, dy = x2 - self.x, y2 - self.y
        board = boards[self.board_id]
        new_cell = board[y2][x2]

        if dx == 0 and dy in (1, 2) and board[y2 - 1][x2] is None: # straight fd
            if dy == 1: # fd 1 cell
                return [self_move]
            
            if dy == 2 and not self.moved and new_cell is None: # fd 2 cells
                return [self_move, lambda: True]
            
            return False

        if abs(dx) == 1 and dy == 1: # take piece
            if new_cell is not None: # regular take
                return True
            if isinstance(new_cell, Pawn) and new_cell.double_moved: # en passant (https://en.wikipedia.org/wiki/En_passant)  
                return True
        return False
        


if __name__ == "__main__":
    board = Board
    