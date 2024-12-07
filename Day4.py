import re
import numpy as np

def get_input(input_file: str='Inputs/Day4_Inputs.txt') -> list:
    """
    Extracts the contents of a word search from an input file.

    Parameters
    ----------
    input_file : str, optional
        Input file containing the word search.
        The default is 'Inputs/Day4_Inputs.txt'.

    Returns
    -------
    word_search : numpy.ndarray
        Word search split into characters in a 2D numpy array.

    """

    # Extract lines from input file
    with open(input_file) as f:
        # Split each row and column
        word_search = np.array([[c for c in l.strip()] for l in f.readlines()])

    return word_search

def count_word(word_search: list, word: str) -> int:
    """
    Counts all occurances of a given word from left to right in a given word search.

    Parameters
    ----------
    word_search : list
        Word search to search.
    word : str
        Word to search for.

    Returns
    -------
    count : int
        Number of occurences of the word in the word search from left to right.

    """
    # Join each row into a string from left to right
    word_search = [''.join(r) for r in word_search]
    # Use regex to count all occurences of the word in each row, and sum across all rows
    count = sum(len(re.findall(word, l)) for l in word_search)
    return count

def Day4_Part1(input_file: str='Inputs/Day4_Inputs.txt', search_word: str='XMAS') -> int:
    """
    Count the occurences of a given word in any direction in a word search given in an input file.

    Parameters
    ----------
    input_file : str, optional
        Input file containing the word search.
        The default is 'Inputs/Day4_Inputs.txt'.
    search_word : str, optional
        Word to search for.
        The default is 'XMAS'.

    Returns
    -------
    total : int
        Total occurences of the word.

    """
    # Parse input file
    word_search = get_input(input_file)
    # Rotate word search in each direction based on which way the words are arranged
    right = word_search.copy() # Words from left->right
    down = word_search.T # Words from top->bottom
     # Words from top-left->bottom-right, extract diagonals using shifted indentity matrix
    down_right = [word_search[np.eye(*word_search.shape, k=t)==1] \
                  for t in range(-word_search.shape[1], word_search.shape[0]-1)]
    # Words from top-right->bottom-left
    down_left = [word_search[np.fliplr(np.eye(*word_search.shape, k=t))==1] \
                 for t in range(-word_search.shape[1], word_search.shape[0]-1)]

    # Sum occerenes of word in four directions and the flipped word in the other four
    total = sum(count_word(ws, w) for ws in [right, down, down_right, down_left] \
                for w in [search_word, search_word[::-1]])

    return total

def Day4_Part2(input_file: str='Inputs/Day4_Inputs.txt') -> int:
    """
    Count all occurences of two MASes in the shape of an X in a word search given in an input file.

    Parameters
    ----------
    input_file : str, optional
        Input file containing the word search.
        The default is 'Inputs/Day4_Inputs.txt'.

    Returns
    -------
    total_x : int
        Total occurences of the X of MASes.

    """

    # Possible diagonal steps
    DIRECTIONS = [(-1, -1), (-1, 1), (1, 1), (1, -1)]
    # Parse input file
    word_search = get_input(input_file)
    # Count occurences
    total_x = 0
    for r in range(len(word_search)):
        for c in range(len(word_search[0])):
            # Find all 'A's
            if word_search[r, c] == 'A':
                # For each A, check all four diagonally adjacent characters
                diag = ''.join(word_search[r+d[0], c+d[1]] for d in DIRECTIONS \
                               # Check they are within the bounds of the word search
                               if 0 <= r+d[0] < len(word_search) and \
                                   0 <= c+d[1] < len(word_search[0]))
                # If there are two 'M's and two 'S's in the correct order then increase the count
                if diag.count('M') == 2 and diag.count('S') == 2 and \
                    ('MM' in diag or 'SS' in diag):
                    total_x += 1
    
    return total_x
