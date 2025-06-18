import pieces

def is_attackable(attacker: int, target: int) -> bool:
    if attacker < 0 and target > 0:
        return True
    elif attacker > 0 and target < 0:
        return True
    else:
        return False

def send_attacker_to(arr: list, row: int, column: int, destination_row: int, destination_column: int) -> None:
    arr[destination_row][destination_column] = arr[row][column]
    arr[row][column] = pieces.BLANK
    