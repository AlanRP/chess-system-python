import enum


class Piece:

    def __init__(self, board) -> None:
        self._position = None
        self._board = board

    @property
    def board(self):
        return self._board

    def move(self):
        ...

    def valid_moves(self):
        ...

    def __str__(self) -> str:
        ...


class Color(enum.Enum):
    BLACK = 1
    WHITE = 2


class ChessPiece(Piece):
    def __init__(self, board):
        super().__init__(board)
