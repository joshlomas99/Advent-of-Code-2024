from time import perf_counter

def time_function(func):
    """
    Decorator function to measure runtime of given function.

    Parameters
    ----------
    func : func
        Function to time.

    """
    def wrapper(*args, **kwargs):
        t1 = perf_counter()
        out = func(*args, **kwargs)
        t2 = perf_counter() - t1
        print(f'\n{func.__name__} ran in {t2:.7f} seconds')
        return out
    return wrapper

def get_input(input_file: str='Inputs/Day19_Inputs.txt') -> tuple:
    """
    Extract a list of towels and a series of designs from an input file.

    Parameters
    ----------
    input_file : str, optional
        Input file giving the towels and designs.
        The default is 'Inputs/Day19_Inputs.txt'.

    Returns
    -------
    towels : set(str)
        Set of all types of towel.
    designs : list(str)
        List of all towel designs.
    max_t_len : int
        Maximum length of any towel type.

    """
    # Parse input file and extract lines
    with open(input_file) as f:
        lines = [l.strip() for l in f.readlines()]

    # Extract towels on first line and designs on following lines
    towels = set(lines[0].split(', '))
    designs = lines[2:]
    # Find max length across all towel types
    max_t_len = max(len(t) for t in towels)

    return towels, designs, max_t_len

def is_possible(design: str, towels: set, max_t_len: int) -> bool:
    """
    Recursive function to find if a given towel design can be constructed from any number of a
    series of given towel types.

    Parameters
    ----------
    design : str
        Desired design.
    towels : set
        Set of available towel types.
    max_t_len : int
        Maximum length across all towel types.

    Returns
    -------
    is_possible : bool
        Whether the design is possible.

    """
    # If the design is in the towels, return True
    if design in towels:
        return True
    else:
        # Else loop through each potential towel to start this design with
        for i in range(1, min(max_t_len, len(design))+1):
            # If this towel exists
            if design[:i] in towels:
                # Check if what's left of the design can be constructed, if so return True
                if is_possible(design[i:], towels, max_t_len):
                    return True

    # If no possiblility was found, return False
    return False

@time_function
def Day19_Part1(input_file: str='Inputs/Day19_Inputs.txt') -> int:
    """
    Determines how many towel designs given in an input file can be constructed from a set of towel
    types given in the same input file.

    Parameters
    ----------
    input_file : str, optional
        Input file giving the designs and towel types.
        The default is 'Inputs/Day19_Inputs.txt'.

    Returns
    -------
    n_poss : int
        The number of possible designs.

    """
    # Parse input file to extract designs and towel types
    towels, designs, max_t_len = get_input(input_file)
    n_poss = 0
    # Loop over designs
    for design in designs:
        # Count how many are possible, determined using recursion
        n_poss += is_possible(design, towels, max_t_len)
    
    return n_poss

import functools

# Use a cache wrapper to massively speed up runtime
@functools.lru_cache(maxsize=None)
def num_ways(design: str, towels: tuple, max_t_len: int, not_composite: tuple) -> int:
    """
    Recursive function to find how many ways a given towel design can be constructed from any
    number of a series of given towel types.   

    Parameters
    ----------
    design : str
        Desired design.
    towels : tuple
        List of available towel types.
    max_t_len : int
        Maximum length across all towel types.
    not_composite : tuple
        List of which towel types cannot be broken down further into smaller towel types.

    Returns
    -------
    num : int
        The total number of ways the construct the given design.

    """
    # If this design is not composite, there is only 1 way to make it
    if design in not_composite:
        return 1
    else:
        # Else keep count
        num = 0
        # If the design is in towels, add 1
        if design in towels:
            num += 1
        # Then for each potential towel to start this design with
        for i in range(1, min(max_t_len, len(design)-1)+1):
            # If this towel exists
            if design[:i] in towels:
                # Recursively count how many ways to construct what's left of the design
                num += num_ways(design[i:], towels, max_t_len, not_composite)

    return num

from tqdm import tqdm

@time_function
def Day19_Part2(input_file: str='Inputs/Day19_Inputs.txt') -> int:
    """
    Determines the sum of the number of different ways you can make each of a series of designs
    given in an input file from a set of towel types given in the same input file.

    Parameters
    ----------
    input_file : str, optional
        Input file giving the designs and towel types.
        The default is 'Inputs/Day19_Inputs.txt'.

    Returns
    -------
    n_ways : int
        The total sum of the number of ways to construct each design.

    """
    # Parse input file to extract designs and towel types
    towels, designs, max_t_len = get_input(input_file)

    # Find which towels cannot be made from other towels in the set
    not_composite = tuple(t for t in towels if not is_possible(t, towels.difference({t}), max_t_len))
    # Convert towel set to a tuple to allow for memoization
    towels = tuple(towels)
    
    n_ways = 0
    # Loop over designs
    for design in tqdm(designs):
        # Add up the number of ways to make each design
        n_ways += num_ways(design, towels, max_t_len, not_composite)
    
    return n_ways
