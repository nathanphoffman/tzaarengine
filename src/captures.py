import numpy as np
from moves import is_attackable, send_attacker_to
import pieces
from scoring import calculate_value_of_color
import math

def captures_from_position(arr, row, column, row_direction, column_direction, attacker = 0, capture_possibilities = []):
    
    if arr[row][column] == pieces.BLANK or arr[row][column] == pieces.VOID or arr[row][column] == pieces.MIDDLE:
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
    
    if target == pieces.VOID:
        return capture_possibilities
    
    # Look ahead to the next capture possibility
    elif target == pieces.BLANK:
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
    
def add_value_to_captures(color: pieces.Color, captures: np.ndarray, board_state: np.ndarray, row, column):
    
    valued_captures = []
    enemy_color = pieces.opposite_color(color)
    
    for i in range(0,len(captures)):
        positions = board_state.copy()
        item = captures[i][0]
        row_move = item[0]
        column_move = item[1]
        send_attacker_to(positions, row, column, row_move, column_move)
        
        board_value = calculate_value_of_color(color, positions) - calculate_value_of_color(enemy_color, positions)
        valued_captures.append([board_value, row, column, captures[i]])
        
    return valued_captures
  
    
def determine_capture_values(color: pieces.Color, board_state: np.ndarray):
    
    valued_captures = []
    
    for i in range(0,9):
        for j in range(0,9):
            piece = board_state[i][j]
            if pieces.is_color(color, piece):
                captures = get_all_captures_by_space(board_state, i, j)
                valued_capture = add_value_to_captures(color, captures, board_state, i, j)
                valued_captures.extend(valued_capture) 
                
    valued_captures = [item for item in valued_captures if item]
    check = valued_captures[0]
    valued_captures.sort(key=lambda x: x[0], reverse=True)
    
    return valued_captures
    
def determine_average_evaluation(evaluation):
    
    if len(evaluation) == 0:
        return 0
    
    average_evaluation = 0
    number = len(evaluation)
    
    for i in range(0,number):
        average_evaluation += evaluation[i][0]
        
    return average_evaluation/number
        
    
def merge_lookahead(row, column, evaluated_captures, enemy_moves):
    for i in range(0,len(evaluated_captures)):
        if evaluated_captures[i][1] == row and evaluated_captures[i][2] == column:
            evaluated_captures[i][0] +- determine_average_evaluation(enemy_moves)
        
    evaluated_captures.sort(key=lambda x: x[0], reverse=True)
    return evaluated_captures
    
def reduce_evaluation(evaluated_captures):
        # with such few options there is no point to look ahead, our move is determined
    if len(evaluated_captures) < 2:
        return evaluated_captures
    # there is really no point to evaluate poor positions so we take the top options, this reduces exponentially look-ahead complexity and runtime
    number_to_consider = math.floor(len(evaluated_captures)/3) + 1
    #number_to_consider = len(evaluated_captures)
    
    reduced_captures = evaluated_captures[:number_to_consider]
    return reduced_captures
    
def find_best_moves(color: pieces.Color, board_state: np.ndarray, first_move = False, runs = 0):
    
    response = []
    evaluated_captures = determine_capture_values(color, board_state)
    reduced_evaluations = reduce_evaluation(evaluated_captures)

    for i in range(0,len(reduced_evaluations)):
        positions = board_state.copy()
        item = reduced_evaluations[i]
        
        row = item[1]
        column = item[2]
        starting_move = [row, column]
        
        row_move = item[3][0][0]
        row_column = item[3][0][1]
        ending_move = [row_move, row_column]
        
        send_attacker_to(positions, row, column, row_move, row_column)
        new_evaluation = determine_capture_values(color, positions) if first_move is False else reduced_evaluations
        
        # now we determine enemy moves
        runs += 1
        enemy_moves = find_best_moves(pieces.opposite_color(color), positions, False, runs) if runs < 5 else []
        response.append([[starting_move], merge_lookahead(row_move, row_column, new_evaluation, enemy_moves)])

    return response
        
   