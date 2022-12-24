class Piece:
    def __init__(self, layout, board):
        self.layout = layout
        self.board = board
        self.position = [2,0] # position of BOTTOM LEFT EDGE
        self.width = len(self.layout[0])
        self.height = len(self.layout)

        self.bottom_indices = [i for i,k in enumerate(self.layout[-1]) if k]
        self.right_indices = [i for i in range(self.height) if self.layout[i][-1]]
        self.left_indices = [i for i in range(self.height) if self.layout[i][0]]

    def move(self, dir) -> bool:
        x,y = self.position
        dx,dy = dir
        if dy == 0:
            print("shift")
            if dx == 1:
                if x+dx+self.width-1 < 7 and all(self.board.grid[y-self.height+1+i][x+self.width-1+dx] == 0 for i in self.right_indices):
                    self.position[0] += dx
            elif dx == -1:
                if x+dx >= 0 and all(self.board.grid[y-self.height+1+i][x+dx] == 0 for i in self.left_indices):
                    self.position[0] += dx
            return True
        else:
            print("drop")
            if y < self.board.height-1 and all(self.board.grid[y+dy][x+i] == 0 for i in self.bottom_indices):
                self.position[1] += dy
                return True
            return False

class Board:
    pieces = [
        [[1,1,1,1]],

        [[0,1,0],
         [1,1,1],
         [0,1,0]],

        [[0,0,1],
         [0,0,1],
         [1,1,1]],

        [[1],
         [1],
         [1],
         [1]],

        [[1,1],
         [1,1]]
    ]

    def __init__(self, jet: str):
        self.jet = tuple([((1,0),(-1,0))["><".index(k)] for k in jet])
        self.jet_length = len(jet)
        self.grid = []
        self.pindex = 0
        self.jindex = 0
        for _ in range(4):
            self.grid.append([0,0,0,0,0,0,0])
        self.height = 4
    
    def place(self, counter: int = None):
        piece = Piece(self.__class__.pieces[self.pindex], self)
        jet = True
        while (counter is None or counter > 0) and (can_move := piece.move(self.jet[self.jindex] if jet else (0, 1))):
            if jet:
                jet = False
                self.jindex = (self.jindex + 1) % self.jet_length
            else:
                jet = True
            if counter is not None:
                counter -= 1

        # y of top of piece
        top = piece.position[1]-piece.height

        # ensure 0 is 3 above tallest piece
        if top < 3:
            self.height += 3-top
            for _ in range(3-top):
                self.grid.insert(0, [0,0,0,0,0,0,0])
            piece.position[1]+=3-top
        for py,row in enumerate(piece.layout):
            for px,cell in enumerate(row):
                if cell:
                    self.grid[piece.position[1]-piece.height+py+1][piece.position[0]+px] = 1
        

        self.pindex = (self.pindex + 1) % len(self.__class__.pieces)

    def __str__(self):
        return "\n".join(f"|{''.join('#' if c else '.' for c in row)}|" for row in self.grid) + "\n+-------+"

PROD = False

with open("input" if PROD else "sample") as f:
    lines = [g.strip() for g in f.readlines()]
    board = Board(lines[0])

for _ in range(3):
    board.place()
board.place(8)


print(str(board))