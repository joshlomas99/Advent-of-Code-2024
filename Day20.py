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

def get_input(input_file: str='Inputs/Day20_Inputs.txt') -> tuple:
    """
    Extracts the layout of a maze consisting of track (.) and walss (#) from an input file, as well
    as starting (S) and target (E) positions.

    Parameters
    ----------
    input_file : str, optional
        Input file giving the maze layout.
        The default is 'Inputs/Day20_Inputs.txt'.

    Returns
    -------
    maze : list(str)
        Maze layout
    walls : set(tuple(int))
        Set of wall coordinates.
    pos : tuple(int)
        Starting (x, y) position.
    end : tuple(int)
        Target (x, y) position.

    """
    # Parse input file and extract each line
    with open(input_file) as f:
        # Remove first and last row and column (outside walls around maze, not relevant)
        maze = [l.strip()[1:-1] for l in f.readlines()][1:-1]
    
    walls = set()
    # Loop through maze
    for r in range(len(maze)):
        for c in range(len(maze[r])):
            # Extract wall and start/target positions
            if maze[r][c] == '#':
                walls.add((r, c))
            elif maze[r][c] == 'S':
                pos = (r, c)
            elif maze[r][c] == 'E':
                end = (r, c)

    return maze, walls, pos, end

# Four orthogonal directions
DIRECTIONS = [(1, 0), (0, 1), (-1, 0), (0, -1)]

def print_maze(maze: list) -> None:
    """
    Print labelled maze visualisation.

    Parameters
    ----------
    maze : list(str)
        Maze layout

    Returns
    -------
    None.

    """
    print('  ' + ''.join(format(i, '2') for i in range(len(maze[0]))))
    for r in range(len(maze)):
        print(format(r, '2') + ' ' + ' '.join(maze[r]))


def shortest_dists(maze: list, pos: tuple) -> dict:
    """
    Uses Djikstra's algorithm to find the shortest distance from a given point in a maze to every
    other point, including wall (#) points connected directly to track (.), where only track (.)
    can be travelled over.

    Parameters
    ----------
    maze : list(str)
        Maze layout
    pos : tuple(int)
        Starting (x, y) position.

    Returns
    -------
    dict
        DESCRIPTION.

    """
    # Find boundaries of maze
    bounds = (len(maze), len(maze[0]))
    # Track minimum discovered distance to each valid point
    min_dist = {pos: 0}
    # Start queue of points to check and set of already checked points
    queue, found = {pos}, set()
    # While there are points to check
    while queue:
        # Find remaining position with minimum distance
        pos = min(queue, key=lambda q: min_dist[q])
        # Remove from queue
        queue.discard(pos)
        # Try to move in every direction
        for d in DIRECTIONS:
            # Find new position
            new_pos = (pos[0]+d[0], pos[1]+d[1])
            # If we are outside the maze boundaries, skip
            if not (0 <= new_pos[0] < bounds[0] and 0 <= new_pos[1] < bounds[1]):
                continue
            # Else if we haven't found this point already and it isn't a rock, add to the queue
            if new_pos not in found and maze[new_pos[0]][new_pos[1]] != '#':
                queue.add(new_pos)
            # If the point is new or the new distance is shorted than the current value, update
            # the minimum distance to this point in the dict
            if new_pos in min_dist:
                if min_dist[pos] + 1 < min_dist[new_pos]:
                    min_dist[new_pos] = min_dist[pos] + 1
            else:
                min_dist[new_pos] = min_dist[pos] + 1
        # Add checked position to set of found points
        found.add(pos)

    return min_dist

from collections import defaultdict

