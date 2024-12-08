import numpy as np

def get_input(input_file: str='Inputs/Day8_Inputs.txt') -> tuple:
    """
    Extracts the frequencies and positions of a series of antennae from a map given in an input
    file.

    Parameters
    ----------
    input_file : str, optional
        Input file giving the map.
        The default is 'Inputs/Day8_Inputs.txt'.

    Returns
    -------
    antennas : dict(str: list(np.1darray(int)))
        Dictionary giving the coordinates of all antennae of each occuring frequency.
    boudns: tuple(int)
        The bounds of the input map in the form (length, width).

    """

    # Extract lines from input file
    with open(input_file) as f:
        lines = [l.strip() for l in f.readlines()]
    # Extract bounds
    bounds = len(lines), len(lines[0])

    antennas = dict()
    # Loop through map
    for r in range(bounds[0]):
        for c in range(bounds[1]):
            # Wherever an antenna is found
            if (char := lines[r][c]) != '.':
                # Add coordinates to the corresponding entry in the dictionary
                if char in antennas:
                    antennas[char].append(np.array((r, c)))
                else:
                    antennas[char] = [np.array((r, c))]

    return antennas, bounds

from itertools import combinations

def Day8_Part1(input_file: str='Inputs/Day8_Inputs.txt') -> int:
    """
    Determines the number of unique locations within the bounds of a map, given in an input file,
    which contain an antinode. The map gives the positions and frequencies of a set of antennae,
    where empty space is represented by '.' and any other character represents an anntena with a 
    resonant frequency corresponding to its character. An antinode occurs at any point that is
    perfectly in line with two antennae of the same frequency - but only when one of the antennae
    is twice as far away as the other.

    Parameters
    ----------
    input_file : str, optional
        Input file giving the antenna positions and frequencies.
        The default is 'Inputs/Day8_Inputs.txt'.

    Returns
    -------
    num_nodes : int
        The number of unique antinode locations within the map.

    """
    # Parse the input file and extract antennae frequencies and positions, and map bounds
    antennas, bounds = get_input(input_file)
    # Track each unique node position with a set
    nodes = set()
    # Loop over each antenna frequency
    for f, coords in antennas.items():
        # For each combination of two antennae of the current frequency
        for a, b in combinations(coords, 2):
            # Find the translation vector between the two
            diff = a - b
            # Apply this vector in either direction of the pair, and add positions to set
            nodes.add(tuple(a + diff))
            nodes.add(tuple(b - diff))

    # Remove node positions which are outside the bounds of the map
    nodes_within_bounds = {(r, c) for r, c in nodes  if 0 <= r < bounds[0] and 0 <= c < bounds[1]}

    # Find number of unique positions
    num_nodes = len(nodes_within_bounds)
    
    return num_nodes

def Day8_Part2(input_file: str='Inputs/Day8_Inputs.txt') -> int:
    """
    Determines the number of unique locations within the bounds of a map, given in an input file,
    which contain an antinode. The map gives the positions and frequencies of a set of antennae,
    where empty space is represented by '.' and any other character represents an anntena with a 
    resonant frequency corresponding to its character. An antinode occurs at any grid position
    exactly in line with at least two antennas of the same frequency, regardless of distance.

    Parameters
    ----------
    input_file : str, optional
        Input file giving the antenna positions and frequencies.
        The default is 'Inputs/Day8_Inputs.txt'.

    Returns
    -------
    num_nodes : int
        The number of unique antinode locations within the map.

    """
    # Parse the input file and extract antennae frequencies and positions, and map bounds
    antennas, bounds = get_input(input_file)
    # Track each unique node position with a set
    nodes = set()
    # Loop over each antenna frequency
    for f, coords in antennas.items():
        # For each combination of two antennae of the current frequency
        for a, b in combinations(coords, 2):
            # Find the translation vector between the two
            diff = a - b
            # From the position of one of the antennae
            test = a.copy()
            # Add its position to the set
            nodes.add(tuple(test))
            # Then move once from that antenna following the vector
            test += diff
            # If the new position is within the map bounds
            while 0 <= test[0] < bounds[0] and 0 <= test[1] < bounds[1]:
                # Add the new position to the set
                nodes.add(tuple(test))
                # Continue moving away until we reach the edge of the map
                test += diff
            # Reset to the antenna position
            test = a.copy()
            # Move in the other direction from the antenna
            test -= diff
            # If the new position is within the map bounds
            while 0 <= test[0] < bounds[0] and 0 <= test[1] < bounds[1]:
                # Add the new position to the set
                nodes.add(tuple(test))
                # Continue moving away until we reach the edge of the map
                test -= diff

    # Find number of unique positions
    num_nodes = len(nodes)

    return num_nodes
