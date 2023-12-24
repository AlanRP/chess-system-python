import os
from termcolor import cprint
from boardGame.board import Board
from boardGame.piece import Piece
from boardGame.player import Player


class UI:
    def __init__(
        self,
        board: Board,
        player1: Player,
        player2: Player
    ) -> None:

        self._board = board
        self.player1 = player1
        self.player2 = player2

    def display_game_over(self, player: Player):
        self.display_game()
        cprint("CHECKMATE!!!", "light_yellow")
        print()
        cprint(f"{player.name} <{player.color.name}> won!", "light_yellow")
        print()

    def display_game(self, possible_moves=None):
        os.system("cls")
        cprint("\t ***     CHESS GAME    *** \n")

        invert = False  # Flag to alternate between white and black square
        cprint(f'\t{self.player2} <Black>\n', "dark_grey")

        for i, row in enumerate(self._board._pieces):

            cprint(f'\t{8 - i}', "dark_grey", end=' ')

            for j, p in enumerate(row):

                highlight = False
                if possible_moves is not None:
                    highlight = possible_moves[i][j]

                square = self._get_square_color(invert, highlight)

                cprint(
                    self._get_piece(p),
                    self._get_piece_color(p),
                    square,
                    attrs=self._get_piece_attr(p),
                    end=''
                )

                invert = not invert

            self._print_removed(i - 2)

            invert = not invert
            print()

        cprint('\t   a  b  c  d  e  f  g  h ', "dark_grey")
        cprint(f"\n\t{self.player1} <White>", "dark_grey")

    def print_msg(self, msg, check):
        if msg is not None:
            print()
            cprint(msg, "dark_grey")
        if check:
            cprint('CHECK!!!', "yellow")

    def get_source_move(self, player):
        print()
        print(f"Waiting for {player} ({player.color.name})")
        print()
        from_square = input("Source move: ")
        return from_square.lower().strip()

    def get_target_move(self, player):
        print()
        print(f"Waiting for {player} ({player.color.name})")
        print()
        to_square = input("Target move: ")
        return to_square.lower().strip()

    def _get_square_color(self, invert, possible_move):
        if possible_move:
            if invert:
                return "on_green"
            return "on_light_green"
        if not invert:
            return "on_cyan"
        return "on_blue"

    def _get_piece(self, piece: Piece):
        return '   ' if piece is None else f' {piece} '

    def _get_piece_color(self, piece: Piece):
        if piece is None:
            return None
        if piece.color.name == 'WHITE':
            return "white"
        return "red"

    def _get_piece_attr(self, piece: Piece):
        if piece is None:
            return None
        if piece.color.name == 'WHITE':
            return ["bold"]
        return ["dark"]

    def _print_removed(self, index):
        removed = self._board._removed_pieces
        if not len(removed):
            return
        if index == 0:
            cprint('  Captured:', 'dark_grey', end='')
        elif index == 3:
            cprint('   [ ', 'dark_grey', end='')
            for p in removed:
                if p.color.name == 'BLACK':
                    cprint(p, 'red', end=' ')
            cprint(']', 'dark_grey', end='')
        elif index == 1:
            cprint('   [ ', 'dark_grey', end='')
            for p in removed:
                if p.color.name == 'WHITE':
                    print(p, end=' ')
            cprint(']', 'dark_grey', end='')
        else:
            return
