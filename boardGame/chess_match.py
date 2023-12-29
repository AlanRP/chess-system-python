from termcolor import cprint
from boardGame.UI import UI
from boardGame.board import Board
from boardGame.chess_piece import (
    Bishop, ChessPiece, King, Knight, Pawn, Queen, Rook)
from boardGame.piece import Piece
from boardGame.player import Player
from boardGame.utility import Color, Position


class ChessMatch:
    def __init__(
            self,
            board: Board,
            player1: str = 'player1',
            player2: str = 'player2'
    ):
        self._board = board
        self._player1 = Player(player1, Color(1))
        self._player2 = Player(player2, Color(2))
        self._UI = UI(self._board, self._player1, self._player2)
        self.turn = True
        self.check = False
        self.checkmate = False
        self.stalemate = False
        self._piece: ChessPiece | None = None

    def _move_piece(self, from_square, to_square, color: Color) -> bool:
        """
        Logic to perform the movement of the piece.

        First we have to check if the movement is rock,
        or if it is en passant.
        After the movement we have to check if the movement is a promotion.
        Then check if the king itself was checked, if so, return the piece.
        Next, we check whether the opponent is in check or checkmate.
        And finally we check if the movement caused the possibility of
        en passant for the next movement.
        """

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

        promoted = self._promotion(color, from_square, to_square)

        if self._is_check(color):
            if promoted:
                # returan pawn before undo
                self._replace_piece(color, Position(to_square), Pawn)
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

        if self.is_game_over(self._opponent_color(color)):
            if self.checkmate:
                self._UI.display_game_over(self._current_player())
            elif self.stalemate:
                self._UI.display_stalemate(self._opponent_color(color))

        if isinstance(self._piece, Pawn):
            self._possible_enPassant(from_square, to_square)

        return True

    def _validate_target(self, from_square, to_square) -> bool:
        """
        Checks whether the input typed as "target move" is valid.
        """
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
        """
        Checks whether the input typed as "source move" is valid.
        """
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

    def _is_enPassant_move(self, from_square, to_square, color) -> bool:
        """
        Checks whether the current move is an "En Passant"
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

    def _perform_enPassant(self, from_square, to_square) -> Piece:
        """
        Performs the special move - en Passant
        """
        passant_square = self._board.enPassantVulnerable.square
        self._perform_move(passant_square, to_square)
        self._perform_move(from_square, to_square)

    def _possible_enPassant(self, from_square, to_square):
        """
        After current move, check possible en Passant for next move
        """
        self._board.enPassantVulnerable = None
        from_row = Position(from_square).row
        to_row = Position(to_square).row
        if abs(to_row - from_row) == 2:
            self._board.enPassantVulnerable = self._piece.position

    def _promotion(self, color, from_square, to_square) -> True:
        """
        Checks whether the current move is a promotion, if so, executes it.
        """

        if self._piece is None or not isinstance(self._piece, Pawn):
            return False

        if (color == Color.WHITE and self._piece.position.row != 0 or
                color == Color.BLACK and self._piece.position.row != 7):
            return False

        _piece = self._pick_a_piece(from_square, to_square)

        position = self._piece.position

        self._replace_piece(color, position, _piece)

        return True

    def _pick_a_piece(self, from_square, to_square) -> Piece:
        """
        Method to chose a piece to replace in case of promotion
        """

        move = f"'{from_square} - {to_square}'"
        letter = "_"

        while letter not in 'QRBN':
            self._UI.display_game()
            print()
            cprint(f"Move {move} - Promotion", "yellow")
            print()
            letter = input("Choose a piece for promotion Q | R | B | N: ")
            letter = letter.strip().upper()

        return self._select_piece(letter)

    def _select_piece(self, letter) -> ChessPiece:
        """
        Return a piece, acording the entered letter
        """
        if letter == "R":
            return Rook
        if letter == "B":
            return Bishop
        if letter == "N":
            return Knight
        return Queen

    def _replace_piece(self, color,  position, piece: ChessPiece):
        """
        Replaces a piece on given position
        """
        self._board._pieces[position.row][position.column] = None
        self._board._place_piece(piece(color, position, self._board))

    def _perform_move(self, from_square: str, to_square: str) -> ChessPiece:
        """
        Method for performing the move of the piece
        """
        row, column = Position(from_square).position
        self._piece = self._board._remove_piece(row, column)
        self._piece.position = Position(to_square)
        return self._board._place_piece(self._piece)  # captured piece

    def _possibleMoves(self, from_square) -> list:
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
            return None
        return piece.moves_mat

    def _possible_L_castling(self, piece: ChessPiece) -> bool:
        """
        Check if it is possible to make the big castling, (Left side)
        before looking for the king's possible moves.
        """

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
        """
        Check if it is possible to make the small castling, (Right side)
        before looking for the king's possible moves.
        """

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
        check if it is a castle move

        returns -> 0, 1, 2
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
        """
        Perform the castle movement.

        Perform the rock movement, both on the king's side
        and on the queen's side.
        Executes it in two stages, to check that the King
        is not in check on the movement path.
        Complete movement with the Rook.
        """
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

    def _opponent_color(self, color: Color) -> Color:
        """Returns the opposite color"""
        return Color.BLACK if color == Color.WHITE else Color.WHITE

    def _opponent_pieces(self, color: Color) -> list:
        """
        Returns the list of pieces on the board in the opposite color to the
        selected one.
        """
        def p_color(p):
            return p is not None and p.color == self._opponent_color(color)

        _pieces = self._board._pieces

        return [p for sub_lst in _pieces for p in sub_lst if p_color(p)]

    def _one_color_pieces(self, color: Color, king_first=False) -> list:
        """
        Returns the list of chess pieces on board in the selected color.

        If king_first, it will be the first in the list result,
        to give more performance when checking if it is not in check.
        """
        pieces = []
        for row_list in self._board._pieces:
            for p in row_list:
                if p is not None and p.color == color:
                    if king_first and isinstance(p, King):
                        pieces.insert(0, p)
                    else:
                        pieces.append(p)
        return pieces

    def _is_check(self, color: Color) -> bool:
        """
        Checks if the king in the selected 'color' is in 'check'.
        """
        row, col = self._search_king_position(color)
        # pieces = self._opponent_pieces(color)
        opponent_pieces = self._one_color_pieces(self._opponent_color(color))

        for p in opponent_pieces:
            p.possible_moves()
            if (row, col) in p.possibles:
                return True
        return False

    def is_game_over(self, color: Color) -> bool:
        """
        Tests: < check >  < checkmate >  < stalemate >

        If check and there's no move = checkmate
        If not check and there's no move = stalemate
        """
        self.check = self._is_check(color)

        if self.check:
            self.stalemate = False
            self.checkmate = self._is_possible_move(color)
        else:
            self.checkmate = False
            self.stalemate = self._is_possible_move(color)

        return self.checkmate or self.stalemate

    def _is_possible_move(self, color) -> bool:
        """
        Tests is there is a possible move for next player
        """
        pieces = self._one_color_pieces(color, True)
        for p in pieces:
            for i, j in p.possibles:
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

    def _search_king_position(self, color: Color) -> tuple:
        """
            Returns the 'row' and 'column' of the King's position
            in the selected 'color'.
        """
        for row in self._board._pieces:
            for p in row:
                if (p is not None and isinstance(p, King)
                        and p.color == color):
                    return p.position.position

        raise LookupError(f"Not found {color.name} king on the board.")

    def _position_exists(self, row, column) -> bool:
        """
        Checks if the position (row, column) is within the chessboard, 8 x 8.
        """
        return row >= 0 and row < 8 and column >= 0 and column < 8

    def _square_exists(self, s: str) -> bool:
        """
        Checks if the position is within the chessboard, 8 x 8.
        Receives a str as a parameter, for example: "a2", "h8"
        """
        return (len(s) == 2 and s[0] >= "a" and s[0]
                <= "h" and s[1] >= "1" and s[1] <= "8")

    def _is_there_a_piece(self, row: int, column: int) -> bool:
        """
        Checks if there is a chess piece in the selected position (row column).
        """
        return self._board._pieces[row][column] is not None

    def warning(self, msg: str):
        """Returns alert or warning messages to the user."""
        cprint(msg,  'yellow', end=' ')
        input("<Enter>")

    def _current_player(self) -> Player:
        """
        Change the player's turn.
        Returns the current player.
        """
        if self.turn:
            return self._player1
        return self._player2
