import numpy as np
from typing import List, Dict


def rand_board(size:int = 5) -> List[List[int]]:
    '''
    Generates a random picross puzzle. Returns the puzzle as a 2D Array of 1s and 0s.
    '''
    try:
        size = int(size)
    except:
        error = "ERROR @ [rand_board] >>> SIZE value must be an integer"
        raise ValueError(error)

    print(f'\n>>> Requesting Picross puzzle of size: {size}')
    board = np.random.randint(2, size=(size, size))
    guides = create_guides(board)

    return {"board" : board.tolist(), "blocks" : guides, "success" : True}


def create_guides(board) -> Dict[str, List[int]]:
    '''
    Generates the number guides for both axis on the board. Returns a dictionary of lists.
    '''
    guides = {}
    guides['rows'] = create_axis_guides(board)
    guides['cols'] = create_axis_guides(board.T)

    return guides


def create_axis_guides(board) -> List[int]:
    '''
    Generates a number guide for each line in a single axis. Returns a list of ints.
    '''
    axis_guides = []

    # loops through every row/column
    for row in board:
        zeroes = (np.where(row == 0))[0]                                    # gets the indices of all values equal to the Blank Space value (0) as an array
        split_arrays = np.split(row, zeroes)                                # splits the array at each blank value into sub arrays
        g = np.array([i.sum() for i in split_arrays])                       # sums each the split array and combines the result into a single array (counts how many consecutive filled spaces there are)
        guide = g[g != 0]                                                   # filters out the zeroes
        if guide.size == 0: guide = np.array([0])                           # adds a single zero if the array is empty
        
        guide = guide.tolist()                                              # converts the np array to a normal python list (for readability in the console)

        axis_guides.append(guide)                                           # appends the current axis guide to the overall axis guides array
    
    return axis_guides


if __name__ == "__main__":
    rand_board(100)
else:
    print("PYCROSS IMPORTED")