from boardGame.board import Board
from boardGame.player import Player
from boardGame.utility import Color
import os


class ChessGame:
    def __init__(self, board: Board):
        self._board = board
        self._player1 = None
        self._player2 = None
        self.turn = True

    def start_game(self):
        os.system("cls")
        print("\t*** Welcome to CHESS ***\n")
        self._board.setup_board()
        self._get_player()

    def play(self):
        while not self.is_game_over():
            move_made = False
            msg = None

            while not move_made:
                player = self._current_player()
                try:
                    self._display_game()

                    if msg is not None:
                        print('\n', msg)

                    print("\n",
                          f"It's {player.name}'s turn ({player.color.name})")

                    from_square = input("Source: ")
                    to_square = input("Goal: ")

                    move_made = self._board.move_piece(
                        player, from_square, to_square)

                    if not move_made:
                        msg = f"Invalid move ('{from_square}' "\
                            f"'{to_square}'), try again."
                    else:
                        msg = None

                except Exception as e:
                    msg = f"Invalid move ('{from_square}' "\
                        f"'{to_square}'), try again.\n{e}"

            self.turn = not self.turn

        print('Game Over!')

    def _get_player(self):
        print()
        name1 = input('Enter the name of the WHITE player: ')
        name2 = input('Enter the name of the BLACK player: ')

        self._player1 = Player(name1, Color(1))
        self._player2 = Player(name2, Color(2))
        self._board.player1 = self._player1.name
        self._board.player2 = self._player2.name

    def _current_player(self):
        if self.turn:
            return self._player1
        return self._player2

    def _display_game(self):
        os.system("cls")
        print("\t***     CHESS GAME    ***\n")
        # print(f'{self._player2.name} <Black>')
        # print(f'\t  {self._player1.name} <White>\n')
        self._board.display()
        return True

    def is_game_over(self):
        return self._board.is_checkmate() or self._board.is_stalemate()


if __name__ == '__main__':
    match = ChessGame(Board())
    match.start_game()
    match.play()
