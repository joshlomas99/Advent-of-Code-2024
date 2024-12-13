import numpy as np

# Directions to search for already discovered coordinates (up and back)
SEARCH = [(0, -1), (-1, 0)]
# All orthogonal directions
DIRECTIONS = [(0, -1), (-1, 0), (0, 1), (1, 0)]

def get_input(input_file: str='Inputs/Day12_Inputs.txt') -> tuple:
    """
    Extract a a map of all unique clusters of garden plots from an arrangement map given in an
    input file. Each garden plot grows only a single type of plant and is indicated by a single
    letter on the map. When multiple garden plots are growing the same type of plant and are
    touching (horizontally or vertically), they form a cluster.

    Parameters
    ----------
    input_file : str, optional
        Input file giving the garden plot arrangement.
        The default is 'Inputs/Day12_Inputs.txt'.

    Returns
    -------
    clusters : numpy.ndarray
        2D numpy array of garden clusters, with each cluster represented by a different integer.

    areas : dict(int: int)
        Dictionary mapping the id of each cluster in the ``clusters`` map to the area of that
        cluster.

    bounds: numpy.ndarray
        Array giving the boundaries of the garden plot in the form (height, width).

    """
    # Extract lines from input file
    with open(input_file) as f:
        # Split each line by character
        lines = [[c for c in l.strip()] for l in f.readlines()]

    # Find bounds of map
    bounds = np.array((len(lines), len(lines[0])))

    # Initalise map of clusters to all zero
    clusters = np.zeros(bounds, dtype=int)
    # Integer to assign to new clusters
    next_cluster = 2
    # Set first plant to cluster 1
    clusters[0, 0] = 1
    # Loop through garden
    for r in range(len(lines)):
        for c in range(len(lines[r])):
            # Search in the two directions to plants already searched
            for d in SEARCH:
                # If we are looking outside the garden bounds, skip
                if any(np.array((r+d[0], c+d[1]))//bounds):
                    continue
                # If we found a connected existing cluster with the same plant
                if lines[r+d[0]][c+d[1]] == lines[r][c]:
                    # If this cluster was already assigned an id
                    if clusters[r, c]:
                        # Reassign all plants with the current id of this plant to the id of the
                        # connected cluster
                        clusters[clusters == clusters[r, c]] = clusters[r+d[0], c+d[1]]
                    # Else set the id of this plant to the id of the connected cluster
                    else:
                        clusters[r, c] = clusters[r+d[0], c+d[1]]
                # If we didn't find a connected plant of the same type
                elif not clusters[r, c]:
                    # Start a new cluster
                    clusters[r, c] = next_cluster
                    # Increment id for new clusters
                    next_cluster += 1

    # Find areas of each cluster
    areas = {n: np.sum(clusters == n) for n in np.unique(clusters)}

    return clusters, areas, bounds

def Day12_Part1(input_file: str='Inputs/Day12_Inputs.txt') -> int:
    """
    Determines the total price required to fence all clusters of plants in a garden, whose
    arrangement is given in an input file. Each garden plot grows only a single type of plant and
    is indicated by a single letter on the map. When multiple garden plots are growing the same
    type of plant and are touching (horizontally or vertically), they form a cluster. The cost of
    fencing around a single cluster is found by multiplying that cluster's area by its perimeter.
    The area of a cluster is simply the number of garden plots the cluster contains. Each garden
    plot is a square and so has four sides. The perimeter of a cluster is the number of sides of
    garden plots in the cluster that do not touch another garden plot in the same cluster.

    Parameters
    ----------
    input_file : str, optional
        Input file giving the garden layout.
        The default is 'Inputs/Day12_Inputs.txt'.

    Returns
    -------
    price : int
        Total price of fencing every cluster in the garden.

    """
    # Parse input file to extract array of clusters, each representing by a unique id, a dict
    # giving the area of each cluster and the bounds of the garden
    clusters, areas, bounds = get_input(input_file)
    # Track total price
    price = 0
    # Loop through garden
    for r in range(len(clusters)):
        for c in range(len(clusters[r])):
            # Search in each direction from the current plant
            for d in DIRECTIONS:
                # If this is outside the bounds of the map, or if the plant at this point is
                # different to the current plant, then there is a fence in this position
                if any(np.array((r+d[0], c+d[1]))//bounds) or clusters[r, c] != clusters[r+d[0], c+d[1]]:
                    # So add the area of the current cluster to the total price (equivalent to
                    # multiplying area by perimeter)
                    price += areas[clusters[r, c]]

    return price

def num_corners(cluster: np.ndarray) -> int:
    """
    Determines the number of corners connected to the current point in a 3x3 map, for a fence 
    built around the cluster matching the centre point in the map.

    Parameters
    ----------
    cluster : numpy.ndarray
        2D numpy array giving the cluster id of points immediately around the centre point.

    Returns
    -------
    num: int
        Number of corners around this point.

    """
    # Count corners
    num = 0
    # Convert map to bools representing which points are part of the current cluster
    this_cluster = (cluster == cluster[1, 1])
    # Loop through orthogonal direction, such that n -> n+1 is a 90 degree rotation clockwise,
    # so between these two points is the current corner to be tested
    for n in range(len(DIRECTIONS)):
        # Find how many of the two orthogonal points around the current corner being tested are
        # part of this cluster
        num_orth = sum(this_cluster[DIRECTIONS[m][0]+1, DIRECTIONS[m][1]+1] for m in [n, (n+1)%4])
        # If neither point is part of this clusterm, this is a convex corner
        if num_orth == 0:
            num += 1
        # Else if both points are part of this cluster
        elif num_orth == 2:
            # If the next point diagonally past the corner being tested is in a different cluster,
            # this is concave corner
            if not this_cluster[DIRECTIONS[n][0]+DIRECTIONS[(n+1)%4][0]+1,
                                DIRECTIONS[n][1]+DIRECTIONS[(n+1)%4][1]+1]:
                num += 1

    return num

def Day12_Part2(input_file: str='Inputs/Day12_Inputs.txt') -> int:
    """
    Determines the total price required to fence all clusters of plants in a garden, whose
    arrangement is given in an input file. Each garden plot grows only a single type of plant and
    is indicated by a single letter on the map. When multiple garden plots are growing the same
    type of plant and are touching (horizontally or vertically), they form a cluster. However, now
    the discounted cost of fencing around a single cluster is found by multiplying that cluster's
    area by the number of sides each region has. Each straight section of fence counts as a side,
    regardless of how long it is. The area of a cluster is simply the number of garden plots the
    cluster contains.

    Parameters
    ----------
    input_file : str, optional
        Input file giving the garden layout.
        The default is 'Inputs/Day12_Inputs.txt'.

    Returns
    -------
    price : int
        Total discounted price of fencing every cluster in the garden.

    """
    # Parse input file to extract array of clusters, each representing by a unique id, a dict
    # giving the area of each cluster and the bounds of the garden
    clusters, areas, bounds = get_input(input_file)

    # Pad the map of clusters with a layer all zeros in each direction
    clusters = np.array([[0]*(len(clusters[0])+2)] + [[0] + list(r) + [0] for r in clusters] + [[0]*(len(clusters[0])+2)])

    # Track total price
    price = 0
    # Loop through garden
    for r in range(1, len(clusters)-1):
        for c in range(1, len(clusters[r])-1):
            # The number of sides of the perimeter of any 2D shape is equal to the number of
            # corners it has
            # Determine the number of corners at the current point, using the region of clusters
            # immediately around this point
            sides = num_corners(clusters[r-1:r+2, c-1:c+2])
            # Add the area of the current cluster multiplied by the number of new sides found to
            # the total price (equivalent to multiplying area by total number of sides)
            price += (sides*areas[clusters[r, c]])

    return price
