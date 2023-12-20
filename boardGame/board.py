from boardGame.utility import Color, Position
from boardGame.chess_piece import King, Rook, Knight, Bishop, Queen, Pawn
from boardGame.piece import Piece
from boardGame.player import Player


class Board:
    def __init__(self, player1: Player, player2) -> None:
        self._pieces = [[None] * 8 for _ in range(8)]
        self.player1 = player1
        self.player2 = player2

    # todo -> to evaluate whether I create a separate class for the interface.

    def piece(self, row, column):
        return self._pieces[[row], [column]]

    def piece_pos(self, position):
        return self._pieces[[position.row], [position.column]]

    def place_piece(self, piece: Piece):
        if self._is_there_a_piece(*piece.position.position):
            raise IndexError(
                f'There is already a piece on '
                f'Position{piece.position.position}')

        row, column = piece.position.position
        self._pieces[row][column] = piece

    def setup_board(self):

        self.place_piece(Rook(Color.BLACK, Position('a8'), self))
        self.place_piece(Knight(Color.BLACK, Position('b8'), self))
        self.place_piece(Bishop(Color.BLACK, Position('c8'), self))
        self.place_piece(Queen(Color.BLACK, Position('d8'), self))
        self.place_piece(King(Color.BLACK, Position('e8'), self))
        self.place_piece(Bishop(Color.BLACK, Position('f8'), self))
        self.place_piece(Knight(Color.BLACK, Position('g8'), self))
        self.place_piece(Rook(Color.BLACK, Position('h8'), self))

        for col in 'abcdefgh':
            self.place_piece(Pawn(Color.WHITE, Position(col + '2'), self))
            self.place_piece(Pawn(Color.BLACK, Position(col + '7'), self))

        self.place_piece(Rook(Color.WHITE, Position('a1'), self))
        self.place_piece(Knight(Color.WHITE, Position('b1'), self))
        self.place_piece(Bishop(Color.WHITE, Position('c1'), self))
        self.place_piece(Queen(Color.WHITE, Position('d1'), self))
        self.place_piece(King(Color.WHITE, Position('e1'), self))
        self.place_piece(Bishop(Color.WHITE, Position('f1'), self))
        self.place_piece(Knight(Color.WHITE, Position('g1'), self))
        self.place_piece(Rook(Color.WHITE, Position('h1'), self))

    def print_piece(self, piece: Piece):
        if not piece:
            print(' ', end=' ')
        else:
            print(piece, end=' ')

    def display(self):
        invert = False  # Flag to alternate between white and black square
        print(self.player2, '<Black>')
        for i, row in enumerate(self._pieces):
            print('\t', 8 - i, end='  ')

            for j in row:
                if invert:
                    print('\33[1;0;100m', end=' ')  # White square color
                else:
                    print('\33[1;0;40m', end=' ')  # Black square color
                invert = not invert
                self.print_piece(j)

            invert = not invert

            print('\33[0m' + '')
        print(self.player1, '<White>')
        print('\t     a  b  c  d  e  f  g  h ')

    def remove_piece(self, row, column):
        piece = self._pieces[row][column]
        self._pieces[row][column] = None
        piece.position = None
        return piece

    def _position_exists(self, row, column) -> bool:
        return row >= 0 and row < 8 and column >= 0 and column < 8

    def _is_there_a_piece(self, row, column):
        if not self._position_exists(row, column):
            raise IndexError('Position not on the board.')
        return self._pieces[row][column] is not None

    def move_piece(self, player, from_square, to_square) -> bool:

        from_position = Position(from_square)
        to_position = Position(to_square)

        if not self._position_exists(*to_position.position):
            input(
                f"Position '{from_square}' doen't exist on board. <Enter>")
            return False

        if not self._is_there_a_piece(*from_position.position):
            input(
                f"There is no piece on '{from_square}'. <Enter>")
            return False

        if not self._position_exists(*from_position.position):
            input(
                f"Position '{from_square}' doen't exist on board. <Enter>")
            return False

        row, column = from_position.position
        piece: Piece = self._pieces[row][column]

        if piece.color != player.color:
            input(
                f"The {piece.color.name.lower()} piece {piece} "
                f"on '{from_square}' is not yours. <Enter>")
            return False

        piece.possible_moves()
        if not piece.is_there_any_possible_move():
            input(
                f"There is NO possible moves for the chosen "
                f"piece {piece} on '{from_square}'. <Enter>"
            )
            return False

        if not self._validate_target_position(from_position, to_position):
            return False

        piece = self.remove_piece(*from_position.position)

        piece.position = to_position
        self.place_piece(piece)

        return True

    def _validate_target_position(self, source: Position, target: Position):
        row, column = source.position
        p = self._pieces[row][column]
        row, column = target.position
        if not p.moves_mat[row][column]:
            print("The piece can't move there.")
            input('<enter>')
            return False
        return True

    def is_valid_move(self, piece, to_square) -> bool:
        # todo -> implementar lógica de verificação do movimento.
        ...

    def is_checkmate(self):
        ...
        # todo -> implementar verificação de checkmate

    def is_stalemate(self):
        ...
        # verificar se está empatado.
