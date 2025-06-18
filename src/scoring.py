import numpy as np
from pieces import Color, Piece, is_color
from scoringvars import GRAVITY_VALUE, TOTT_VALUE, TZARR_VALUE, TZARRA_VALUE

def calculate_gravity(row: int, column: int) -> float:
    row_distance = abs(row-4)
    column_distance = abs(column-4)
    
    return GRAVITY_VALUE * max(row_distance, column_distance)

def get_piece_value(piece_abs: int) -> float:
    if piece_abs < Piece.TZARRA.value:
        return TOTT_VALUE
    elif piece_abs < Piece.TZAAR.value:
        return TZARRA_VALUE
    else:
        return TZARR_VALUE

def calculate_value_of_color(color: Color, board_state: np.ndarray) -> float:
    value : float = 0
    
    for i in range(0,9):
        for j in range(0,9):
            piece = board_state[i][j]
            if is_color(color, piece):
                piece_value = get_piece_value(abs(piece))
                gravity_value = calculate_gravity(i,j)
                value += piece_value - gravity_value 
                
    return value
     
   