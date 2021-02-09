"""
module for working with skyscrapers game
git repo: https://github.com/fox-flex/skyscrapers
"""


def read_input(path: str):
    """
    Read game board file from path.
    Return list of str.
    """
    with open(path, 'r') as file:
        board = list(map(lambda x: x.strip(), file.readlines()))
    return board


def left_to_right_check(input_line: str, pivot: int) -> bool:
    """
    Check row-wise visibility from left to right.
    Return True if number of building from the left-most hint is visible
     looking to the right,
    False otherwise.
    input_line - representing board row.
    pivot - number on the left-most hint of the input_line.
    >>> left_to_right_check("412453*", 4)
    True
    >>> left_to_right_check("452453*", 5)
    False
    """
    line = input_line[1:-1]
    last_seen = line[0]
    seen = 1
    for high in line[1:]:
        if last_seen < high:
            seen += 1
            last_seen = high
    return seen == pivot


def check_not_finished_board(board: list) -> bool:
    """
    Check if skyscraper board is not finished, i.e., '?' present
     on the game board.
    Return True if finished, False otherwise.
    >>> check_not_finished_board(['***21**', '4?????*', '4?????*', '*?????5', \
'*?????*', '*?????*', '*2*1***'])
    False
    >>> check_not_finished_board(['***21**', '412453*', '423145*', '*543215', \
'*35214*', '*41532*', '*2*1***'])
    True
    >>> check_not_finished_board(['***21**', '412453*', '423145*', '*5?3215', \
'*35214*', '*41532*', '*2*1***'])
    False
    """
    finished = True
    for line in board[1:-1]:
        if '?' in line:
            finished = False
            break
    return finished


def check_uniqueness_in_rows(board: list) -> bool:
    """
    Check buildings of unique height in each row.
    Return True if buildings in a row have unique length, False otherwise.
    >>> check_uniqueness_in_rows(['***21**', '412453*', '423145*', '*543215', \
'*35214*', '*41532*', '*2*1***'])
    True
    >>> check_uniqueness_in_rows(['***21**', '452453*', '423145*', '*543215', \
'*35214*', '*41532*', '*2*1***'])
    False
    >>> check_uniqueness_in_rows(['***21**', '412453*', '423145*', '*553215', \
'*35214*', '*41532*', '*2*1***'])
    False
    """
    unique = True
    num = len(board) - 2
    board_c = list(map(lambda x: x[1: -1], board[1:-1]))
    possible_val = set(map(str, range(1, num+1)))
    for line in board_c:
        line_val = set()
        for val in line:
            if val in possible_val and val not in line_val:
                line_val.add(val)
            else:
                unique = False
                break
        if not unique:
            break
    return unique


def check_horizontal_visibility(board: list) -> bool:
    """
    Check row-wise visibility (left-right and vice versa)
    Return True if all horizontal hints are satisfiable,
     i.e., for line 412453* , hint is 4, and 1245 are the four buildings
      that could be observed from the hint looking to the right.
    >>> check_horizontal_visibility(['***21**', '412453*', '423145*', \
'*543215', '*35214*', '*41532*', '*2*1***'])
    True
    >>> check_horizontal_visibility(['***21**', '452453*', '423145*', \
'*543215', '*35214*', '*41532*', '*2*1***'])
    False
    >>> check_horizontal_visibility(['***21**', '452413*', '423145*', \
'*543215', '*35214*', '*41532*', '*2*1***'])
    False
    """
    if check_not_finished_board(board) and check_uniqueness_in_rows(board):
        is_ok = True
        board_c = board[1:-1]
        for line in board_c:
            try:
                pivot = int(line[0])
                if not left_to_right_check(line, pivot):
                    is_ok = False
                    break
            except ValueError:
                pass
            try:
                pivot = int(line[-1])
                if not left_to_right_check(line[::-1], pivot):
                    is_ok = False
                    break
            except ValueError:
                pass
    else:
        is_ok = False
    return is_ok


def check_columns(board: list) -> bool:
    """
    Check column-wise compliance of the board for uniqueness (buildings of
     unique height) and visibility (top-bottom and vice versa).
    Same as for horizontal cases, but aggregated in one function for vertical
     case, i.e. columns.
    >>> check_columns(['***21**', '412453*', '423145*', '*543215', '*35214*', \
'*41532*', '*2*1***'])
    True
    >>> check_columns(['***21**', '412453*', '423145*', '*543215', '*35214*', \
'*41232*', '*2*1***'])
    False
    >>> check_columns(['***21**', '412553*', '423145*', '*543215', '*35214*', \
'*41532*', '*2*1***'])
    False
    """
    board_str = ''
    for line in board:
        board_str += line
    board_columns = []
    num = len(board)
    for i in range(num):
        board_columns.append(board_str[i::num])
    return check_horizontal_visibility(board_columns)


def check_skyscrapers(input_path: str) -> bool:
    """
    Main function to check the status of skyscraper game board.
    Return True if the board status is compliant with the rules,
    False otherwise.
    """
    board = read_input(input_path)
    return check_not_finished_board(board) and\
           check_horizontal_visibility(board) and check_columns(board)


if __name__ == "__main__":
    print(check_skyscrapers("check.txt"))