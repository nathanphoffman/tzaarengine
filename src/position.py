from typing import Self
from enum import Enum

class Action(Enum):
    CAPTURE = 1
    STACK = 2

class Coordinates:
    
    def __init__(self: Self, row: int, column: int) -> None:
        self.row = row
        self.column = column
    
    row: int
    column: int

class Move:
    
    def __init__(self: Self, row: int, column: int) -> None:
        self.at = Coordinates(row, column)
    
    at: Coordinates
    action: Action
    evaluation: int
    moves: list[Self]
    enemy_moves: list[Self]