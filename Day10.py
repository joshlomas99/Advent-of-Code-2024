import numpy as np

def get_input(input_file: str='Inputs/Day10_Inputs.txt') -> tuple:
    """
    Extracts a topographic map from an input file, where each point indicates the height at that
    position using a scale from 0 (lowest) to 9 (highest).

    Parameters
    ----------
    input_file : str, optional
        Input file containing the map.
        The default is 'Inputs/Day10_Inputs.txt'.

    Returns
    -------
    lines : numpy.ndarray
        Numpy array of extracted map, split by individual position.

    trailheads : dict(tuple(int): int)
        Dictionary mapping the positions of every point with zero height, to the number of trails
        found from that point.

    bounds : tuple(int)
        Tuple giving the height and width of the topographic map.

    """
    # Extract lines from input file
    with open(input_file) as f:
        # Split each row by character and convert to integers
        lines = np.array([[int(i) for i in l.strip()] for l in f.readlines()])

    # Find each coordinate with 0 height
    trailheads = {(r, c): 0 for r in range(len(lines)) for c in range(len(lines[0])) if lines[r, c] == 0}
    # Found bounds of map
    bounds = np.array((len(lines), len(lines[0])))

    return lines, trailheads, bounds

# Four orthogonal directions
DIRECTIONS = [np.array(d) for d in [(0, 1), (1, 0), (0, -1), (-1, 0)]]

def Day10_Part1(input_file: str='Inputs/Day10_Inputs.txt') -> int:
    """
    Finds the sum of the scores of all trailheads on a topographic map given in an input file,
    where a hiking trail is any path that starts at height 0, ends at height 9, and always
    increases by a height of exactly 1 at each step. Hiking trails never include diagonal steps -
    only up, down, left, or right (from the perspective of the map). A trailhead is any position
    that starts one or more hiking trails - here, these positions will always have height 0. The
    score of a trailhead is the number of 9-height positions reachable from that trailhead via a
    hiking trail.

    Parameters
    ----------
    input_file : str, optional
        Input file giving the topographic map.
        The default is 'Inputs/Day10_Inputs.txt'.

    Returns
    -------
    total_score : int
        The sum of the scores of all trailheads on the map.

    """
    # Parse input file to extract map layout, the position of each trailhead and the map bounds
    lines, trailheads, bounds = get_input(input_file)

    # Loop through trailheads
    for th in trailheads:
        # Track positions reached on this step
        trails = [np.array(th)]
        # Loop from the next step being height 1 up to 9
        for i in range(1, 10):
            # Track valid next steps
            new_trails = []
            # For each trail being tracked
            for pos in trails:
                # Add each valid next step (height == i) to the new list, enforcing map bounds
                new_trails += [pos + d for d in DIRECTIONS if not any((pos + d)//bounds) \
                               and lines[tuple(pos + d)] == i]
        
            trails = new_trails.copy()

        # Find the number of unique 9-height positions reached on the final step
        trailheads[th] = len(set(tuple(t) for t in trails))

    # Sum scores of every trailhead
    total_score = sum(trailheads.values())

    return total_score

def Day10_Part2(input_file: str='Inputs/Day10_Inputs.txt') -> int:
    """
    Finds the sum of the ratings  of all trailheads on a topographic map given in an input file,
    where a hiking trail is any path that starts at height 0, ends at height 9, and always
    increases by a height of exactly 1 at each step. Hiking trails never include diagonal steps -
    only up, down, left, or right (from the perspective of the map). A trailhead is any position
    that starts one or more hiking trails - here, these positions will always have height 0. The
    rating of a trailhead is the number of distinct hiking trails which begin at that trailhead.

    Parameters
    ----------
    input_file : str, optional
        Input file giving the topographic map.
        The default is 'Inputs/Day10_Inputs.txt'.

    Returns
    -------
    total_rating : int
        The sum of the ratings of all trailheads on the map.

    """
    # Parse input file to extract map layout, the position of each trailhead and the map bounds
    lines, trailheads, bounds = get_input(input_file)

    # Loop through trailheads
    for th in trailheads:
        # Track positions reached on this step
        trails = [np.array(th)]
        # Loop from the next step being height 1 up to 9
        for i in range(1, 10):
            # Track valid next steps
            new_trails = []
            # For each trail being tracked
            for pos in trails:
                # Add each valid next step (height == i) to the new list, enforcing map bounds
                new_trails += [pos + d for d in DIRECTIONS if not any((pos + d)//bounds) \
                               and lines[tuple(pos + d)] == i]
        
            trails = new_trails.copy()

        # Find the number of total trails tracked after the final step
        trailheads[th] = len(trails)

    # Sum rating of every trailhead
    total_rating = sum(trailheads.values())

    return total_rating
