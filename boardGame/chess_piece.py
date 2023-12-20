from boardGame.utility import Color, Position
from boardGame.piece import Piece


class ChessPiece(Piece):
    def __init__(self, color: Color, position: Position, board) -> None:
        super().__init__(color, position)
        self._pieces = [[None] * 8] * 8
        self.board = board

    def _is_there_opponent_piece(self, position: Position) -> bool:
        row, column = position.position
        p = self.board._pieces[row][column]
        return p is not None and p.color != self.color


class Pawn(ChessPiece):
    def possible_moves(self):
        res = [[False] * 8 for _ in range(8)]
        res[0][0] = True    # todo just test, need to be deleted
        return res

    def __str__(self) -> str:
        if self.color == Color.WHITE:
            return '♙'
        return '♟'


class Rook(ChessPiece):
    def possible_moves(self) -> bool:
        self.moves_mat = [[False] * 8 for _ in range(8)]

        # p = Position('a1')
        # check above
        p = Position((self.position.row - 1, self.position.column))
        while (self.board._position_exists(*p.position) and not
                self.board._is_there_a_piece(*p.position)):
            self.moves_mat[p.row][p.column] = True
            # p.set_values(p.row - 1, p.column)
            p.row -= 1
        if self.board._position_exists(*p.position):
            if self._is_there_opponent_piece(p):
                self.moves_mat[p.row][p.column] = True

        # check Left
        p = Position((self.position.row, self.position.column - 1))
        while (self.board._position_exists(*p.position) and not
                self.board._is_there_a_piece(*p.position)):
            self.moves_mat[p.row][p.column] = True
            # p.set_values(p.row, p.column - 1)
            p.column -= 1
        if self.board._position_exists(*p.position):
            if self._is_there_opponent_piece(p):
                self.moves_mat[p.row][p.column] = True

        # check Right
        p = Position((self.position.row, self.position.column + 1))
        while (self.board._position_exists(*p.position) and not
                self.board._is_there_a_piece(*p.position)):
            self.moves_mat[p.row][p.column] = True
            # p.set_values(p.row, p.column + 1)
            p.column += 1
        if self.board._position_exists(*p.position):
            if self._is_there_opponent_piece(p):
                self.moves_mat[p.row][p.column] = True

        # check Below
        p = Position((self.position.row + 1, self.position.column))
        while (self.board._position_exists(*p.position) and not
                self.board._is_there_a_piece(*p.position)):
            self.moves_mat[p.row][p.column] = True
            # p.set_values(p.row + 1, p.column)
            p.row += 1
        if self.board._position_exists(*p.position):
            if self._is_there_opponent_piece(p):
                self.moves_mat[p.row][p.column] = True
        # return self.moves_mat

    def __str__(self) -> str:
        if self.color == Color.WHITE:
            return '♖'
        return '♜'


class Knight(ChessPiece):
    def possible_moves(self):
        return [[False] * 8 for _ in range(8)]

    def __str__(self) -> str:
        if self.color == Color.WHITE:
            return '♘'
        return '♞'


class Bishop(ChessPiece):
    def possible_moves(self):
        return [[False] * 8 for _ in range(8)]

    def __str__(self) -> str:
        if self.color == Color.WHITE:
            return '♗'
        return '♝'


class Queen(ChessPiece):
    def possible_moves(self):
        return [[False] * 8 for _ in range(8)]

    def __str__(self) -> str:
        if self.color == Color.WHITE:
            return '♕'
        return '♛'


class King(ChessPiece):
    def possible_moves(self):
        return [[False] * 8 for _ in range(8)]

    def __str__(self) -> str:
        if self.color == Color.WHITE:
            return '♔'
        return '♚'
