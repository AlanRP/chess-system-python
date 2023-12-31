from boardGame.utility import (
    Color, Position, moves_all, cross_moves, x_moves, knight_moves)
from boardGame.piece import Piece


class ChessPiece(Piece):
    def __init__(self, color: Color, position: Position, board) -> None:
        super().__init__(color, position)
        self._pieces = [[None] * 8] * 8
        self.board = board
        self._move_count = 0

    @property
    def move_count(self):
        return self._move_count

    def increase_move_count(self):
        self._move_count += 1

    def decrease_move_count(self):
        self._move_count -= 1

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
        self.possibles = []

        if self.color == Color.WHITE:
            # Check one square above
            p = Position((self.position.row - 1, self.position.column))
            if self.board._position_exists(*p.position):
                if not self.board._is_there_a_piece(*p.position):
                    self.moves_mat[p.row][p.column] = True
                    self.possibles.append((p.row, p.column))

            # Check two square above and if it's first move
            p = Position((self.position.row - 2, self.position.column))
            if self.position.row == 6 and self.moves_mat[5][p.column]:
                if self.board._position_exists(*p.position):
                    if not self.board._is_there_a_piece(*p.position):
                        self.moves_mat[p.row][p.column] = True
                        self.possibles.append((p.row, p.column))

            # Check capture diagonal square left
            p = Position((self.position.row - 1, self.position.column - 1))
            if self.board._position_exists(*p.position):
                if self._is_there_opponent_piece(p):
                    self.moves_mat[p.row][p.column] = True
                    self.possibles.append((p.row, p.column))

            # Check capture diagonal square right
            p = Position((self.position.row - 1, self.position.column + 1))
            if self.board._position_exists(*p.position):
                if self._is_there_opponent_piece(p):
                    self.moves_mat[p.row][p.column] = True
                    self.possibles.append((p.row, p.column))

            # Check capture diagonal en Passant
            passant: Position = self.board.enPassantVulnerable
            if (passant is not None and
                    self.position.row == passant.row == 3 and
                    abs(self.position.column - passant.column) == 1):
                self.moves_mat[passant.row - 1][passant.column] = True
                self.possibles.append((passant.row - 1, passant.column))

        else:   # Black color piece
            p = Position((self.position.row + 1, self.position.column))
            if self.board._position_exists(*p.position):
                if not self.board._is_there_a_piece(*p.position):
                    self.moves_mat[p.row][p.column] = True
                    self.possibles.append((p.row, p.column))

            # Check two square below and if it's first move
            p = Position((self.position.row + 2, self.position.column))
            if self.position.row == 1 and self.moves_mat[2][p.column]:
                if self.board._position_exists(*p.position):
                    if not self.board._is_there_a_piece(*p.position):
                        self.moves_mat[p.row][p.column] = True
                        self.possibles.append((p.row, p.column))

            # Check capture diagonal square left
            p = Position((self.position.row + 1, self.position.column - 1))
            if self.board._position_exists(*p.position):
                if self._is_there_opponent_piece(p):
                    self.moves_mat[p.row][p.column] = True
                    self.possibles.append((p.row, p.column))

            # Check capture diagonal square right
            p = Position((self.position.row + 1, self.position.column + 1))
            if self.board._position_exists(*p.position):
                if self._is_there_opponent_piece(p):
                    self.moves_mat[p.row][p.column] = True
                    self.possibles.append((p.row, p.column))

            # Check capture diagonal en Passant
            passant: Position = self.board.enPassantVulnerable
            if (passant is not None and
                    self.position.row == passant.row == 4 and
                    abs(self.position.column - passant.column) == 1):
                self.moves_mat[passant.row + 1][passant.column] = True
                self.possibles.append((passant.row + 1, passant.column))

    def __str__(self) -> str:
        if self.color == Color.WHITE:
            return '♙'
        return '♟'


