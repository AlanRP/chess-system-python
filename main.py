from termcolor import cprint
from boardGame.UI import UI
from boardGame.board import Board
from boardGame.chess_piece import King
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
        self._UI = UI(self._board)
        self._player1 = player1
        self._player2 = player2
        self.turn = True
        self.check = False

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
                    self._UI.display_game(
                        possible_moves, self._player1, self._player2)
                    self._UI.print_msg(msg, self.check)

                    print()
                    print(f"Waiting for {player} ({player.color.name})")

                    from_square = input("Source move: ")

                    if not self._checkSeletion(player, from_square):
                        raise ''

                    possible_moves = self._possibleMoves(from_square)

                    self._UI.display_game(
                        possible_moves, self._player1, self._player2)

                    to_square = input("Goal move: ")

                    self._search_piece(Color.WHITE)

                    move_made = self._move_piece(from_square, to_square)

                    if not move_made:
                        msg = f"Invalid move ('{from_square}' "\
                            f"'{to_square}'), try again."
                    else:
                        opponent_color = self._opponent_color(
                            player.color)
                        self.check = self._test_check(opponent_color)
                        if self.check:
                            msg = f'{opponent_color.name} is in CHECK !!'
                        else:
                            msg = None

                except Exception as e:
                    if to_square is None:
                        msg = f"Invalid seletion ('{from_square}'), try again"
                    else:
                        msg = (f"Invalid move ('{from_square}' "
                               f"'{to_square}'), try again.\n{e}")

            self.turn = not self.turn

        print('Game Over!')
# ***************** checar

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

    def _move_piece(self, from_square, to_square) -> bool:

        if not self._square_exists(to_square):
            self.warning(f"Position '{to_square}' doen't exist on board.")
            return False

        row, column = Position(from_square).position
        to_row, to_column = Position(to_square).position

        if not self._validate_target_position(row, column, to_row, to_column):
            return False

        piece = self._board._remove_piece(row, column)

        piece.position = Position(to_square)

        captured = self._board._place_piece(piece)

        if self._test_check(piece.color):
            self._board._undo_move(from_square, to_square, captured)
            self.warning("You cannot let your king in check.")
            return False

        return True

    def _validate_target_position(self, row, column, to_row, to_column):
        p = self._board.piece(row, column)
        if p is not None and not p.moves_mat[to_row][to_column]:
            self.warning(f"The piece {p} cannot move there.")
            return False
        return True

    # *************************************************************

    def _opponent_color(self, color):
        return Color.BLACK if color == Color.WHITE else Color.WHITE

    def _test_check(self, color: Color) -> bool:
        king_ = self._search_piece(color)
        row, col = king_.position.position
        for r in self._board._pieces:
            for p in r:
                if p is not None and p.color == self._opponent_color(color):
                    p.possible_moves()
                    if p.moves_mat[row][col]:
                        return True
        return False

    def _search_piece(self, color: Color, piece: Piece = King) -> Piece:
        for row in self._board._pieces:
            for p in row:
                if (p is not None and isinstance(p, piece)
                        and p.color == color):
                    return p
        raise LookupError(f"Not found {color.name} king on the board.")
    # *************************************************************

    def _position_exists(self, row, column) -> bool:
        return row >= 0 and row < 8 and column >= 0 and column < 8

    def _square_exists(self, s: str) -> bool:
        s = s.lower().strip()
        return (len(s) == 2 and s[0] >= "a" and s[0]
                <= "h" and s[1] >= "1" and s[1] <= "8")

    def _is_there_a_piece(self, row, column):
        return self._board._pieces[row][column] is not None

    def warning(self, msg):
        cprint(msg,  'yellow', end=' ')
        input("<Enter>")

    def _checkSeletion(self,  player, from_square) -> bool:

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

    def _current_player(self):
        if self.turn:
            return self._player1
        return self._player2

    def is_game_over(self):
        return self._board.is_checkmate() or self._board.is_stalemate()


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
