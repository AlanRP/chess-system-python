from boardGame.utility import Color, Position
from boardGame.piece import (Piece, King, Rook, Knight, Bishop, Queen, Pawn)


class Board:
    def __init__(self) -> None:
        self._pieces = [[None] * 8 for _ in range(8)]

    # todo -> to evaluate whether I create a separate class for the interface.

    def piece(self, row, column):
        return self._pieces[[row], [column]]

    def piece_pos(self, position):
        return self._pieces[[position.row], [position.column]]

    def place_piece(self, piece: Piece):
        if self._is_there_a_piece(piece.position):
            raise IndexError(
                f'There is already a piece on '
                f'Position{piece.position.position}')

        row, column = piece.position.position
        self._pieces[row][column] = piece

    def setup_board(self):

        self.place_piece(Rook(Color.BLACK, Position('a8')))
        self.place_piece(Knight(Color.BLACK, Position('b8')))
        self.place_piece(Bishop(Color.BLACK, Position('c8')))
        self.place_piece(Queen(Color.BLACK, Position('d8')))
        self.place_piece(King(Color.BLACK, Position('e8')))
        self.place_piece(Bishop(Color.BLACK, Position('f8')))
        self.place_piece(Knight(Color.BLACK, Position('g8')))
        self.place_piece(Rook(Color.BLACK, Position('h8')))

        for col in 'abcdefgh':
            self.place_piece(Pawn(Color.WHITE, Position(col + '2')))
            self.place_piece(Pawn(Color.BLACK, Position(col + '7')))

        self.place_piece(Rook(Color.WHITE, Position('a1')))
        self.place_piece(Knight(Color.WHITE, Position('b1')))
        self.place_piece(Bishop(Color.WHITE, Position('c1')))
        self.place_piece(Queen(Color.WHITE, Position('d1')))
        self.place_piece(King(Color.WHITE, Position('e1')))
        self.place_piece(Bishop(Color.WHITE, Position('f1')))
        self.place_piece(Knight(Color.WHITE, Position('g1')))
        self.place_piece(Rook(Color.WHITE, Position('h1')))

    def print_piece(self, piece: Piece):
        if not piece:
            print(' ', end=' ')
        else:
            print(piece, end=' ')

    def display(self):
        invert = False  # Flag to alternate between white and black square

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

        print('\n\t     a  b  c  d  e  f  g  h ')

    def remove_piece(self, position: str):

        if not self._position_exists(Position(position)):
            raise ValueError('Position not on the board')

        row, column = Position(position).position

        piece = self._pieces[row][column]
        self._pieces[row][column] = None
        piece.position = None
        return piece

    def _position_exists(self, position: Position) -> bool:
        row, column = position.position
        return row >= 0 and row < 8 and column >= 0 and column < 8

    def _is_there_a_piece(self, position: Position):
        if not self._position_exists(position):
            raise IndexError('Position not on the board.')
        row, column = position.position
        return self._pieces[row][column] is not None

    def move_piece(self, player, from_square, to_square) -> bool:

        from_position = Position(from_square)
        to_position = Position(to_square)

        if not self._position_exists(to_position):
            return False

        if not self._is_there_a_piece(from_position):
            # print(f"There is no piece on position '{from_square}'")
            return False

        if not self._position_exists(from_position):
            return False
        row, column = from_position.position
        piece = self._pieces[row][column]

        if piece.color != player.color:
            return False

        piece = self.remove_piece(from_square)

        piece.position = to_position
        self.place_piece(piece)

        return True

        # todo -> Verificar se a peça from_square é do jogador atual
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
