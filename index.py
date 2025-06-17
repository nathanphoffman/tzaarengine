import numpy as np
import sys

import os, sys

# type: ignore
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))
from captures import find_best_moves, get_all_captures_by_space
from scoring import calculate_value_of_color
from pieces import Color
import pieces
from setup import get_starting_positions
from moves import send_attacker_to

def print_board(arr: np.ndarray):
    for i in range(0, 9):
        print_line(arr[i])
    
def print_line(arr: np.ndarray):
    line: str = ""
    for i in range(0, 9):  # Loop from 0 to 8
        line += " "
        if arr[i] == pieces.VOID:
            line += "."
        elif arr[i] == pieces.BLANK:
            line += "__"
        elif arr[i] == pieces.MIDDLE:
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
    
standard_starting_positions = get_starting_positions()


# send_attacker_to(standard_starting_positions, 3,4, 3,3) # white
# send_attacker_to(standard_starting_positions, 5,5, 5,6) # black
# # send_attacker_to(standard_starting_positions, 6,5, 6,4) # black

print(calculate_value_of_color(Color.WHITE, standard_starting_positions))
print(calculate_value_of_color(Color.BLACK, standard_starting_positions))

print(find_best_moves(Color.BLACK, standard_starting_positions, False, 0))

print_board(standard_starting_positions)