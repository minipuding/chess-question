from abc import ABC, abstractmethod
from chessLib.position import Position
from chessLib.move import KnightMove
import random

class BaseGame(ABC):
    @abstractmethod
    def play(self, moves: int):
        pass

    @abstractmethod
    def setup(self):
        pass

class BishopMove:

    _moves_unit = [(1, 1), (-1, -1), (1, -1), (-1, 1)]

    def valid_moves(self, pos: Position) -> list:
        result = []
        validDist = self.valid_dist(pos.x, pos.y)
        for i, unit in enumerate(self._moves_unit):
            for dist in range(1, validDist[i]+1):
                p = Position(pos.x + dist * unit[0], pos.y + dist * unit[1])
                result.append(p)
        return result

    def valid_dist(self, x, y):
        """
        Calculating the valid move distance diagonally from current position. The order
        is corresponding to the `_moves_unit`.
        """
        return [
            min(8-x, 8-y),
            min(x-1, y-1),
            min(8-x, y-1),
            min(x-1, 8-y),
        ]

class QueenMove(BishopMove):

    _moves_unit = [(1, 1), (-1, -1), (1, -1), (-1, 1), (1, 0), (0, 1), (-1, 0), (0, -1)]

    def valid_dist(self, x, y):
        """
        Add horizontal and vertical valid distance based on `BishopMove.valid_dist`. The order
        is corresponding to the `_moves_unit`.
        """
        return super().valid_dist(x, y) + [8-x, 8-y, x-1, y-1]

class ComplexGame(BaseGame):

    def __init__(self):
        self.pieces = [KnightMove(), BishopMove(), QueenMove()]
        self.piecesPos = [None, None, None]
        self.piecesName = ["KNIGHT", "BISHOP", "QUEUE"]
        self.valid_idxes = [0, 1, 2]

    def play(self, moves: int):
        """put your code here"""

        # print the initial position of all pieces.
        for i in self.valid_idxes:
            print(f"0: I am {self.piecesName[i]}. My position is " + self.piecesPos[i].to_string())

        for i in range(1, moves+1):
            
            # the program will choose a piece at random.
            idx = random.choice(self.valid_idxes)

            while True:

                # move piece to a randomly selected valid position.
                pos = random.choice(self.pieces[idx].valid_moves(self.piecesPos[idx]))
                
                # keep one piece occupy any position on the board at a given time.
                if self._assert_diff_position(pos, self.piecesPos[(idx+1) % 3]) and \
                   self._assert_diff_position(pos, self.piecesPos[(idx-1) % 3]):
                    break
            
            # print Infos
            print(f"{i}: I am {self.piecesName[idx]}. My last position is {self.piecesPos[idx].to_string()}, and "
                  f"my current position is {pos.to_string()}")
            
            # update current position
            self.piecesPos[idx] = pos

    def setup(self):
        """put your code here"""

        # random.seed(0)

        # random to choose the predefined positions of each pieces.
        self.piecesPos[0] = Position(random.randint(1, 8), random.randint(1, 8))
        while True:
            self.piecesPos[1] = Position(random.randint(1, 8), random.randint(1, 8))
            if self._assert_diff_position(self.piecesPos[0], self.piecesPos[1]):
                break
        while True:
            self.piecesPos[2] = Position(random.randint(1, 8), random.randint(1, 8))
            if self._assert_diff_position(self.piecesPos[2], self.piecesPos[0]) and \
               self._assert_diff_position(self.piecesPos[2], self.piecesPos[1]):
                break
    
    @staticmethod
    def _assert_diff_position(pos1: Position, pos2: Position) -> bool:
        """
        Game Rule 1: Only one piece can occupy any position on the board at a given time.
        if the `pos1` is different from `pos2`, return True.
        """
        if pos1.x == pos2.x and pos1.y == pos2.y:
            return False
        return True