def get_input(input_file: str='Inputs/Day18_Inputs.txt') -> tuple:
    """
    Extracts a list of coordinates for where bytes will fall into a memory space.

    Parameters
    ----------
    input_file : str, optional
        Input file giving the byte coordinates.
        The default is 'Inputs/Day18_Inputs.txt'.

    Returns
    -------
    bytes_pos : list(tuple(int))
        List of (X, Y) byte coordinates.
    bounds : tuple(int)
        Dimensions of the full memory space.

    """
    # Extract lines from input file
    with open(input_file) as f:
        # Convert each coordinate to tuple
        bytes_pos = [tuple(int(i) for i in l.strip().split(',')) for l in f.readlines()]

    # Find maximum coordinate to give bounds
    bounds = (max(max(p) for p in bytes_pos),)*2

    return bytes_pos, bounds

# Define all orthogonal movements
DIRECTIONS = [(1, 0), (0, 1), (-1, 0), (0, -1)]

def find_min_dist_to_exit(num_fallen: int, bytes_pos: list, bounds: tuple, start_pos: tuple=(0, 0)):
    """
    Find the minimum number of steps required to move from a given start position to a given
    end position defined by the boundaries of the space you are in, given the coordinates of a
    series of bytes which are falling into the space, and the number of these which have fallen.

    Parameters
    ----------
    num_fallen : int
        Number of bytes which have fallen into the space.
    bytes_pos : list(tuple(int))
        List of byte coordinates once they fall into the space (in order).
    bounds : tuple(int)
        Dimensions of the full space, and end position.
    start_pos : tuple(int), optional
        Start position in space.
        The default is (0, 0).

    Returns
    -------
    min_dist : int or None
        The minimum number of steps to get from the start to the end position. If there is no
        valid path, returns None.

    """
    # Extract the coordinates of all bytes which have fallen into place
    fallen_bytes = set(bytes_pos[:num_fallen])
    pos = start_pos
    # Queue of positions left to check, and set of already checked positions
    queue, found = {pos}, set()
    # Track minimum found distances to each point
    dist = {pos: 0}
    # While there are places left to check
    while queue:
        # Find the position in the queue with the minimum distance from the start point
        pos = min(queue, key=lambda q: dist[q])
        # Remove it from the queue
        queue.discard(pos)
        # Check every option for the next step
        for d in DIRECTIONS:
            # Find new coordinate after step
            new_pos = (pos[0]+d[0], pos[1]+d[1])
            # If we go outside the space bounaries, this is not valid so continue
            if not (0 <= new_pos[0] <= bounds[0] and 0 <= new_pos[1] <= bounds[1]):
                continue
            # If this spot isn't a fallen byte
            if new_pos not in fallen_bytes:
                # If we haven't seen this position before, add to the queue
                if new_pos not in found:
                    queue.add(new_pos)
                # If position is new, or if this is a new minimum score to this position,
                # update dictionary with this value
                if new_pos in dist:
                    if dist[pos] + 1 < dist[new_pos]:
                        dist[new_pos] = dist[pos] + 1
                else:
                    dist[new_pos] = dist[pos] + 1
        # Note that we have checked this state
        found.add(pos)

    # If the end position has been found
    if bounds in dist:
        # Return minimum distance to the end position
        return dist[bounds]
    # Else return None
    else:
        return None

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

@time_function
def Day18_Part1(input_file: str='Inputs/Day18_Inputs.txt', num_fallen: int=1024) -> int:
    """
    Determines the minimum number of steps needed to reach the exit in the bottom right corner of
    a memory space, starting from the top left corner, after the first 1024 of set of bytes, whose
    coordinates once they fall are given in an input file, have fallen onto the memory space.

    Parameters
    ----------
    input_file : str, optional
        Input file giving the fallen bytes coordinates, in the order that they fall.
        The default is 'Inputs/Day18_Inputs.txt'.
    num_fallen : int, optional
        The number of bytes which have fallen when we move through the space.
        The default is 1024.

    Returns
    -------
    min_dist : int
        The minimum steps required to reach the exit after 1024 bytes have fallen.

    """
    # Parse input file to extract fallen bytes coordinates
    bytes_pos, bounds = get_input(input_file)

    # Use Djikstra's algorithm to find the minimum distance to the exit
    min_dist = find_min_dist_to_exit(num_fallen, bytes_pos, bounds)

    return min_dist

@time_function
def Day18_Part2(input_file: str='Inputs/Day18_Inputs.txt') -> str:
    """
    Finds the coordinates of the first of a series of bytes which are falling into a memory space,
    that will prevent the exit in the bottom right corner from being reachable from the starting
    position at the top left corner. The coordinates of eachg byte once they have fallen, in the
    order in which they fall, are given in an input file.

    Parameters
    ----------
    input_file : str, optional
        Input file giving the fallen bytes coordinates, in the order that they fall.
        The default is 'Inputs/Day18_Inputs.txt'.

    Returns
    -------
    first_blockage : str
        The coordinates of the first byte which blocks the route, as two integers separated by a
        comma.

    """
    # Parse input file to extract fallen bytes coordinates
    bytes_pos, bounds = get_input(input_file)

    # Perform binary search for the first number of fallen bytes which has no valid path from
    # the start to the end position
    # Start with the boundaries of the full list
    L, R = 0, len(bytes_pos) - 1
    while L <= R:
        # If L and R are one apart, the solution must be L-1
        if R - L <= 1:
            break
        # Find the midpoint
        m = (L + R) // 2
        # If there is still a valid path at this point, the solution is higher so set L to one
        # above this value
        if find_min_dist_to_exit(m, bytes_pos, bounds) is not None:
            L = m + 1
        # Else the solution is lower, so set R to this value
        else:
            R = m

    # Find the corresponding coordinate and join the values with a comma
    first_blockage = ','.join(str(i) for i in bytes_pos[L-1])
    
    return first_blockage
