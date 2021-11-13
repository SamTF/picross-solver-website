### IMPORTS
from flask import Flask, send_from_directory        # The Main Flask App thing, and sfd to serve static files from local directory
import json                                         # To parse and send JSON objects to and from the svelte front-end

import random                                       # TEMP just for testing/fun

import picross_origins as pic                       # My module that solves picross puzzles!
import pycross                                      # Stripped down version of Pycross to generate random puzzles and their matching block guides

from typing import Dict, List                       # Type hinting



### INITIALISING APP
app = Flask(__name__)


### ROUTES
# SVELTE :: Path for our main Svelte page
@app.route("/")
def base():
    return send_from_directory('svelte-frontend/public', 'index.html')
# SVELTE :: Path for all the static files (compiled JS/CSS, etc.)
@app.route("/<path:path>")
def home(path):
    return send_from_directory('svelte-frontend/public', path)


# BACKEND :: Random number API
@app.route('/rand')
def rand():
    return str(random.randint(0, 100))

# BACKEND :: Random picross puzzle
@app.route('/rand_board/<size>')
def rand_board(size:int = 5):
    try:
        return pycross.rand_board(size)
    except ValueError:
        return {"success" : False, "data" : "ERROR @ [rand_board] >>> SIZE value must be an integer"}

# BACKEND :: Receving the Picross puzzle info from the front-end as a JSON string in the format {rows: [1,2,3], cols: [4,5,6]}
@app.route('/solve/<object>')
def solve(object):
    print('>>> Recieved request to solve Picross puzzle:')
    data = json.loads(object) # converting the JSON String into a Python Dictionary
    print(data)
    print(type(data))
    # formatted_data = format_input(data) # formatting the data client-side. can be reversed if needed. not sure which approach is better.

    if is_valid_input(data):
        print("###### Input is valid! #######")
    else:
        return { 'data' : "invalid input!", 'success' : False }
        

    try:
        solution = pic.solve(data)
        print(solution)
        solution = zeros_and_ones(solution)
        success = True
    except RecursionError:
        solution = "ERROR: No solution possible, or puzzle has multiple solutions. This solver only works for single solution puzzles!"
        success = False

    return { 'data' : solution, 'success' : success }


#### INPUT VALIDATION & FORMATTING #######################################
def is_valid_input(input_data:dict) -> bool:
    '''
    Checks if the given input matches the required format: a dictionary containing keys "rows" and "cols", whose values are a 2D list of ints.
    '''
    keys = ["rows", "cols"]

    # Checking if the input is a dict
    if not type(input_data) is dict:
        return False

    # Checking if the input has the required keys
    if not all(k in input_data.keys() for k in keys):
        return False
    
    # Checking if the dict's values are nested lists of integers
    for key, value in input_data.items():
        if not type(value) == list and all(type(x) == int for x in value):
            return False
    
    # True if all conditions above are true
    return True


def format_input(object:Dict[str, List[str]]) -> Dict[str, List[List[int]]]:
    '''
    Takes the JSON dict with its list of strings and converts it into the required format: two keys (row/col), each containing a main list housing a sub-list of integers.
    '''
    return {axis: [f(block) for block in line] for axis, line in object.items()} # list comp within dict comp. iterating over all elements in a line, and formatting them, for all dict keys

def f(value:str) -> List[int]:
    '''
    Converts a string of numbers into a list of integers
    '''
    return [int(v) for v in value.split()]


def zeros_and_ones(solution:List[str]) -> List[int]:
    '''
    Converting the CLI-friendly puzzle of Xs and Dots into 1s and 0s for the front-end to render.
    '''
    lookup = {'.' : 0, 'X' : 1, '?' : 0}
    formatted = [[lookup[x] for x in row] for row in solution]
    return formatted


### RUNNING THE APP
if __name__ == "__main__":
    app.run(port=5000)
else:
    print("APP IMPORTED")