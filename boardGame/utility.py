
import enum


class Position:
    def __init__(self, square: str) -> None:
        self._row = None
        self._column = None
        self.position = (self._row, self._column)
        self._square = None
        if not self._to_position(square.lower()):
            raise ValueError("Invalid value.")

    @property
    def square(self):
        return self._square

    @property
    def row(self):
        return self._row

    @property
    def column(self):
        return self._column

    def _to_position(self, value):
        if len(value) != 2:
            return False

        letter, number = value[0], value[1]

        if not ('a' <= letter <= 'h'):
            return False

        if not ('1' <= number <= '8'):
            return False

        self._square = value
        self._row = 8 - int(value[1])
        self._column = ord(value[0]) - ord('a')
        self.position = (self._row, self._column)

        return True

    def from_position(self, row, column):

        if row < 0 or row > 7 or column < 0 or column > 7:
            raise ValueError("Invalid values for row or column.")

        return chr(column + ord('a')) + str(8 - row)

    def __str__(self) -> str:
        return f'{self._row}, {self._column}'


class Color(enum.Enum):
    WHITE = 1
    BLACK = 2
