from boardGame.utility import Color, Position
from boardGame.piece import (Piece, King, Rook)


class Board:
    # todo -> to evaluate whether I wil really need rows and column here
    def __init__(self, rows: int, columns: int) -> None:
        self._rows = rows
        self._columns = columns
        self._pieces = [[None] * self._rows for _ in range(self._columns)]

    @property
    def rows(self):
        return self._rows

    @rows.setter
    def rows(self, value):
        self._rows = value

    @property
    def columns(self):
        return self._columns

    @columns.setter
    def columns(self, value):
        self._columns = value

    # @property
    # def pieces(Position):
    #     return self._pieces[[], []]

    # todo -> to evaluate whether I create a separate class for the interface.
    def piece(self, row, column):
        return self._pieces[[row], [column]]

    def piece_pos(self, position):
        return self._pieces[[position.row], [position.column]]

    def place_piece(self, piece: Piece):
        row = piece.position.row
        column = piece.position.column
        print(row, column)
        print('*'*20)
        self._pieces[row][column] = piece

    def setup_board(self):
        # todo -> implementar a configuração inicial do board
        # Adicionar peçars às casas.

        king = King(self, Color.BLACK, Position('e8'))

        self.place_piece(king)

        # self.place_piece(Rook(self, Color.BLACK), Position('a8'))
        # self.place_piece(King(self, Color.WHITE), Position('e1'))
        # self.place_piece(Rook(self, Color.WHITE), Position('a1'))
        # self.place_piece(Rook(self, Color.WHITE), Position('a8'))

    # avail

    def print_piece(self, piece: Piece):
        if not piece:
            print('-', end=' ')
        else:
            print(piece, end=' ')

    def display(self):
        for i, row in enumerate(self._pieces):
            print(8 - i, end=' ')
            for j in row:
                self.print_piece(j)
            print()
        print('  a b c d e f g h ')

    def move_piece(self, player, from_square, to_square) -> bool:
        ...
        # todo -> implementar a lógica para mover uma peça
        # verificar se a jogada é válida

    def is_valid_move(self, piece, to_square) -> bool:
        # todo -> implementar lógica de verificação do movimento.
        ...

    def is_checkmate(self):
        ...
        # todo -> implementar verificação de checkmate

    def is_stalemate(self):
        ...
        # verificar se está empatado.
