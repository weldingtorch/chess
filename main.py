from types import FunctionType


max_id = -1
boards = []


class Board:
    def __init__(self, w=8, h=8) -> None:
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
        if piece is not None and piece.team == team:
            result = piece.check_move(x2, y2)
            if result is not None:
                for obj in result:
                    if isinstance(obj, tuple):
                        (x1, y1), (x2, y2) = obj
                        self.board[y2][x2] = self.board[y1][x1]
                        self.board[y2][x2].x, self.board[y2][x2].y = x2, y2
                        self.board[y1][x1] = None
                    elif isinstance(obj, FunctionType):
                        obj()
            else:
                print("illegal move")


class Piece:
    def __init__(self, board_id, team, x, y) -> None:
        self.properties = dict()
        self.board_id = self.properties["board_id"] = board_id
        self.team = self.properties["team"] = team
        self.x = self.properties["x"] = x
        self.y = self.properties["y"] = y

        self.board = boards[board_id]
        self.board.board[y][x] = self

    def get_properties(self, **args):
        values = [self.properties[key] for key in args if key in self.properties]
        return values
    
    def set_properties(self, **kwargs):
        for (key, value) in kwargs:
            if key in self.properties:
                self.properties[key] = value

    def check_move(self, x2, y2):
        new_cell = self.board.board[y2][x2]

        if x2 < 0 or x2 > self.board.w or x2 < 0 or y2 > self.board.h:
            return None
        
        if new_cell is not None and new_cell.team == self.team:
            return None
        
        return [((self.x, self.y),(x2, y2))]
    
    def discard(self):
        self.board.board[self.y][self.x] = None


class Pawn(Piece):
    def __init__(self, board_id, team, x, y) -> None:
        super().__init__(board_id, team, x, y)
        self.moved = self.properties["moved"] = False
        self.double_moved = self.properties["double_moved"] = False

    def __repr__(self):
        return "p"

    def check_move(self, x2, y2):
        self_move = super().check_move(x2, y2)
        if self_move is None:
            return None

        self_move = self_move[0]
        dx, dy = x2 - self.x, y2 - self.y
        board = self.board.board
        new_cell = board[y2][x2]

        if dx == 0 and dy in (1, 2) and board[y2 - 1][x2] is None: # straight fd
            if dy == 1: # fd 1 cell
                if not self.moved: #TODO add promotion
                    return [self_move, lambda: self.set_properties(moved=True)]
                if self.double_moved:
                    return [self_move, lambda: self.set_properties(double_moved=False)]
                return [self_move]

            if dy == 2 and not self.moved and new_cell is None: # fd 2 cells
                return [self_move, lambda: self.set_properties(moved=True, double_moved=True), ]
            
            return None

        if abs(dx) == 1 and dy == 1: # take piece
            nearby_cell = board[y2 - 1][x2]
            if new_cell is not None or (isinstance(nearby_cell, Pawn) and 
                                        nearby_cell.team != self.team and 
                                        nearby_cell.double_moved): # regular take or en passant (https://en.wikipedia.org/wiki/En_passant)  
                if not self.moved:
                    return [lambda: new_cell.discard(), self_move, lambda: self.set_properties(moved=True)]
                if self.double_moved:
                    return [lambda: new_cell.discard(), self_move, lambda: self.set_properties(double_moved=False)]
                return [lambda: new_cell.discard(), self_move]
                   
        return None


class Bishop(Piece):

    def __init__(self, board_id, team, x, y) -> None:
        super().__init__(board_id, team, x, y)

    def __repr__(self):
        return "b"

    def check_move(self, x2, y2):
        self_move = super().check_move(x2, y2)
        if self_move is None:
            return None
        
        self_move = self_move[0]

        dx = x2 - self.x
        dy = y2 - self.y
        if abs(dx) == abs(dy):
            sx = dx // abs(dx)
            sy = dy // abs(dy)

            for d in range(1, abs(dx)):
                print(f"checking: ({self.y + d * sy}, {self.x + d * sx}) -> {self.board.board[self.y + d * sy][self.x + d * sx]}")
                if self.board.board[self.y + d * sy][self.x + d * sx] is not None:
                    return None
                
            new_cell = self.board.board[y2][x2]
            if new_cell is not None:
                return [lambda: new_cell.discard(), self_move]
            
            return [self_move]
          
        return None


# class Knight(Piece):
#     def __init__(self, board_id, team, x, y) -> None:
#         super().__init__(board_id, team, x, y)

if __name__ == "__main__":
    board = Board()
    Pawn(0, "black", 7, 7)
    Bishop(0, "white", 0, 0)

    while True:
        for rank in board.board:
            print(rank)
        x1, y1, x2, y2 = (int(i) for i in input("x1 y1 x2 y2:").split())
        board.make_move("white", x1, y1, x2, y2)
