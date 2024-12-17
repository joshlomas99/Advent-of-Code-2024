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

def get_input(input_file: str='Inputs/Day16_Inputs.txt') -> tuple:
    """
    Extract a map of a maze from an input file, including start and end coordinates.

    Parameters
    ----------
    input_file : str, optional
        Input file giving the maze.
        The default is 'Inputs/Day16_Inputs.txt'.

    Returns
    -------
    maze : list(str)
        Map of the maze layout.
    pos : tuple(int)
        Starting coordinates in the maze.
    facing : tuple(int)
        Starting direction faced.
    end : tuple (int)
        Target coordinates in the maze.

    """
    # Extract lines from input file
    with open(input_file) as f:
        maze = [l.strip() for l in f.readlines()]
    # Loop through maze and find start and end coordinates
    for r, row in enumerate(maze):
        # print(row)
        if 'S' in row:
            pos = (r, row.index('S'))
        if 'E' in row:
            end = (r, row.index('E'))
            maze[r] = row.replace('E', '.')

    # Start facing east
    facing = (0, 1)

    return maze, pos, facing, end

# Map of direction changes for both types of 90 degree turn
TURN_CW = {(0, 1): (1, 0), (1, 0): (0, -1), (0, -1): (-1, 0), (-1, 0): (0, 1)}
TURN_ACW = {(0, 1): (-1, 0), (-1, 0): (0, -1), (0, -1): (1, 0), (1, 0): (0, 1)}

@time_function
def Day16_Part1(input_file: str='Inputs/Day16_Inputs.txt') -> int:
    """
    Determines the lowest score a Reindeer could possibly get travelling from the start to the end
    of a maze, whose layout is given in an input file. The Reindeer start on the Start Tile
    (marked S) facing East and need to reach the End Tile (marked E). They can move forward one
    tile at a time (increasing their score by 1 point), but never into a wall (#). They can also
    rotate clockwise or counterclockwise 90 degrees at a time (increasing their score by 1000
    points).

    Parameters
    ----------
    input_file : str, optional
        Input file giving the maze layout.
        The default is 'Inputs/Day16_Inputs.txt'.

    Returns
    -------
    min_score : int
        The minimum possible score required to reach the end of the maze.

    """
    # Parse input file to extract maze layout and start and end coordinates
    maze, pos, facing, end = get_input(input_file)

    # Track minimum found distances to each point whie facing in a given direction
    dist = {(pos, facing): 0}
    # Queue of states left to check, and set of already checked states
    queue, found = {(pos, facing)}, set()
    # While there are places left to check
    while queue:
        # Find the state in the queue with the minimum distance from the start point
        pos, facing = min(queue, key=lambda q: dist[q])
        # Remove it from the queue
        queue.discard((pos, facing))
        # Check every option (turn left, go straight, turn right)
        for s, d in [(1001, TURN_ACW[facing]), (1, facing), (1001, TURN_CW[facing])]:
            # Find new coordinate after step
            new_pos = (pos[0]+d[0], pos[1]+d[1])
            # If this spot isn't a wall
            if maze[new_pos[0]][new_pos[1]] == '.':
                # If we haven't seen this position before, add to the queue
                if (new_pos, d) not in found:
                    queue.add((new_pos, d))
                # If position is new, or if this is a new minimum score to this position,
                # update dictionary with this value
                if (new_pos, d) in dist:
                    if dist[pos, facing] + s < dist[new_pos, d]:
                        dist[new_pos, d] = dist[pos, facing] + s
                else:
                    dist[new_pos, d] = dist[pos, facing] + s
        # Note that we have checked this state
        found.add((pos, facing))

    # Find minimum score for getting to the end position, facing in any direction
    min_score = min(v for k, v in dist.items() if k[0] == end)
    
    return min_score

@time_function
def Day16_Part2(input_file: str='Inputs/Day16_Inputs.txt') -> int:
    """
    Determines how many tiles are part of at least one of the best paths from the start to the end
    of a maze, whose layout is given in an input file. The Reindeer start on the Start Tile
    (marked S) facing East and need to reach the End Tile (marked E). They can move forward one
    tile at a time (increasing their score by 1 point), but never into a wall (#). They can also
    rotate clockwise or counterclockwise 90 degrees at a time (increasing their score by 1000
    points).

    Parameters
    ----------
    input_file : str, optional
        Input file giving the maze layout.
        The default is 'Inputs/Day16_Inputs.txt'.

    Returns
    -------
    num_pos : int
        The number of unique positions which are part of at least one of the best paths through
        the maze.

    """
    # Parse input file to extract maze layout and start and end coordinates
    maze, pos, facing, end = get_input(input_file)

    # Track minimum found distances to each point whie facing in a given direction
    dist = {(pos, facing): 0}
    # Track paths to each point while facing in a given direction with the current minimum score
    paths = {(pos, facing): [[pos]]}
    # Queue of states left to check, and set of already checked states
    queue, found = {(pos, facing)}, set()
    # While there are places left to check
    while queue:
        # Find the state in the queue with the minimum distance from the start point
        pos, facing = min(queue, key=lambda q: dist[q])
        # Remove it from the queue
        queue.discard((pos, facing))
        # Check every option (turn left, go straight, turn right)
        for s, d in [(1001, TURN_ACW[facing]), (1, facing), (1001, TURN_CW[facing])]:
            # Find new coordinate after step
            new_pos = (pos[0]+d[0], pos[1]+d[1])
            # If this spot isn't a wall
            if maze[new_pos[0]][new_pos[1]] == '.':
                # If we haven't seen this position before, add to the queue
                if (new_pos, d) not in found:
                    queue.add((new_pos, d))
                # If position is new, or if this is a new minimum score to this position,
                # update dictionary with this value and update the list of paths to this point
                # with this minimum score
                if (new_pos, d) in dist:
                    if dist[pos, facing] + s < dist[new_pos, d]:
                        dist[new_pos, d] = dist[pos, facing] + s
                        paths[new_pos, d] = [p + [new_pos] for p in paths[pos, facing]]
                    # If score matches the current minimum found, add this path to the list of
                    # paths being tracked
                    elif dist[pos, facing] + s == dist[new_pos, d]:
                        paths[new_pos, d] += [p + [new_pos] for p in paths[pos, facing]]
                else:
                    dist[new_pos, d] = dist[pos, facing] + s
                    paths[new_pos, d] = [p + [new_pos] for p in paths[pos, facing]]
        # Note that we have checked this state
        found.add((pos, facing))

    # Find minimum score for getting to the end position, facing in any direction
    min_score = min(v for k, v in dist.items() if k[0] == end)
    # Find number of unique positions in paths leading to the end position, facing in any
    # direction,  while achieving the minimum score found for this position
    num_pos = len(set(pos for k, v in paths.items() for path in v for pos in path \
                      if k[0] == end and dist[k] == min_score))
    
    return num_pos
