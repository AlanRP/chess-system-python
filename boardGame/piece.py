from .position import Position


class Piece:

    def __init__(self, board) -> None:
        self._position: Position = None
        self._board = board

    @property
    def board(self):
        return self._board

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, position):
        self._position = position

    def move(self):
        ...

    def valid_moves(self):
        ...
