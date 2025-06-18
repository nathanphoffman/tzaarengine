from typing import Union

import numpy as np
import pieces

def number_of_occurences(arr: np.ndarray, num: int) -> int:
    
    occurrences : int = sum(1 for i in range(9) for j in range(9) if arr[i][j] == num)

    # for i in range(0,9):
    #     for j in range(0,9):
    #         if num == arr[i][j]:
    #             occurrences += 1
               
    #result = [(i, j) for i in range(3) for j in range(2)]
    
                
    return occurrences

def six_occurrences(arr: np.ndarray, piece: int) -> bool:
    return number_of_occurences(arr, piece) == 6

def nine_occurrences(arr: np.ndarray, piece: int) -> bool:
    return number_of_occurences(arr, piece) == 9

def fifteen_occurrences(arr: np.ndarray, piece: int) -> bool:
    return number_of_occurences(arr, piece) == 15

def setup_has_a_problem(arr: np.ndarray) -> Union[str, bool]:
    try:
        # number of rows check:
        if len(arr) != 9:
            return f"Number of rows {len(arr)} not 9"
        
        elif not fifteen_occurrences(arr, pieces.WHITE_TOTT) or not fifteen_occurrences(arr, pieces.BLACK_TOTT):
            return "There are not 15 TOTTS of each color on the board"
        
        elif not nine_occurrences(arr, pieces.WHITE_TZARRA) or not nine_occurrences(arr, pieces.BLACK_TZARRA):
            return "There are not 9 TZARRA of each color on the board"
        
        elif not six_occurrences(arr, pieces.WHITE_TZAAR) or not six_occurrences(arr, pieces.BLACK_TZAAR):
            return "There are not 6 TZAARS of each color on the board"
        
        else: 
            return False
        
    except Exception as e:
        print(e)
        return True

def get_starting_positions() -> np.array:
    standard_starting_positions = np.array([
        [*[pieces.VOID]*4, *[pieces.WHITE_TOTT]*4, pieces.BLACK_TOTT],
        [*[pieces.VOID]*3, pieces.BLACK_TOTT, *[pieces.WHITE_TZARRA]*3, pieces.BLACK_TZARRA, pieces.BLACK_TOTT],
        [*[pieces.VOID]*2, pieces.BLACK_TOTT, pieces.BLACK_TZARRA, *[pieces.WHITE_TZAAR]*2, pieces.BLACK_TZAAR, pieces.BLACK_TZARRA, pieces.BLACK_TOTT],
        [pieces.VOID, pieces.BLACK_TOTT, pieces.BLACK_TZARRA, pieces.BLACK_TZAAR, pieces.WHITE_TOTT,pieces.BLACK_TOTT, pieces.BLACK_TZAAR, pieces.BLACK_TZARRA, pieces.BLACK_TOTT],
        [pieces.BLACK_TOTT, pieces.BLACK_TZARRA, pieces.BLACK_TZAAR, pieces.BLACK_TOTT, pieces.MIDDLE, pieces.WHITE_TOTT, pieces.WHITE_TZAAR, pieces.WHITE_TZARRA, pieces.WHITE_TOTT],
        [pieces.VOID, pieces.WHITE_TOTT, pieces.WHITE_TZARRA, pieces.WHITE_TZAAR, pieces.WHITE_TOTT, pieces.BLACK_TOTT, pieces.WHITE_TZAAR, pieces.WHITE_TZARRA, pieces.WHITE_TOTT],
        [*[pieces.VOID]*2, pieces.WHITE_TOTT, pieces.WHITE_TZARRA, pieces.WHITE_TZAAR, *[pieces.BLACK_TZAAR]*2, pieces.WHITE_TZARRA, pieces.WHITE_TOTT],
        [*[pieces.VOID]*3, pieces.WHITE_TOTT, pieces.WHITE_TZARRA, *[pieces.BLACK_TZARRA]*3, pieces.WHITE_TOTT],
        [*[pieces.VOID]*4, pieces.WHITE_TOTT, *[pieces.BLACK_TOTT]*4]
    ])
    
    problem = setup_has_a_problem(standard_starting_positions)
    if problem:
        print("Something is wrong with the starting board state")
        raise Exception(problem)
    
    else:
        return standard_starting_positions