@time_function
def Day20_Part1(input_file: str='Inputs/Day20_Inputs.txt') -> int:
    """
    Determines how many cheats would save you at least 100 picoseconds in a race from the start
    to the end position in a maze, whose layout is given in an input file. The maze consists of
    track (.) and walls (#) and usually only track can be travelled on. However, exactly once
    during a race, wall collisions can be disabled for up to 2 picoseconds, allowing you to pass
    through walls as if they were regular track. At the end of the cheat, you must be back on
    normal track again, or you will get disqualified.

    Parameters
    ----------
    input_file : str, optional
        Input file giving the maze layout.
        The default is 'Inputs/Day20_Inputs.txt'.

    Returns
    -------
    num_saving_100 : int
        Number of distinct cheats which save at least 100 picoseconds.

    """
    # Parse input file to extract maze layout, wall positions and start/target coordinates
    maze, walls, pos, end = get_input(input_file)
    # Use Djikstra's algorithm to find the shortest distance from the start position to every
    # other point which is either track or a wall connected orthogonally to track
    dist_from_start = shortest_dists(maze, pos)
    # Same but from every point to the target position
    dist_to_end = shortest_dists(maze, end)

    # Find coordinates of every wall which was found by Djikstra's and so is connected to at least
    # one track
    connected_walls = [w for w in walls if w in dist_from_start]

    # Track numbers of cheats giving a given amount of time saving
    savings = defaultdict(int)
    # Try each wall connected to track as the one to pass through
    for wall in connected_walls:
        # Find the corresponding distance from start to target positions through this wall and
        # subtract default distance without cheats to find saving, increment corresponding counter
        savings[dist_from_start[end] - (dist_from_start[wall] + dist_to_end[wall])] += 1

    # Sum numbers of cheats giving savings of at least 100
    num_saving_100 = sum(v for k, v in savings.items() if k >= 100)
    
    return num_saving_100

from itertools import combinations
from math import factorial as fact
from tqdm import tqdm

@time_function
def Day20_Part2(input_file: str='Inputs/Day20_Inputs.txt') -> int:
    """
    Determines how many cheats would save you at least 100 picoseconds in a race from the start
    to the end position in a maze, whose layout is given in an input file. The maze consists of
    track (.) and walls (#) and usually only track can be travelled on. However, exactly once
    during a race, wall collisions can now be disabled for an increased period of up to 20
    picoseconds, allowing you to pass through walls as if they were regular track. At the end of
    the cheat, you must be back on normal track again, or you will get disqualified.

    Parameters
    ----------
    input_file : str, optional
        Input file giving the maze layout.
        The default is 'Inputs/Day20_Inputs.txt'.

    Returns
    -------
    num_saving_100 : int
        Number of distinct cheats which save at least 100 picoseconds.

    """
    # Parse input file to extract maze layout, wall positions and start/target coordinates
    maze, walls, pos, end = get_input(input_file)

    # Use Djikstra's algorithm to find the shortest distance from the start position to every
    # other point which is either track or a wall connected orthogonally to track
    dist_from_start = shortest_dists(maze, pos)
    # Same but from every point to the target position
    dist_to_end = shortest_dists(maze, end)

    # Find the coordinates of every track in the maze
    tracks = [(r, c) for r in range(len(maze)) for c in range(len(maze[0])) if (r, c) not in walls]
    
    # Track numbers of cheats giving a given amount of time saving
    savings = defaultdict(int)
    # Try every possible combination of two different track positions to attempt to use the cheat
    # to travel between
    for cheat_start, cheat_end in tqdm(combinations(tracks, 2),
                                     total=fact(len(tracks))//(fact(len(tracks) - 2)*fact(2))):
        # Find the Manhattan distance between these points
        man_dist = abs(cheat_end[0] - cheat_start[0]) + abs(cheat_end[1] - cheat_start[1])
        # If it is at most 20, this is a valid cheat
        if man_dist <= 20:
            # Find the optimal direction in which to use this cheat, and the corresponding total
            # time taken for this route
            min_dist = min(dist_from_start[cheat_start] + dist_to_end[cheat_end] + man_dist,
                           dist_from_start[cheat_end] + dist_to_end[cheat_start] + man_dist)
            # Find the saving relative to the distance without cheats and increment counter
            savings[dist_from_start[end] - min_dist] += 1
    
    # Sum numbers of cheats giving savings of at least 100
    num_saving_100 = sum(v for k, v in savings.items() if k >= 100)
    
    return num_saving_100
