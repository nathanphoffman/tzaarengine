from typing import Self
from enum import Enum
import numpy as np
import pieces
import copy

class Action(Enum):
    START = 0
    CAPTURE = 1
    STACK = 2

Piece = int
#Array_Coordinate = list[int] #of type [row: int, column: int]
Board_Line = list[Piece]
Board = list[Board_Line]

BOARD_SIZE = range(0,9)

class Coordinates:
    
    def __init__(self: Self, x: int, y: int) -> None:
        self.x = x
        self.y = y
    
    x: int
    y: int
    
    def equals(this: Self, that: Self) -> bool:
        return this.x == that.x and this.y == this.y
    
    def xy(self: Self) -> list[int]:
        return [self.row, self.column]

class Piece:
    
    def __init__(self: Self, x: int, y: int, number) -> None:
        self.at = Coordinates(x, y)
        self.number = number
        self.color = pieces.is_color(self.piece)
        
    at: Coordinates
    number: pieces.Piece
    color: pieces.Color

class Position:
    
    def __init__(self: Self, board: Board, x: int, y: int) -> None:
        self.board = board
        board_piece_number = board[x][y]
        self.piece = Piece(x, y, board_piece_number)
        
    recursion_max: int
    recursion: int
    board: Board
    piece: Piece
    evaluation: int
    action: Action
    
    captures: list[Self]
    enemy_captures: list[Self]
    
    stacks: list[Self]
    enemy_stacks: list[Self]
    
    def move_valid(self: Self, move_x: int, move_y: int):
        
        undefined_move = (
            move_x > 8 
            or move_x < 0
            or move_y > 8 
            or move_y < 0
        )
        
        if(undefined_move):
            return []
        
        target = self.board[move_x][move_y]
        
        invalid_move = (
            pieces.is_color(self.piece.color) 
            or target == pieces.MIDDLE 
            or target == pieces.VOID
        )
        
        return not invalid_move
    
    def empty_move(self: Self, move_x: int, move_y: int):
        
        target = self.board[move_x][move_y]
        return target == pieces.BLANK
            
    def find_capture(self: Self, x, y, x_direction, y_direction):
        
        new_x = x + x_direction
        new_y = y + y_direction
        
        # move further on the line to see if a piece is capturable
        if(self.move_empty(new_x, new_y)):
            return self.find_capture(new_x, new_y, x_direction, y_direction)
        
        elif(self.move_valid(new_x, new_y)):
            return Position(self.board, new_x, new_y)
            
        else:
            return []
            
    def evaluate_captures(position: Self) -> None:
        # move the piece
        # construct the new board state

        
        return self
    
    def evaluate_stacks(position: Self) -> Self:
        # move the piece
        # construct the new board state
        
        return self
    
    def evaluate_next_moves(self: Self, player_color: pieces.Color, recursion: 0, recursion_max: int) -> None:
        
        # evaluate the whole board for useable pieces of the color indicated
        for x in BOARD_SIZE:
            for y in BOARD_SIZE:
                piece = Piece(x,y,self.board[x][y])
                enemy_color = pieces.opposite_color(player_color)
                
                # If a piece is trapped (it has no moves to make) position will be a None value, this is filtered out later on 
                # For now we just add all possible positions regardless of legal moves to make upstream logic easier to follow
                if(pieces.is_color(player_color, piece.color)):
                    self.captures.extend(*Position(copy.deepcopy(self.board), x, y).evaluate_captures())
                    self.stacks.extend(*Position(copy.deepcopy(self.board), x, y).evaluate_stacks())
                    
                elif(pieces.is_color(enemy_color)):
                    self.enemy_captures.extend(*Position(copy.deepcopy(self.board), x, y).evaluate_captures())
                    self.enemy_stacks.extend(*Position(copy.deepcopy(self.board), x, y).evaluate_stacks())
        
        return None
    
    def evaluate(self: Self, max_moves: int, max_time_ms: int) -> None:
        return None
        
