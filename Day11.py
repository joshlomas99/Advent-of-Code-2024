def get_input(input_file: str='Inputs/Day11_Inputs.txt') -> dict:
    """
    Extract a list of numbers engraved on an arrangement of stones from an input file.

    Parameters
    ----------
    input_file : str, optional
        Input file giving the stones' engravings.
        The default is 'Inputs/Day11_Inputs.txt'.

    Returns
    -------
    stones : dict(int: int}
        Dictionary mapping each existing stone engraving and the number of stones with that
        engraving.

    """
    # Extract lines from input file
    with open(input_file) as f:
        # Split single input line and convert to integers
        lines = [int(n) for n in f.readlines()[0].strip().split()]
    # Build dictionary of counts of each existing stone type
    stones = {n: lines.count(n) for n in set(lines)}

    return stones

def blink(stones: dict) -> dict:
    """
    Determine the new arrangement of a series of stones with numbers engraved on them, after
    blinking a single time. Every time you blink, the stones each simultaneously change according
    to the first applicable rule in this list:
        - If the stone is engraved with the number 0, it is replaced by a stone engraved with the
          number 1.
        - If the stone is engraved with a number that has an even number of digits, it is replaced
          by two stones. The left half of the digits are engraved on the new left stone, and the
          right half of the digits are engraved on the new right stone. (The new numbers don't keep
          extra leading zeroes: 1000 would become stones 10 and 0.)
        - If none of the other rules apply, the stone is replaced by a new stone; the old stone's
          number multiplied by 2024 is engraved on the new stone.

    Parameters
    ----------
    stones : dict
        Dictionary mapping each existing stone engraving and the number of stones with that
        engraving.

    Returns
    -------
    new_stones : dict
        Dictionary of the new stone engravings after blinking once.

    """
    # Initialise new stones dictionary
    new_stones = dict()
    # Loop through current stones dict
    for n, count in stones.items():
        # If the stone is number 0, change to 1
        if n == 0:
            new_nums = 1,
        # Else for an even number of characters, split into two stones
        elif not len(str(n))%2:
            # Convert to string, split string and convert back to int
            string = str(n)
            new_nums = int(string[:len(string)//2]), int(string[len(string)//2:])
        # Else multiply stone by 2024
        else:
            new_nums = n*2024,
        # For each new stone, add the count of the stone type currently being considered to their
        # totals
        for new_n in new_nums:
            if new_n in new_stones:
                new_stones[new_n] += count
            else:
                new_stones[new_n] = count

    return new_stones

def Day11_Part1(input_file: str='Inputs/Day11_Inputs.txt') -> int:
    """
    Determines the number of stones with numbers engraved on them, whose initial arrangement is
    given in an input file, that you will have after blinking 25 times. Every time you blink, the
    stones each simultaneously change according to the first applicable rule in this list:
        - If the stone is engraved with the number 0, it is replaced by a stone engraved with the
          number 1.
        - If the stone is engraved with a number that has an even number of digits, it is replaced
          by two stones. The left half of the digits are engraved on the new left stone, and the
          right half of the digits are engraved on the new right stone. (The new numbers don't keep
          extra leading zeroes: 1000 would become stones 10 and 0.)
        - If none of the other rules apply, the stone is replaced by a new stone; the old stone's
          number multiplied by 2024 is engraved on the new stone.

    Parameters
    ----------
    input_file : str, optional
        Input file giving the initial stone arrangement.
        The default is 'Inputs/Day11_Inputs.txt'.

    Returns
    -------
    num_stones : int
        The total number of stones after 25 blinks.

    """
    # Parse input file to extract the initial numbers of each type of stone, in a dict
    stones = get_input(input_file)
    # Loop over 25 blinks
    for i in range(25):
        # Find the new numbers of each stone type after each blink
        stones = blink(stones)

    # At the end, sum up the counts of all types of stones
    num_stones = sum(stones.values())

    return num_stones

def Day11_Part2(input_file: str='Inputs/Day11_Inputs.txt') -> int:
    """
    Determines the number of stones with numbers engraved on them, whose initial arrangement is
    given in an input file, that you will have after blinking 75 times. Every time you blink, the
    stones each simultaneously change according to the first applicable rule in this list:
        - If the stone is engraved with the number 0, it is replaced by a stone engraved with the
          number 1.
        - If the stone is engraved with a number that has an even number of digits, it is replaced
          by two stones. The left half of the digits are engraved on the new left stone, and the
          right half of the digits are engraved on the new right stone. (The new numbers don't keep
          extra leading zeroes: 1000 would become stones 10 and 0.)
        - If none of the other rules apply, the stone is replaced by a new stone; the old stone's
          number multiplied by 2024 is engraved on the new stone.

    Parameters
    ----------
    input_file : str, optional
        Input file giving the initial stone arrangement.
        The default is 'Inputs/Day11_Inputs.txt'.

    Returns
    -------
    num_stones : int
        The total number of stones after 75 blinks.

    """
    # Parse input file to extract the initial numbers of each type of stone, in a dict
    stones = get_input(input_file)
    # Loop over 75 blinks
    for i in range(75):
        # Find the new numbers of each stone type after each blink
        stones = blink(stones)

    # At the end, sum up the counts of all types of stones
    num_stones = sum(stones.values())

    return num_stones

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
        print(f'{func.__name__} ran in {t2:.7f} seconds')
        return out
    return wrapper

from tqdm import tqdm

@time_function
def n_blinks(n):

    stones = get_input('Inputs/Day11_Inputs.txt')

    for i in tqdm(range(n)):
        stones = blink(stones)

    num_stones = sum(stones.values())

    print(len(stones))

    return stones
