from boardGame.utility import Position, Color


class Piece:

    def __init__(self, color: Color, position: Position) -> None:
        self.position = position
        self._color = color

    @property
    def color(self):
        return self._color

    def move(self):
        ...

    def valid_moves(self):
        ...

    def __str__(self):
        raise NotImplementedError(
            "__str__ method must be implemented in derived classes.")


class Pawn(Piece):
    def __str__(self) -> str:
        if self.color == Color.WHITE:
            return '♙'
        return '♟'


class Rook(Piece):
    def __str__(self) -> str:
        if self.color == Color.WHITE:
            return '♖'
        return '♜'


class Knight(Piece):
    def __str__(self) -> str:
        if self.color == Color.WHITE:
            return '♘'
        return '♞'


class Bishop(Piece):
    def __str__(self) -> str:
        if self.color == Color.WHITE:
            return '♗'
        return '♝'


class Queen(Piece):
    def __str__(self) -> str:
        if self.color == Color.WHITE:
            return '♕'
        return '♛'


class King(Piece):
    def __str__(self) -> str:
        if self.color == Color.WHITE:
            return '♔'
        return '♚'
