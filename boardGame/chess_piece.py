from boardGame.utility import (
    Color, Position, moves_all, cross_moves, x_moves, knight_moves)
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

# Symbols for pieces used:
# ♔ ♕ ♖ ♗ ♘ ♙ (White)
# ♚ ♛ ♜ ♝ ♞ ♟ (black)


class Pawn(ChessPiece):
    def possible_moves(self):
        self.moves_mat = [[False] * 8 for _ in range(8)]

        if self.color == Color.WHITE:
            # Check one square above
            p = Position((self.position.row - 1, self.position.column))
            if self.board._position_exists(*p.position):
                if not self.board._is_there_a_piece(*p.position):
                    self.moves_mat[p.row][p.column] = True

            # Check two square above and if it's first move
            p = Position((self.position.row - 2, self.position.column))
            if self.position.row == 6 and self.moves_mat[5][p.column]:
                if self.board._position_exists(*p.position):
                    if not self.board._is_there_a_piece(*p.position):
                        self.moves_mat[p.row][p.column] = True

            # Check capture diagonal square left
            p = Position((self.position.row - 1, self.position.column - 1))
            if self.board._position_exists(*p.position):
                if self._is_there_opponent_piece(p):
                    self.moves_mat[p.row][p.column] = True

            # Check capture diagonal square right
            p = Position((self.position.row - 1, self.position.column + 1))
            if self.board._position_exists(*p.position):
                if self._is_there_opponent_piece(p):
                    self.moves_mat[p.row][p.column] = True

        else:   # Black color piece
            p = Position((self.position.row + 1, self.position.column))
            if self.board._position_exists(*p.position):
                if not self.board._is_there_a_piece(*p.position):
                    self.moves_mat[p.row][p.column] = True

            # Check two square below and if it's first move
            p = Position((self.position.row + 2, self.position.column))
            if self.position.row == 1 and self.moves_mat[2][p.column]:
                if self.board._position_exists(*p.position):
                    if not self.board._is_there_a_piece(*p.position):
                        self.moves_mat[p.row][p.column] = True

            # Check capture diagonal square left
            p = Position((self.position.row + 1, self.position.column - 1))
            if self.board._position_exists(*p.position):
                if self._is_there_opponent_piece(p):
                    self.moves_mat[p.row][p.column] = True

            # Check capture diagonal square right
            p = Position((self.position.row + 1, self.position.column + 1))
            if self.board._position_exists(*p.position):
                if self._is_there_opponent_piece(p):
                    self.moves_mat[p.row][p.column] = True

    def __str__(self) -> str:
        if self.color == Color.WHITE:
            return '♙'
        return '♟'


class Rook(ChessPiece):
    def possible_moves(self) -> bool:
        self.moves_mat = [[False] * 8 for _ in range(8)]

        # Searching moves for Rook
        for r, c in cross_moves.values():
            p = Position((self.position.row + r, self.position.column + c))
            while (self.board._position_exists(*p.position) and not
                    self.board._is_there_a_piece(*p.position)):
                self.moves_mat[p.row][p.column] = True
                p.row += r
                p.column += c
            if self.board._position_exists(*p.position):
                if self._is_there_opponent_piece(p):
                    self.moves_mat[p.row][p.column] = True

    def __str__(self) -> str:
        if self.color == Color.WHITE:
            return '♖'
        return '♜'


class Knight(ChessPiece):
    def can_move(self, position: Position):
        row, column = position.position
        p = self.board._pieces[row][column]
        return p is None or p.color != self.color

    def possible_moves(self):
        self.moves_mat = [[False] * 8 for _ in range(8)]

        # Searching moves for Knight
        for r, c in knight_moves.values():
            p = Position((self.position.row + r, self.position.column + c))
            if (self.board._position_exists(*p.position) and
                    self.can_move(p)):
                self.moves_mat[p.row][p.column] = True

    def __str__(self) -> str:
        if self.color == Color.WHITE:
            return '♘'
        return '♞'


class Bishop(ChessPiece):
    def possible_moves(self) -> bool:
        self.moves_mat = [[False] * 8 for _ in range(8)]

        # Searching moves for Bishop
        for r, c in x_moves.values():
            p = Position((self.position.row + r, self.position.column + c))
            while (self.board._position_exists(*p.position) and not
                    self.board._is_there_a_piece(*p.position)):
                self.moves_mat[p.row][p.column] = True
                p.row += r
                p.column += c
            if self.board._position_exists(*p.position):
                if self._is_there_opponent_piece(p):
                    self.moves_mat[p.row][p.column] = True

    def __str__(self) -> str:
        if self.color == Color.WHITE:
            return '♗'
        return '♝'


class Queen(ChessPiece):
    def possible_moves(self) -> bool:
        self.moves_mat = [[False] * 8 for _ in range(8)]

        # Searching moves for Queen
        for r, c in moves_all.values():
            p = Position((self.position.row + r, self.position.column + c))
            while (self.board._position_exists(*p.position) and not
                    self.board._is_there_a_piece(*p.position)):
                self.moves_mat[p.row][p.column] = True
                p.row += r
                p.column += c
            if self.board._position_exists(*p.position):
                if self._is_there_opponent_piece(p):
                    self.moves_mat[p.row][p.column] = True

    def __str__(self) -> str:
        if self.color == Color.WHITE:
            return '♕'
        return '♛'


class King(ChessPiece):
    def can_move(self, position: Position):
        row, column = position.position
        p = self.board._pieces[row][column]
        return p is None or p.color != self.color

    def possible_moves(self):
        self.moves_mat = [[False] * 8 for _ in range(8)]

        # Searching moves for King
        for r, c in moves_all.values():
            p = Position((self.position.row + r, self.position.column + c))
            if (self.board._position_exists(*p.position) and
                    self.can_move(p)):
                self.moves_mat[p.row][p.column] = True

    def __str__(self) -> str:
        if self.color == Color.WHITE:
            return '♔'
        return '♚'
