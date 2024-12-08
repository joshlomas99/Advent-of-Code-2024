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

import numpy as np

def get_input(input_file: str='Inputs/Day6_Inputs.txt') -> tuple:
    """
    Extracts a series of lines describing a map of the layout of a room, where empty space is
    represented by '.' and obstacles are represented by '#'. In addition, the start position and
    direction faced by a guard are extracted, given by either '<', '>', 'v' or '^' depending on the
    direction.

    Parameters
    ----------
    input_file : str, optional
        Input file giving the map.
        The default is 'Inputs/Day6_Inputs.txt'.

    Raises
    ------
    Exception
        If an unrecognised symbol is found in the input map.

    Returns
    -------
    lines : np.ndarray
        2D numpy array of characters giving the map layout.
    start_pos : tuple(int)
        Starting coordinates of the guard.
    start_facing : tuple(int)
        Initial direction faced by the guard.

    """
    # Extract lines from input file and split into characters
    with open(input_file) as f:
        lines = np.array([[c for c in l.strip()] for l in f.readlines()])
    
    # Search through the map for the guard's position
    r = 0
    start_pos = None
    while r < len(lines):
        c = 0
        while c < len(lines[0]):
            # When the guard is found
            if lines[r, c] not in ['.', '#']:
                # Record their position
                start_pos = (r, c)
                # Depending on the character, record the direction they're facing
                if lines[r, c] == '^':
                    start_facing = (-1, 0)
                elif lines[r, c] == '>':
                    start_facing = (0, 1)
                elif lines[r, c] == 'v':
                    start_facing = (1, 0)
                elif lines[r, c] == '<':
                    start_facing = (0, -1)
                else:
                    raise Exception(f"Unrecognised symbol {lines[r, c]}!")
                break
            c += 1
        if start_pos:
            break
        r += 1

    return lines, start_pos, start_facing

# Map of direction changes corresponding to a 90 degree turn to the right (clockwise)
TURNS = {(-1, 0): (0, 1),
         (0, 1): (1, 0),
         (1, 0): (0, -1),
         (0, -1): (-1, 0)}

def Day6_Part1(input_file: str='Inputs/Day6_Inputs.txt') -> int:
    """
    Determines how many distinct positions a guard will visit in a room before leaving a mapped
    area given in an input file. In the map empty space is represented by '.' and obstacles are
    represented by '#'. In addition, the start position and direction faced by a guard are
    extracted, given by either '<', '>', 'v' or '^' depending on the direction. The guard will step
    forward in the direction they are facing, unless there is something directly in front of them,
    then they turn right 90 degrees (clockwise).

    Parameters
    ----------
    input_file : str, optional
        Input file giving the map.
        The default is 'Inputs/Day6_Inputs.txt'.

    Returns
    -------
    num_pos : int
        The number of unique positions visited by the guard.

    """
    # Parse the input file and extract the map and the guard's initial position and direction
    lines, start_pos, start_facing = get_input(input_file)
    # Track set of all positions visited
    all_pos = {start_pos}
    # Start position and direction
    pos = start_pos
    facing = start_facing
    # While the guard is within the bounds of the map
    while 0 <= pos[0] + facing[0] < len(lines) and 0 <= pos[1] + facing[1] < len(lines[0]):
        # If the next space in the current direction is empty
        if lines[pos[0] + facing[0], pos[1] + facing[1]] != '#':
            # Move into the new position
            pos = (pos[0] + facing[0], pos[1] + facing[1])
            # Add to the set
            all_pos.add(pos)
        else:
            # Else turn to the right 90 degrees
            facing = TURNS[facing]

    # Find the length of the full set of unique positions
    num_pos = len(all_pos)

    return num_pos

def print_map(lines, all_pos):
    """
    Draw the map with all visited positions and the direction faced when they were visited.

    Parameters
    ----------
    lines : numpy.ndarray
        2D numpy array describing the map layout.
    all_pos : dict(tuple(int): set(tuple(int)))
        Dictionary of all positions visited, and each direction faced while in that position.

    Returns
    -------
    None.

    """
    # Label each column
    print(' ' + ''.join(str(c) for c in range(len(lines[0]))))
    for r in range(len(lines)):
        for c in range(len(lines[r])):
            # If visited position
            if (r, c) in all_pos:
                if len(all_pos[r, c]) > 1:
                    # If facing multiple ways, label with '+'
                    lines[r, c] = '+'
                # Else label according to direction
                else:
                    if (-1, 0) in all_pos[r, c]:
                        lines[r, c] = '^'
                    elif (0, 1) in all_pos[r, c]:
                        lines[r, c] = '>'
                    elif (1, 0) in all_pos[r, c]:
                        lines[r, c] = 'v'
                    elif (0, -1) in all_pos[r, c]:
                        lines[r, c] = '<'
        # Print and label each row
        print(str(r)+''.join(lines[r]))

