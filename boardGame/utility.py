
import enum


class Position:
    def __init__(self, value) -> None:

        self._row = None
        self._column = None
        self._square = None
        if isinstance(value, str):
            if not self._to_position(value.lower().strip()):
                raise ValueError("Invalid value.")
        elif isinstance(value, (list, tuple)):
            if len(value) == 2:
                self._row = int(value[0])
                self._column = int(value[1])

    @property
    def square(self):
        if self.row < 0 or self.row > 7 or self.column < 0 or self.column > 7:
            self.square = None
            return

        self._square = chr(self.column + ord('a')) + str(8 - self.row)

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

    @property
    def position(self):
        return ((self._row, self._column))

    @position.setter
    def position(self, value): ...

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

        return True

    def set_values(self, row, column):

        if row < 0 or row > 7 or column < 0 or column > 7:
            raise ValueError("Invalid values for row or column.")

        # self._square = chr(column + ord('a')) + str(8 - row)
        self._row = row
        self._column = column

    def __str__(self) -> str:
        return f'{self._row}, {self._column}'


class Color(enum.Enum):
    WHITE = 1
    BLACK = 2
