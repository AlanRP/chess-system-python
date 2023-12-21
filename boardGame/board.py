from boardGame.utility import Color, Position
from boardGame.chess_piece import King, Rook, Knight, Bishop, Queen, Pawn
from boardGame.piece import Piece
from boardGame.player import Player
from termcolor import cprint


class Board:
    def __init__(self, player1: Player, player2) -> None:
        self._pieces = [[None] * 8 for _ in range(8)]
        self.player1 = player1
        self.player2 = player2
        self.removed_pieces = []

    # todo -> to evaluate whether I create a separate class for the interface.

    def piece(self, row, column):
        return self._pieces[[row], [column]]

    def piece_pos(self, position):
        return self._pieces[[position.row], [position.column]]

    def place_piece(self, piece: Piece):
        row, column = piece.position.position

        if self._is_there_a_piece(*piece.position.position):
            self.removed_pieces.append(self.remove_piece(row, column))

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

    def _get_square_color(self, invert, possible_move):
        if possible_move:
            if invert:
                return "on_blue"
            return "on_cyan"
        if not invert:
            return "on_black"
        return None

    def display(self, possible_moves):
        invert = False  # Flag to alternate between white and black square
        cprint(f'\t{self.player2} <Black>\n', "dark_grey")

        for i, row in enumerate(self._pieces):

            cprint(f'\t{8 - i}', "dark_grey", end='  ')

            for j, p in enumerate(row):

                # square = None if invert else "on_black"
                square = self._get_square_color(invert, possible_moves[i][j])

                cprint(
                    self._get_piece(p),
                    self._get_piece_color(p),
                    square, end='')

                invert = not invert

            self._print_removed(i - 2)

            invert = not invert
            print()

        cprint('\t    a  b  c  d  e  f  g  h ', "dark_grey")
        cprint(f"\n\t{self.player1} <White>", "dark_grey")

        # self._print_removed()

    def _get_piece(self, piece: Piece):
        return '   ' if piece is None else f' {piece} '

    def _get_piece_color(self, piece: Piece):
        if piece is None:
            return None
        if piece.color.name == 'WHITE':
            return "white"
        return "red"

    def _print_removed(self, index):
        if not len(self.removed_pieces):
            return
        if index == 0:
            cprint('  Captured:', 'dark_grey', end='')
        elif index == 3:
            cprint('   [ ', 'dark_grey', end='')
            for p in self.removed_pieces:
                if p.color.name == 'BLACK':
                    cprint(p, 'red', end=' ')
            cprint(']', 'dark_grey', end='')
        elif index == 1:
            cprint('   [ ', 'dark_grey', end='')
            for p in self.removed_pieces:
                if p.color.name == 'WHITE':
                    print(p, end=' ')
            cprint(']', 'dark_grey', end='')
        else:
            return

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

    def _checkSeletion(self,  player, from_square) -> bool:
        row, column = Position(from_square).position

        if not self._is_there_a_piece(row, column):
            input(
                f"There is no piece on '{from_square}'. <Enter>")
            return False

        if not self._position_exists(row, column):
            input(
                f"Position '{from_square}' doen't exist on board. <Enter>")
            return False

        piece: Piece = self._pieces[row][column]

        if piece.color != player.color:
            input(
                f"The {piece.color.name.lower()} piece {piece} "
                f"on '{from_square}' is not yours. <Enter>")
            return False

        return True

    def _possibleMoves(self, player, from_square) -> bool:
        row, column = Position(from_square).position

        piece: Piece = self._pieces[row][column]

        piece.possible_moves()
        if not piece.is_there_any_possible_move():
            input(
                f"There is NO possible moves for the chosen "
                f"piece {piece} on '{from_square}'. <Enter>"
            )
            raise ''
        return piece.moves_mat

    def move_piece(self, player, from_square, to_square) -> bool:

        row, column = Position(from_square).position
        to_row, to_column = Position(to_square).position

        if not self._position_exists(to_row, to_column):
            input(
                f"Position '{from_square}' doen't exist on board. <Enter>")
            return False

        if not self._validate_target_position(row, column, to_row, to_column):
            return False

        piece = self.remove_piece(row, column)

        piece.position = Position(to_square)
        self.place_piece(piece)

        return True

    def _validate_target_position(self, row, column, to_row, to_column):
        p = self._pieces[row][column]

        if p is not None and not p.moves_mat[to_row][to_column]:
            input("The piece can't move there.'<enter>'")
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
