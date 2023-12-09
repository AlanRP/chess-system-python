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


class Piece:

    def __init__(self, board) -> None:
        self._position = None
        self._board = board

    @property
    def board(self):
        return self._board
