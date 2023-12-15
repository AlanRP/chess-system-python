from boardGame.utility import Color, Position
from boardGame.piece import (Piece, King, Rook, Knight, Bishop, Queen, Pawn)


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
        self._pieces[row][column] = piece

    def setup_board(self):

        self.place_piece(Rook(self, Color.BLACK, Position('a8')))
        self.place_piece(Knight(self, Color.BLACK, Position('b8')))
        self.place_piece(Bishop(self, Color.BLACK, Position('c8')))
        self.place_piece(Queen(self, Color.BLACK, Position('d8')))
        self.place_piece(King(self, Color.BLACK, Position('e8')))
        self.place_piece(Bishop(self, Color.BLACK, Position('f8')))
        self.place_piece(Knight(self, Color.BLACK, Position('g8')))
        self.place_piece(Rook(self, Color.BLACK, Position('h8')))

        for col in 'abcdefgh':
            self.place_piece(Pawn(self, Color.WHITE, Position(col + '2')))
            self.place_piece(Pawn(self, Color.BLACK, Position(col + '7')))

        self.place_piece(Rook(self, Color.WHITE, Position('a1')))
        self.place_piece(Knight(self, Color.WHITE, Position('b1')))
        self.place_piece(Bishop(self, Color.WHITE, Position('c1')))
        self.place_piece(Queen(self, Color.WHITE, Position('d1')))
        self.place_piece(King(self, Color.WHITE, Position('e1')))
        self.place_piece(Bishop(self, Color.WHITE, Position('f1')))
        self.place_piece(Knight(self, Color.WHITE, Position('g1')))
        self.place_piece(Rook(self, Color.WHITE, Position('h1')))

    def print_piece(self, piece: Piece):
        if not piece:
            print(' ', end=' ')
        else:
            print(piece, end=' ')

    def display(self):
        invert = False
        for i, row in enumerate(self._pieces):
            print('\t', 8 - i, end='  ')

            for j in row:
                if invert:
                    print('\33[100m ', end='')  # White square color
                else:
                    print('\33[0m ', end='')  # Black square color
                invert = not invert
                self.print_piece(j)

            invert = not invert

            print('\33[0m' + '')
            # print()
        print('\n\t     a  b  c  d  e  f  g  h ')

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
