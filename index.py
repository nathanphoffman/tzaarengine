print("Hello, World!")

from enum import Enum
import numpy as np
from typing import Union
import  math


class Color(Enum):
    BLACK = -1
    WHITE = 1

class Piece(Enum):
    TOTT = 1
    TZARRA = 11
    TZAAR = 21
    

def form_piece(color: Color, piece: Piece):
    return color.value * piece.value


WHITE_TOTT = form_piece(Color.WHITE, Piece.TOTT)
WHITE_TZARRA = form_piece(Color.WHITE, Piece.TZARRA)
WHITE_TZAAR = form_piece(Color.WHITE, Piece.TZAAR)

BLACK_TOTT = form_piece(Color.BLACK, Piece.TOTT)
BLACK_TZARRA = form_piece(Color.BLACK, Piece.TZARRA)
BLACK_TZAAR = form_piece(Color.BLACK, Piece.TZAAR)

BLANK = 0
VOID = 100
MIDDLE = 50

def number_of_occurences(arr: np.ndarray, num: int):
    
    occurrences : int = 0
    
    #result = [(i, j) for i in range(3) for j in range(2)]
    
    for i in range(0,9):
        for j in range(0,9):
            if num == arr[i][j]:
                occurrences += 1
                
    return occurrences

def six_occurrences(arr: np.ndarray, piece: int):
    return number_of_occurences(arr, piece) == 6

def nine_occurrences(arr: np.ndarray, piece: int):
    return number_of_occurences(arr, piece) == 9

def fifteen_occurrences(arr: np.ndarray, piece: int):
    return number_of_occurences(arr, piece) == 15

def setup_has_a_problem(arr: np.ndarray) -> Union[str, bool]:
    try:
        # number of rows check:
        if len(arr) != 9:
            return f"Number of rows {len(arr)} not 9"
        
        elif not fifteen_occurrences(arr, WHITE_TOTT) or not fifteen_occurrences(arr, BLACK_TOTT):
            return "There are not 15 TOTTS of each color on the board"
        
        elif not nine_occurrences(arr, WHITE_TZARRA) or not nine_occurrences(arr, BLACK_TZARRA):
            return "There are not 9 TZARRA of each color on the board"
        
        elif not six_occurrences(arr, WHITE_TZAAR) or not six_occurrences(arr, BLACK_TZAAR):
            return "There are not 6 TZAARS of each color on the board"
        
        else: 
            return False
        
    except Exception as e:
        print(e)
        return True

standard_starting_positions = np.array([
    [*[VOID]*4, *[WHITE_TOTT]*4, BLACK_TOTT],
    [*[VOID]*3, BLACK_TOTT, *[WHITE_TZARRA]*3, BLACK_TZARRA, BLACK_TOTT],
    [*[VOID]*2, BLACK_TOTT, BLACK_TZARRA, *[WHITE_TZAAR]*2, BLACK_TZAAR, BLACK_TZARRA, BLACK_TOTT],
    [VOID, BLACK_TOTT, BLACK_TZARRA, BLACK_TZAAR, WHITE_TOTT,BLACK_TOTT, BLACK_TZAAR, BLACK_TZARRA, BLACK_TOTT],
    [BLACK_TOTT, BLACK_TZARRA, BLACK_TZAAR, BLACK_TOTT, MIDDLE, WHITE_TOTT, WHITE_TZAAR, WHITE_TZARRA, WHITE_TOTT],
    [VOID, WHITE_TOTT, WHITE_TZARRA, WHITE_TZAAR, WHITE_TOTT, BLACK_TOTT, WHITE_TZAAR, WHITE_TZARRA, WHITE_TOTT],
    [*[VOID]*2, WHITE_TOTT, WHITE_TZARRA, WHITE_TZAAR, *[BLACK_TZAAR]*2, WHITE_TZARRA, WHITE_TOTT],
    [*[VOID]*3, WHITE_TOTT, WHITE_TZARRA, *[BLACK_TZARRA]*3, WHITE_TOTT],
    [*[VOID]*4, WHITE_TOTT, *[BLACK_TOTT]*4]
])

problem = setup_has_a_problem(standard_starting_positions)
if problem:
    print("Something is wrong with the starting board state")
    raise Exception(problem)

def print_board(arr: np.ndarray):
    for i in range(0, 9):
        print_line(arr[i])
    
def print_line(arr: np.ndarray):
    line: str = ""
    for i in range(0, 9):  # Loop from 0 to 8
        line += " "
        if arr[i] == VOID:
            line += "."
        elif arr[i] == BLANK:
            line += "__"
        elif arr[i] == MIDDLE:
            line += "[ ]"
        elif arr[i] > 0:
            if(arr[i] < 10):
                line += "+0" + str(arr[i])
            else:
                line += "+" + str(arr[i])
        elif arr[i] < 0 and arr[i] > -10:
            line += "-0" + str(abs(arr[i]))
        else:
            line += str(arr[i])
        
    
    print(line)

def is_attackable(attacker, target):
    if attacker < 0 and target > 0:
        return True
    elif attacker > 0 and target < 0:
        return True
    else:
        return False

def captures_from_position(arr, row, column, row_direction, column_direction, attacker = 0, capture_possibilities = []):
    
    if arr[row][column] == BLANK or arr[row][column] == VOID or arr[row][column] == MIDDLE:
        return []
    
    if attacker == 0:
        attacker = arr[row][column]
    
    row_move = row + row_direction
    column_move = column + column_direction
    
    if row_move < 0 or row_move > 8:
        return capture_possibilities
    
    elif column_move < 0 or column_move > 8:
        return capture_possibilities
    
    target = arr[row_move][column_move]
    
    if target == VOID:
        return capture_possibilities
    
    # Look ahead to the next capture possibility
    elif target == BLANK:
        capture_possibilities = captures_from_position(arr, row_move, column_move, row_direction, column_direction, capture_possibilities)
        
    elif is_attackable(attacker, target):
        capture_possibilities.append([row_move, column_move])
        
    return capture_possibilities
        
