
from enum import Enum

class Color(Enum):
    BLACK = -1
    WHITE = 1

class Piece(Enum):
    TOTT = 1
    TZARRA = 11
    TZAAR = 21
    
def form_piece(color: Color, piece: Piece) -> int:
    return color.value * piece.value

# def piece_color(piece: int) -> Union[Color, False]:
#     if piece == BLANK or piece == VOID or piece == MIDDLE:
#         raise Exception("Can't be pieces.BLANK or pieces.VOID")
#     elif piece > 0:
#         return Color.WHITE
#     elif piece < 0:
#         return Color.BLACK
#     else:
#         return False

def opposite_color(color: Color) -> Color:
    if color == Color.BLACK:
        return Color.WHITE

    else:
        return Color.BLACK

def is_color(color: Color, piece_value: int) -> bool:
    if piece_value == BLANK or piece_value == VOID or piece_value == MIDDLE:
        return False
    elif piece_value > 0 and color.value == Color.WHITE.value:
        return True
    elif piece_value < 0 and color.value == Color.BLACK.value:
        return True
    else:
        return False

WHITE_TOTT = form_piece(Color.WHITE, Piece.TOTT)
WHITE_TZARRA = form_piece(Color.WHITE, Piece.TZARRA)
WHITE_TZAAR = form_piece(Color.WHITE, Piece.TZAAR)

BLACK_TOTT = form_piece(Color.BLACK, Piece.TOTT)
BLACK_TZARRA = form_piece(Color.BLACK, Piece.TZARRA)
BLACK_TZAAR = form_piece(Color.BLACK, Piece.TZAAR)

BLANK = 0
VOID = 100
MIDDLE = 50