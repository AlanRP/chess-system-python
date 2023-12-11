

class Position:
    def __init__(self, row, column) -> None:
        self._row = row
        self._column = column

    @property
    def row(self):
        return self._row

    @row.setter
    def row(self, value):
        self._row = value

    @property
    def column(self):
        return self._column

    @column.setter
    def column(self, value):
        self._column = value

    def __str__(self) -> str:
        return f'{self._row}, {self._column}'


class Board:
    def __init__(self, rows: int, columns: int) -> None:
        self._rows = rows
        self._columns = columns
        self._pieces = [[], []]

    @property
    def rows(self):
        return self._rows

    @rows.setter
    def rows(self, value):
        self._rows = value

    @property
    def columns(self):
        return self._columns

    @columns.setter
    def columns(self, value):
        self._columns = value

    @property
    def pieces(Position):
        return self._pieces[[], []]

    def piece(self, row, column):
        return self._pieces[[row], [column]]

    def piece_pos(self, position):
        return self._pieces[[position.row], [position.column]]

    def setup_board(self):
        ...
        # todo -> implementar a configuração inicial do board
        # Adicionar peçars às casas.

    def display(self):
        ...
        # todo -> implementar a lógica para exibir o tabuleiro no console

    def move_piece(self, player, from_square, to_square) -> bool:
        ...
        # todo -> implementar a lógica para mover uma peça
        # verificar se a jogada é válida

    def is_valid_move(self, piece, to_square) -> bool:
        # todo -> implementar lógica de verificação do movimento.
        ...

    def is_checkmate(self):
        ...
        # todo -> implementar verificação de checkmate

    def is_stalemate(self):
        ...
        # verificar se está empatado.
