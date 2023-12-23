import os
from termcolor import cprint
from boardGame.board import Board
from boardGame.piece import Piece


class UI:
    def __init__(self, board: Board) -> None:
        self._board = board

    def display_game(self, possible_moves, player1, player2):
        os.system("cls")
        print("\t  ***     CHESS GAME    ***\n")

        invert = False  # Flag to alternate between white and black square
        cprint(f'\t{player2} <Black>\n', "dark_grey")

        for i, row in enumerate(self._board._pieces):

            cprint(f'\t{8 - i}', "dark_grey", end=' ')

            for j, p in enumerate(row):

                square = self._get_square_color(invert, possible_moves[i][j])

                cprint(
                    self._get_piece(p),
                    self._get_piece_color(p),
                    square, end='')

                invert = not invert

            self._print_removed(i - 2)

            invert = not invert
            print()

        cprint('\t   a  b  c  d  e  f  g  h ', "dark_grey")
        cprint(f"\n\t{player1} <White>", "dark_grey")

    def print_msg(self, msg, check):
        if msg is not None:
            print()
            color = "yellow" if check else "dark_grey"
            cprint(msg, color)

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

    def _print_removed(self, index):
        removed = self._board.removed_pieces
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
