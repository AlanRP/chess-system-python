from boardGame.board import Board
from boardGame.player import Player
from boardGame.utility import Color
import os
from termcolor import cprint


class ChessGame:
    def __init__(self, board: Board):
        self._board = board
        self._player1 = self._board.player1
        self._player2 = self._board.player2
        self.turn = True
        self.check = False

    def play(self):
        self._board.setup_board()
        msg = None

        while not self.is_game_over():
            move_made = False
            from_square = None
            to_square = None

            while not move_made:
                player = self._current_player()
                possible_moves = [[False] * 8 for _ in range(8)]

                try:
                    self._display_game(possible_moves)

                    if msg is not None:
                        print()
                        cprint(msg, "dark_grey")

                    print()
                    print(f"Waiting for {player} ({player.color.name})")

                    from_square = input("Source move: ")

                    if not self._board._checkSeletion(player, from_square):
                        raise ''

                    possible_moves = self._board._possibleMoves(from_square)

                    self._display_game(possible_moves)

                    to_square = input("Goal move: ")

                    self._board._search_piece(Color.WHITE)

                    move_made = self._board._move_piece(from_square, to_square)

                    if not move_made:
                        msg = f"Invalid move ('{from_square}' "\
                            f"'{to_square}'), try again."
                    else:
                        opponent_color = self._board._opponent_color(
                            player.color)
                        self.check = self._board._test_check(opponent_color)
                        if self.check:
                            msg = f'{opponent_color.name} is in CHECK!'
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

    def _current_player(self):
        if self.turn:
            return self._player1
        return self._player2

    def _display_game(self, possible_moves):
        os.system("cls")
        print("\t***     CHESS GAME    ***\n")
        self._board.display(possible_moves)
        return True

    def is_game_over(self):
        return self._board.is_checkmate() or self._board.is_stalemate()


if __name__ == '__main__':

    os.system("cls")
    print("\t*** Welcome to CHESS ***\n\n")
    name1 = input('Enter the name of the WHITE player: ')
    name2 = input('Enter the name of the BLACK player: ')

    player1 = Player(name1, Color(1))
    player2 = Player(name2, Color(2))

    match = ChessGame(Board(player1, player2))

    # match.start_game()
    match.play()
