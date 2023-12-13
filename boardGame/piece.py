from boardGame.utility import Position, Color


class Piece:

    def __init__(self, board, color: Color, position: Position) -> None:
        self.position: Position = position
        self._board = board
        self._color = color

    @property
    def color(self):
        return self._color

    @property
    def board(self):
        return self._board

    # @property
    # def position(self):
    #     return self._position

    # @position.setter
    # def position(self, position):
    #     self._position = position

    def move(self):
        ...

    def valid_moves(self):
        ...

    def __repr__(self) -> str:
        # return super().__repr__()
        cls_name = self.__class__.__name__
        return f'{cls_name} - Position: {self.position}'


class King(Piece):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __str__(self) -> str:
        # return super().__str__()
        return 'K'


class Rook(Piece):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __str__(self) -> str:
        return 'R'
