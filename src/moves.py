import pieces

def is_attackable(attacker, target):
    if attacker < 0 and target > 0:
        return True
    elif attacker > 0 and target < 0:
        return True
    else:
        return False

def send_attacker_to(arr, row, column, destination_row, destination_column):
    arr[destination_row][destination_column] = arr[row][column]
    arr[row][column] = pieces.BLANK
    
     