def does_loop(pos, facing, lines, all_pos):
    """
    Determine if a loop is reached in the path taken by a guard starting in a given position,
    facing in a given direction, in a room of a given layout where empty space is represented by
    '.' and obstacles are represented by '#', and the guard will always move forward if within the
    map's boundaries, unless they reach an obstacle when they turn 90 degrees to the right.

    Parameters
    ----------
    pos : tuple(int)
        Initial position.
    facing : tuple(int)
        Initial direction faced.
    lines : numpy.ndarray
        2D numpy array giving the map layout.
    all_pos : dict(tuple(int): set(tuple(int)))
        Dictionary of all positions visited before, and each direction faced while in that position.

    Returns
    -------
    does_loop : bool
        Whether the path loops or not.

    """
    # While the guard is within the bounds of the map
    while 0 <= pos[0] + facing[0] < len(lines) and 0 <= pos[1] + facing[1] < len(lines[0]):
        # If the next space in the current direction is empty
        if lines[pos[0] + facing[0], pos[1] + facing[1]] != '#':
            # Move into the new position
            pos = (pos[0] + facing[0], pos[1] + facing[1])
            # If this position was visited before
            if pos in all_pos:
                # If it was visited while facing in the same direction, this must be a loop
                if facing in all_pos[pos]:
                    return True
                # Else add this direction to the set for this position
                all_pos[pos].add(facing)
            else:
                # Or initialise the set with this direction
                all_pos[pos] = {facing}
        else:
            # Else turn to the right 90 degrees
            facing = TURNS[facing]
            # Add the new direction faced to the set for this position
            all_pos[pos].add(facing)

    # If the guard has left the map, no loop was found so return False
    return False

@time_function
def Day6_Part2(input_file: str='Inputs/Day6_Inputs.txt') -> int:
    """
    Determine how many different positions could be chosen for an additional obstruction added to a
    map given in an input file, such that a guard starting at a position given in the map would
    become stuck in a loop before leaving the map boundaries. In the map, empty space is
    represented by '.' and obstacles are represented by '#', and the guard will always move forward 
    if within the map's boundaries, unless they reach an obstacle when they turn 90 degrees to the
    right.

    Parameters
    ----------
    input_file : str, optional
        Input file giving the map layout.
        The default is 'Inputs/Day6_Inputs.txt'.

    Returns
    -------
    possible_obs_pos : int
        Number of possible positions to add an obstacle and cause a loop in the guard's path.

    """
    # Parse the input file and extract the map and the guard's initial position and direction
    lines, start_pos, start_facing = get_input(input_file)
    # Track all new obstacle positions which cause a loop
    extra_obs_pos = set()
    # Track all positions visited by the guard and the directions faced while in these positions
    all_pos = {start_pos: {start_facing}}
    # Start position and direction
    pos = start_pos
    facing = start_facing
    # While the guard is within the bounds of the map
    while 0 <= pos[0] + facing[0] < len(lines) and 0 <= pos[1] + facing[1] < len(lines[0]):
        # If the next space in the current direction is empty and not already visited by the guard
        if lines[pos[0] + facing[0], pos[1] + facing[1]] != '#' and \
            (pos[0] + facing[0], pos[1] + facing[1]) not in all_pos:
            # Create copy of map
            extra_obs = lines.copy()
            # And set the next position in the direction faced by the guard to an obstacle
            extra_obs[pos[0] + facing[0], pos[1] + facing[1]] = '#'
            # If a loop is found with the new obstacle
            if does_loop(pos, facing, extra_obs, {k: v.copy() for k, v in all_pos.items()}):
                # Add this position to the set
                extra_obs_pos.add((pos[0] + facing[0], pos[1] + facing[1]))
        # If the next space in the current direction is empty
        if lines[pos[0] + facing[0], pos[1] + facing[1]] != '#':
            # Move into the new position
            pos = (pos[0] + facing[0], pos[1] + facing[1])
            # If this position was visited before
            if pos in all_pos:
                # Add this direction to the set for this position
                all_pos[pos].add(facing)
            else:
                # Or initialise the set with this direction
                all_pos[pos] = {facing}
        else:
            # Else turn to the right 90 degrees
            facing = TURNS[facing]
            # Add the new direction faced to the set for this position
            all_pos[pos].add(facing)

    # Find number of possible new obstacle positions
    possible_obs_pos = len(extra_obs_pos)

    return possible_obs_pos
