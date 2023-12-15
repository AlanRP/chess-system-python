
import enum


class Position:
    def __init__(self, square: str) -> None:
        self._row = None
        self._column = None
        self._square = None
        self._validate_position(square.lower())

    @property
    def square(self):
        return self._square

    @property
    def row(self):
        return self._row

    @property
    def column(self):
        return self._column

    @row.setter
    def row(self, value):
        self._row = value

    @column.setter
    def column(self, value):
        self._column = value

    def _validate_position(self, value):
        if len(value) != 2:
            return None

        letter, number = value[0], value[1]

        if not ('a' <= letter <= 'h'):
            return None

        if not ('1' <= number <= '8'):
            return None

        self._square = value

        self._row = 8 - int(value[1])
        self._column = ord(value[0]) - ord('a')

        return value

    def __str__(self) -> str:
        return f'{self._row}, {self._column}'


class Color(enum.Enum):
    WHITE = 1
    BLACK = 2
