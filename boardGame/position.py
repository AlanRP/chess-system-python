
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