class Rook(ChessPiece):
    def possible_moves(self) -> bool:
        self.moves_mat = [[False] * 8 for _ in range(8)]
        self.possibles = []

        # Searching moves for Rook
        for r, c in cross_moves.values():
            p = Position((self.position.row + r, self.position.column + c))
            while (self.board._position_exists(*p.position) and not
                    self.board._is_there_a_piece(*p.position)):
                self.moves_mat[p.row][p.column] = True
                self.possibles.append((p.row, p.column))
                p.row += r
                p.column += c
            if self.board._position_exists(*p.position):
                if self._is_there_opponent_piece(p):
                    self.moves_mat[p.row][p.column] = True
                    self.possibles.append((p.row, p.column))

    def __str__(self) -> str:
        if self.color == Color.WHITE:
            return '♖'
        return '♜'


class Knight(ChessPiece):
    def _can_move(self, position: Position):
        row, column = position.position
        p = self.board._pieces[row][column]
        return p is None or p.color != self.color

    def possible_moves(self):
        self.moves_mat = [[False] * 8 for _ in range(8)]
        self.possibles = []

        # Searching moves for Knight
        for r, c in knight_moves.values():
            p = Position((self.position.row + r, self.position.column + c))
            if (self.board._position_exists(*p.position) and
                    self._can_move(p)):
                self.moves_mat[p.row][p.column] = True
                self.possibles.append((p.row, p.column))

    def __str__(self) -> str:
        if self.color == Color.WHITE:
            return '♘'
        return '♞'


class Bishop(ChessPiece):
    def possible_moves(self) -> bool:
        self.moves_mat = [[False] * 8 for _ in range(8)]
        self.possibles = []

        # Searching moves for Bishop
        for r, c in x_moves.values():
            p = Position((self.position.row + r, self.position.column + c))
            while (self.board._position_exists(*p.position) and not
                    self.board._is_there_a_piece(*p.position)):
                self.moves_mat[p.row][p.column] = True
                self.possibles.append((p.row, p.column))
                p.row += r
                p.column += c
            if self.board._position_exists(*p.position):
                if self._is_there_opponent_piece(p):
                    self.moves_mat[p.row][p.column] = True
                    self.possibles.append((p.row, p.column))

    def __str__(self) -> str:
        if self.color == Color.WHITE:
            return '♗'
        return '♝'


class Queen(ChessPiece):
    def possible_moves(self) -> bool:
        self.moves_mat = [[False] * 8 for _ in range(8)]
        self.possibles = []

        # Searching moves for Queen
        for r, c in moves_all.values():
            p = Position((self.position.row + r, self.position.column + c))
            while (self.board._position_exists(*p.position) and not
                    self.board._is_there_a_piece(*p.position)):
                self.moves_mat[p.row][p.column] = True
                self.possibles.append((p.row, p.column))

                p.row += r
                p.column += c
            if self.board._position_exists(*p.position):
                if self._is_there_opponent_piece(p):
                    self.moves_mat[p.row][p.column] = True
                    self.possibles.append((p.row, p.column))

    def __str__(self) -> str:
        if self.color == Color.WHITE:
            return '♕'
        return '♛'


class King(ChessPiece):
    def __init__(self, color: Color, position: Position, board) -> None:
        super().__init__(color, position, board)
        self._queen_side_castling: bool = False
        self._king_side_castling: bool = False

    @property
    def queen_side_castling(self):
        return self._queen_side_castling

    @queen_side_castling.setter
    def queen_side_castling(self, value: bool):
        self._queen_side_castling = value

    @property
    def king_side_castling(self):
        return self._king_side_castling

    @king_side_castling.setter
    def king_side_castling(self, value: bool):
        self._king_side_castling = value

    def _can_move(self, position: Position):
        row, column = position.position
        p = self.board._pieces[row][column]
        return p is None or p.color != self.color

    def possible_moves(self):
        self.moves_mat = [[False] * 8 for _ in range(8)]
        self.possibles = []

        # special castling move
        row = self.position.row
        if self._queen_side_castling:
            self.moves_mat[row][2] = True
            self.possibles.append((row, 2))

        if self._king_side_castling:
            self.moves_mat[row][6] = True
            self.possibles.append((row, 6))

        # Searching moves for King
        for r, c in moves_all.values():
            p = Position((self.position.row + r, self.position.column + c))
            if (self.board._position_exists(*p.position) and
                    self._can_move(p)):
                self.moves_mat[p.row][p.column] = True
                self.possibles.append((p.row, p.column))

    def __str__(self) -> str:
        if self.color == Color.WHITE:
            return '♔'
        return '♚'
