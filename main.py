from boardGame.board import Board
from boardGame.chess_match import ChessMatch
import os


def main():
    os.system("cls")
    print("\t*** Welcome to CHESS ***\n\n")
    player1 = input('Enter the name of the WHITE player: ')
    player2 = input('Enter the name of the BLACK player: ')

    game = ChessMatch(Board(), player1, player2)
    game._board.setup_board()
    UI = game._UI
    msg = None

    while not game.is_game_over():
        move_made = False
        from_square = None
        to_square = None
        player = game._current_player()

        while not move_made:
            possible_moves = [[False] * 8 for _ in range(8)]

            try:
                UI.display_game(possible_moves)

                game.check = game._is_check(player.color)
                UI.print_msg(msg, game.check)

                from_square = UI.get_source_move(player)

                if not game._validate_source(player, from_square):
                    msg = (f"Invalid source seletion: "
                           f"'{from_square}', try again.")
                    continue

                possible_moves = game._possibleMoves(from_square)

                UI.display_game(possible_moves)

                to_square = UI.get_target_move(player)

                if not game._validate_target(from_square, to_square):
                    msg = (f"Invalid source seletion: "
                           f"'{to_square}', try again.")
                    continue

                move_made = game._move_piece(
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

        game.turn = not game.turn

    print('Game Over!')


if __name__ == '__main__':

    main()
