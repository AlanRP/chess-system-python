from abc import ABC, abstractclassmethod
from boardGame.utility import Position, Color


class Piece(ABC):

    def __init__(self, color: Color, position: Position) -> None:
        self._position = position
        self._color = color

    @property
    def color(self):
        return self._color

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, position):
        self._position = position

    def moves(self):
        ...

    @abstractclassmethod
    def possible_moves(self): ...

    def valid_moves(self):
        row, column = self._position
        return self.possible_moves()[row][column]

    def is_there_any_possible_move(self):
        mat = self.possible_moves()
        for row in mat:
            for value in row:
                if value:
                    return True
        return False

    @abstractclassmethod
    def __str__(self): ...


class Pawn(Piece):
    def possible_moves(self):
        return [[False] * 8 for _ in range(8)]

    def __str__(self) -> str:
        if self.color == Color.WHITE:
            return '♙'
        return '♟'


class Rook(Piece):
    def possible_moves(self):
        return [[False] * 8 for _ in range(8)]

    def __str__(self) -> str:
        if self.color == Color.WHITE:
            return '♖'
        return '♜'


class Knight(Piece):
    def possible_moves(self):
        return [[False] * 8 for _ in range(8)]

    def __str__(self) -> str:
        if self.color == Color.WHITE:
            return '♘'
        return '♞'


class Bishop(Piece):
    def possible_moves(self):
        return [[False] * 8 for _ in range(8)]

    def __str__(self) -> str:
        if self.color == Color.WHITE:
            return '♗'
        return '♝'


class Queen(Piece):
    def possible_moves(self):
        return [[False] * 8 for _ in range(8)]

    def __str__(self) -> str:
        if self.color == Color.WHITE:
            return '♕'
        return '♛'


class King(Piece):
    def possible_moves(self):
        return [[False] * 8 for _ in range(8)]

    def __str__(self) -> str:
        if self.color == Color.WHITE:
            return '♔'
        return '♚'
