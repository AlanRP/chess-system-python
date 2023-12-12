from boardGame.piece import Piece
import enum


class Color(enum.Enum):
    WHITE = 1
    BLACK = 2


class ChessPiece(Piece):
    def __init__(self, board, color: Color):
        super().__init__(board)
        self._color = color

    @property
    def color(self):
        return self._color

    def __repr__(self) -> str:
        # return super().__repr__()
        cls_name = self.__class__.__name__
        return f'{cls_name} - Position: {self.position}'
