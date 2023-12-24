from termcolor import cprint
from boardGame.UI import UI
from boardGame.board import Board
from boardGame.chess_piece import ChessPiece, King
from boardGame.piece import Piece
from boardGame.player import Player
from boardGame.utility import Color, Position
import os


class ChessGame:
    def __init__(
            self,
            board: Board,
            player1: Player,
            player2: Player,
            _piece: ChessPiece | None = None
    ):
        self._board = board
        self._player1 = player1
        self._player2 = player2
        self._UI = UI(self._board, self._player1, self._player2)
        self.turn = True
        self.check = False
        self.checkmate = False

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
                        continue

                    possible_moves = self._possibleMoves(from_square)

                    self._UI.display_game(possible_moves)

                    to_square = self._UI.get_target_move(player)

                    if not self._validate_target(from_square, to_square):
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

    def _possibleMoves(self, from_square) -> bool:
        row, column = Position(from_square).position

        piece: Piece = self._board.piece(row, column)

        piece.possible_moves()
        if not piece.is_there_any_possible_move():
            self.warning(
                f"There is NO possible moves for the chosen "
                f"piece {piece} on '{from_square}'."
            )
            raise ''
        return piece.moves_mat

    def _move_piece(self, from_square, to_square, color) -> bool:
        captured = self._perform_move(from_square, to_square)

        if self._is_check(color):
            self._board._undo_move(from_square, to_square, captured)
            self.warning("You cannot let your king in check.")
            return False

        self._piece.increase_move_count()
        self._piece = None

        if self._is_checkmate(self._opponent_color(color)):
            self.checkmate = True
            self._UI.display_game_over(self._current_player())

        return True

    def _perform_move(self, from_square, to_square) -> Piece:

        row, column = Position(from_square).position
        self._piece = self._board._remove_piece(row, column)
        self._piece.position = Position(to_square)
        return self._board._place_piece(self._piece)  # captured piece

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