def get_all_captures_by_space(arr, row, column):
    
    all_capture_spots = []

    # captures along the row (the east side of the hex)
    all_capture_spots.append(captures_from_position(arr, row, column, 0, 1, 0, []))
    
    #  # captures along the row in the opposite direction (the west side of the hex)
    all_capture_spots.append(captures_from_position(arr, row, column, 0, -1, 0, []))
    
    # # # captures along the column (the south-east side of the hex)
    all_capture_spots.append(captures_from_position(arr, row, column, 1, 0, 0, []))
    
    # # # captures along the column in the opposite direction (the north-west side of the hex)
    all_capture_spots.append(captures_from_position(arr, row, column, -1, 0, 0, []))
    
    # # # ---- to get the third line we need to calculate it with both row and column adjustments to give us the diagnol the last of the three hex lines (6 positions)
    
    # # # captures along the 2nd column (the north-east side of the hex)
    all_capture_spots.append(captures_from_position(arr, row, column, -1, 1, 0, []))
    
    # # # captures along the 2nd column (the north-west side of the hex)
    all_capture_spots.append(captures_from_position(arr, row, column, 1, -1, 0, []))
    
    # remove empty lists
    all_capture_spots = [item for item in all_capture_spots if item]
    
    return all_capture_spots
    
def send_attacker_to(arr, row, column, destination_row, destination_column):
    arr[destination_row][destination_column] = arr[row][column]
    arr[row][column] = BLANK

TOTT_VALUE = 1
TZARRA_VALUE = 1.25
TZARR_VALUE = 1.5  
REACH_VALUE = 1
GRAVITY_VALUE = 0.1
    
def calculate_gravity(row, column):
    row_distance = abs(row-4)
    column_distance = abs(column-4)
    
    return GRAVITY_VALUE * max(row_distance, column_distance)


def is_color(color: Color, piece):
    if piece == BLANK or piece == VOID or piece == MIDDLE:
        return False
    elif piece > 0 and color.value == Color.WHITE.value:
        return True
    elif piece < 0 and color.value == Color.BLACK.value:
        return True
    else:
        return False
        
def get_piece_value(piece_abs: int):
    if piece_abs < Piece.TZARRA.value:
        return TOTT_VALUE
    elif piece_abs < Piece.TZAAR.value:
        return TZARRA_VALUE
    else:
        return TZARR_VALUE


def calculate_value_of_color(color: Color, board_state: np.ndarray):
    value = 0
    
    for i in range(0,9):
        for j in range(0,9):
            piece = board_state[i][j]
            if is_color(color, piece):
                piece_value = get_piece_value(abs(piece))
                gravity_value = calculate_gravity(i,j)
                value += piece_value - gravity_value 
                
    return value
     
   
def piece_color(piece: int):
    if piece == BLANK or piece == VOID or piece == MIDDLE:
        raise Exception("Can't be blank or void")
    elif piece > 0:
        return Color.WHITE.value
    elif piece < 0:
        return Color.BLACK.value
    else:
        return False
   
def opposite_color(color: Color):
    if color == Color.BLACK:
        return Color.WHITE
    
    else: 
        return Color.BLACK
   
def add_value_to_captures(color: Color, captures: np.ndarray, board_state: np.ndarray, row, column):
    
    valued_captures = []
    enemy_color = opposite_color(color)
    
    for i in range(0,len(captures)):
        positions = board_state.copy()
        item = captures[i][0]
        row_move = item[0]
        column_move = item[1]
        send_attacker_to(positions, row, column, row_move, column_move)
        
        board_value = calculate_value_of_color(color, positions) - calculate_value_of_color(enemy_color, positions)
        valued_captures.append([board_value, row, column, captures[i]])
        
    return valued_captures
   
def find_best_moves(color: Color, board_state: np.ndarray, next_moves = []):
    
    valued_captures = []
    
    for i in range(0,9):
        for j in range(0,9):
            piece = board_state[i][j]
            if is_color(color, piece):
                if i == 4 and j == 4:
                    print("yep")
                print(piece)
                captures = get_all_captures_by_space(board_state, i, j)
                valued_capture = add_value_to_captures(color, captures, board_state, i, j)
                valued_captures.extend(valued_capture) 
                
                
    
    valued_captures = [item for item in valued_captures if item]
    check = valued_captures[0]
    valued_captures.sort(key=lambda x: x[0], reverse=True)
    
    if len(valued_captures) < 3:
        return valued_captures
    
    if next_moves == []:
        next_moves = valued_captures[:3]
    else:
        return valued_captures
        
    for i in range(0,len(next_moves)):
        positions = board_state.copy()
        item = next_moves[i]
        row = item[1]
        column = item[2]
        
        row_move = item[3][0][0]
        row_column = item[3][0][1]
        
        send_attacker_to(positions, row, column, row_move, row_column)
        new_captures = find_best_moves(color, positions, next_moves)
        print("ran")
        
    
    return valued_captures
                

         
#send_attacker_to(standard_starting_positions, 2,4,3,3)

print(calculate_value_of_color(Color.WHITE, standard_starting_positions))
print(calculate_value_of_color(Color.BLACK, standard_starting_positions))

print(get_all_captures_by_space(standard_starting_positions, 3,3))

print(find_best_moves(Color.WHITE, standard_starting_positions))

print_board(standard_starting_positions)
