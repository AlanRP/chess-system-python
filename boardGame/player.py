from boardGame.utility import Color
from dataclasses import dataclass


@dataclass
class Player:
    name: str
    color: Color

    def __str__(self) -> str:
        return self.name
