from typing import Self
from enum import Enum

class Action(Enum):
    CAPTURE = 1
    STACK = 2

class Coordinates:
    row: int
    column: int

class Move:
    at: Coordinates
    move_to: Coordinates
    action: Action
    evaluation: int
    moves: list[Self]
    enemy_moves: list[Self]