from boardGame.utility import Color
from boardGame.piece import Piece


class King(Piece):
    def __init__(self, board, color: Color):
        super().__init__(board, color)

    def __str__(self) -> str:
        # return super().__str__()
        return 'K'


class Rook(Piece):
    def __init__(self, board, color: Color):
        super().__init__(board, color)

    def __str__(self) -> str:
        return 'R'
