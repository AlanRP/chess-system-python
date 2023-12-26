from termcolor import cprint
from boardGame.UI import UI
from boardGame.board import Board
from boardGame.chess_piece import ChessPiece, King, Pawn, Rook
from boardGame.piece import Piece
from boardGame.player import Player
from boardGame.utility import Color, Position
import os


class ChessGame:
    def __init__(
            self,
            board: Board,
            player1: Player,
            player2: Player
    ):
        self._board = board
        self._player1 = player1
        self._player2 = player2
        self._UI = UI(self._board, self._player1, self._player2)
        self.turn = True
        self.check = False
        self.checkmate = False
        self._piece: ChessPiece | None = None

    def play(self):
        self._board.setup_board()
        msg = None

        while not self.is_game_over():
            move_made = False
            from_square = None
            to_square = None
            player = self._current_player()

            while not move_made:
                possible_moves = [[False] * 8 for _ in range(8)]

                try:
                    self._UI.display_game(possible_moves)

                    self.check = self._is_check(player.color)
                    self._UI.print_msg(msg, self.check)

                    from_square = self._UI.get_source_move(player)

                    if not self._validate_source(player, from_square):
                        msg = (f"Invalid source seletion: "
                               f"'{from_square}', try again.")
                        continue

                    possible_moves = self._possibleMoves(from_square)

                    self._UI.display_game(possible_moves)

                    to_square = self._UI.get_target_move(player)

                    if not self._validate_target(from_square, to_square):
                        msg = (f"Invalid source seletion: "
                               f"'{to_square}', try again.")
                        continue

                    move_made = self._move_piece(
                        from_square, to_square, player.color)

                    if move_made:
                        msg = None
                    else:
                        msg = f"Invalid move ('{from_square}' "\
                            f"'{to_square}'), try again."

                except Exception as e:
                    if to_square is None:
                        msg = f"Invalid seletion ('{from_square}'), try again"
                    else:
                        msg = (f"Invalid move ('{from_square}' "
                               f"'{to_square}'), try again.\n{e}")

            self.turn = not self.turn

        print('Game Over!')

    def _is_enPassant_move(self, from_square, to_square, color) -> bool:
        """
            Verify if is an "En Passant" move
        """
        self._piece = self._board.piece_from_square(from_square)

        if (not isinstance(self._piece, Pawn) or
                self._board.enPassantVulnerable is None):
            return False

        if (color == Color.WHITE and
                Position(from_square).row != 3):
            return False

        if (color == Color.BLACK and
                Position(from_square).row != 4):
            return False

        passant: Position = self._board.enPassantVulnerable
        to_col = Position(to_square).column

        if passant.column != to_col:
            return False

        return True

    def _move_piece(self, from_square, to_square, color) -> bool:

        _castling_side = self._is_castling_move(from_square, to_square)
        castling_ok = True

        en_passant = self._is_enPassant_move(from_square, to_square, color)

        if _castling_side:
            castling_ok = self._perform_castling(
                from_square, to_square, color, _castling_side)

        elif en_passant:

            captured = self._perform_enPassant(from_square, to_square)
        else:
            captured = self._perform_move(from_square, to_square)

        if self._is_check(color):
            self._board._undo_move(from_square, to_square, captured)

            if en_passant:
                p_removed = self._board._removed_pieces.pop()
                p_removed.position = self._board.enPassantVulnerable
                self._board._place_piece(p_removed)

            self.warning("You cannot let your king in check.")
            return False

        # If the caltling move is not successful,
        # neither increases move_count nor passes the turn
        if _castling_side and not castling_ok:
            return False

        self._piece.increase_move_count()
        # self._piece = None

        if self._is_checkmate(self._opponent_color(color)):
            self.checkmate = True
            self._UI.display_game_over(self._current_player())

        if isinstance(self._piece, Pawn):
            self._possible_enPassant(from_square, to_square)

        return True

    def _possible_enPassant(self, from_square, to_square):
        self._board.enPassantVulnerable = None
        from_row = Position(from_square).row
        to_row = Position(to_square).row
        if abs(to_row - from_row) == 2:
            self._board.enPassantVulnerable = self._piece.position

    def _perform_enPassant(self, from_square, to_square) -> Piece:
        passant_square = self._board.enPassantVulnerable.square
        self._perform_move(passant_square, to_square)
        self._perform_move(from_square, to_square)

    def _perform_move(self, from_square, to_square) -> Piece:

        row, column = Position(from_square).position
        self._piece = self._board._remove_piece(row, column)
        self._piece.position = Position(to_square)
        return self._board._place_piece(self._piece)  # captured piece

    def _possibleMoves(self, from_square) -> bool:
        row, column = Position(from_square).position

        piece: Piece = self._board.piece(row, column)

        if isinstance(piece, King):
            piece.queen_side_castling = self._possible_L_castling(piece)
            piece.king_side_castling = self._possible_R_castling(piece)

        piece.possible_moves()
        if not piece.is_there_any_possible_move():
            self.warning(
                f"There is NO possible moves for the chosen "
                f"piece {piece} on '{from_square}'."
            )
        return piece.moves_mat

    def _possible_L_castling(self, piece: ChessPiece):

        # L castling is the queen side castling
        if self.check or piece.move_count > 0:
            return False

        row = piece.position.row

        _rook: Rook | None = None
        _rook = self._board._pieces[row][0]

        if (not isinstance(_rook, Rook) or _rook.move_count > 0):
            return False

        if self._board._pieces[row][1:4] != [None, None, None]:
            return False
        return True

    def _possible_R_castling(self, piece: ChessPiece) -> bool:

        # L castling is the king side castling
        if self.check or piece.move_count > 0:
            return False

        row = piece.position.row

        _rook: Rook | None = None
        _rook = self._board._pieces[row][7]

        if (not isinstance(_rook, Rook) or _rook.move_count > 0):
            return False

        if self._board._pieces[row][5:7] != [None, None]:
            return False
        return True

    def _is_castling_move(self, from_square, to_square) -> int:
        """
            possible return -> 0, 1, 2
            - 0 not castling
            - 1 king side castling
            - 2 queen side castling
        """
        self._piece = self._board.piece_from_square(from_square)
        if not isinstance(self._piece, King):
            return 0

        to_col = Position(to_square).column
        from_col = Position(from_square).column
        if from_col == 4:       # Initial position
            if to_col == 6:     # Column 'F' King side castling
                return 1
            elif to_col == 2:   # Column 'B' Queen side castling
                return 2
        return 0

    def _perform_castling(self, from_square, to_square, color, side) -> bool:
        # side 1 = King  side castling
        # side 2 = Queen side castling
        row, col = Position(from_square).position
        col = (col + 1) if side == 1 else (col - 1)

        _rook_col = 7 if side == 1 else 0

        midlle_square = Position((row, col)).square
        _rook_square = Position((row, _rook_col)).square

        self._perform_move(from_square, midlle_square)

        if self._is_check(color):
            self._board._undo_move(from_square, midlle_square, None)
            self.warning(
                f"Cannot castling because square "
                f"'{midlle_square}' is in check")
            return False

        self._perform_move(midlle_square, to_square)
        self._piece.increase_move_count()
        _piece = self._piece
        self._perform_move(_rook_square, midlle_square)

        if self._is_check(color):
            self._board._undo_move(_rook_square, midlle_square, None)
            self._board._undo_move(from_square, to_square, None)
            self.warning("You cannot let your king in check.")
            self._piece = _piece
            self._piece.decrease_move_count()
            return False

        return True

    def _validate_target(self, from_square, to_square):

        if not self._square_exists(to_square):
            self.warning(f"Position '{to_square}' doen't exist on board.")
            return False

        row, column = Position(to_square).position

        p = self._board.piece(*Position(from_square).position)
        if p is not None and not p.moves_mat[row][column]:
            self.warning(f"The piece {p} cannot move there.")
            return False
        return True

    def _validate_source(self,  player, from_square) -> bool:

        if not self._square_exists(from_square):
            self.warning(f"Position '{from_square}' doen't exist on board.")
            return False

        row, column = Position(from_square).position

        if not self._is_there_a_piece(row, column):
            self.warning(f"There is no piece on '{from_square}'.")
            return False

        piece = self._board.piece(row, column)
        if piece.color != player.color:
            self.warning(f"The {piece.color.name.lower()} piece {piece} "
                         f"on '{from_square}' is not yours.")
            return False

        return True

    def _opponent_color(self, color):
        return Color.BLACK if color == Color.WHITE else Color.WHITE

    def _is_check(self, color: Color) -> bool:
        king_ = self._search_piece(color)
        row, col = king_.position.position
        for r in self._board._pieces:
            for p in r:
                if p is not None and p.color == self._opponent_color(color):
                    p.possible_moves()
                    if p.moves_mat[row][col]:
                        return True
        return False

    def _is_checkmate(self, color: Color) -> bool:
        if not self._is_check(color):
            return False
        pieces = []
        for row_list in self._board._pieces:
            for p in row_list:
                if p is not None and p.color == color:
                    pieces.append(p)
        for p in pieces:
            p.possible_moves()
            for i in range(7):
                for j in range(7):
                    if p.moves_mat[i][j]:
                        from_square = p.position.square
                        to_square = Position((i, j)).square

                        captured = self._perform_move(from_square, to_square)
                        check = self._is_check(color)
                        self._board._undo_move(
                            from_square, to_square, captured)
                        if not check:
                            return False

        return True

    def _search_piece(self, color: Color, piece: Piece = King) -> Piece:
        for row in self._board._pieces:
            for p in row:
                if (p is not None and isinstance(p, piece)
                        and p.color == color):
                    return p
        raise LookupError(f"Not found {color.name} king on the board.")

    def _position_exists(self, row, column) -> bool:
        return row >= 0 and row < 8 and column >= 0 and column < 8

    def _square_exists(self, s: str) -> bool:
        return (len(s) == 2 and s[0] >= "a" and s[0]
                <= "h" and s[1] >= "1" and s[1] <= "8")

    def _is_there_a_piece(self, row, column):
        return self._board._pieces[row][column] is not None

    def warning(self, msg):
        cprint(msg,  'yellow', end=' ')
        input("<Enter>")

    def _current_player(self):
        if self.turn:
            return self._player1
        return self._player2

    def is_game_over(self):
        return self.checkmate
        # return self.is_checkmate() or self._board.is_stalemate()


if __name__ == '__main__':

    os.system("cls")
    print("\t*** Welcome to CHESS ***\n\n")
    name1 = input('Enter the name of the WHITE player: ')
    name2 = input('Enter the name of the BLACK player: ')

    match = ChessGame(
        Board(),
        Player(name1, Color(1)),
        Player(name2, Color(2))
    )
    match.play()
