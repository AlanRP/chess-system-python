class ChessGame:
    def __init__(self, board, player1, player2):
        self._board = board
        self._player1 = player1
        self._player2 = player2

    def start_game(self):
        print("Bem vindo ao jogo de xadrez!")
        self.board.setup_board()
        self.board.display()

    def play(self):
        current_player = self.player1

        while not self.is_game_over():
            move_made = False

            while not move_made:
                try:
                    print(f'\nÉ a vez de {current_player.name}.')
                    move = input("Digite sua jogada (ex: 'e2 e4'): ")
                    move = move.split()

                    if len(move) != 2:
                        raise ValueError(
                            "Jogada inválida. Digite duas posições.")

                    from_square, to_square = move
                    move_made = self.board.move_piece(
                        current_player, from_square, to_square)

                    if not move_made:
                        print("Jogada inválida. Tente novamente.")

                    self.board.display()

                except Exception as e:
                    print(f'Erro: {e}')

            if current_player == self._player1:
                current_player = self._player2
            else:
                current_player = self._player1

        print('Fim de Jogo!')

    def is_game_over(self):
        return self.board.is_checkmate() or self.board.is_stalemate()
