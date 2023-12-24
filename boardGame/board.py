from boardGame.utility import Color, Position
from boardGame.chess_piece import King, Rook, Knight, Bishop, Queen, Pawn
from boardGame.piece import Piece


class Board:
    def __init__(self) -> None:
        self._pieces = [[None] * 8 for _ in range(8)]
        self._removed_pieces = []

    def piece(self, row: int, column: int) -> Piece | None:
        return self._pieces[row][column]

    def piece_pos(self, position):
        return self._pieces[[position.row], [position.column]]

    def _place_piece(self, piece: Piece):
        row, column = piece.position.position
        captured = None
        if self._is_there_a_piece(*piece.position.position):
            captured = self._remove_piece(row, column)
            self._removed_pieces.append(captured)
        self._pieces[row][column] = piece
        return captured

    def setup_board(self):

        self._place_piece(Rook(Color.BLACK, Position('a8'), self))
        self._place_piece(Knight(Color.BLACK, Position('b8'), self))
        self._place_piece(Bishop(Color.BLACK, Position('c8'), self))
        self._place_piece(Queen(Color.BLACK, Position('d8'), self))
        self._place_piece(King(Color.BLACK, Position('e8'), self))
        self._place_piece(Bishop(Color.BLACK, Position('f8'), self))
        self._place_piece(Knight(Color.BLACK, Position('g8'), self))
        self._place_piece(Rook(Color.BLACK, Position('h8'), self))

        for col in 'abcdefgh':
            self._place_piece(Pawn(Color.WHITE, Position(col + '2'), self))
            self._place_piece(Pawn(Color.BLACK, Position(col + '7'), self))

        self._place_piece(Rook(Color.WHITE, Position('a1'), self))
        self._place_piece(Knight(Color.WHITE, Position('b1'), self))
        self._place_piece(Bishop(Color.WHITE, Position('c1'), self))
        self._place_piece(Queen(Color.WHITE, Position('d1'), self))
        self._place_piece(King(Color.WHITE, Position('e1'), self))
        self._place_piece(Bishop(Color.WHITE, Position('f1'), self))
        self._place_piece(Knight(Color.WHITE, Position('g1'), self))
        self._place_piece(Rook(Color.WHITE, Position('h1'), self))

    def _remove_piece(self, row: int, column: int) -> Piece:
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

    def _undo_move(self, from_square, to_square, captured_piece: Piece):
        row, column = Position(to_square).position

        p = self._remove_piece(row, column)
        p.position = Position(from_square)

        self._place_piece(p)

        if captured_piece is not None:
            captured_piece.position = Position(to_square)
            self._place_piece(captured_piece)
            if len(self._removed_pieces):
                self._removed_pieces.pop()

    def is_stalemate(self):
        ...
        # verificar se está empatado.
