def get_input(input_file: str='Inputs/Day1_Inputs.txt') -> list:
    """
    Extracts the lines of a document given in an input file containing two list of integers side by
    side.

    Parameters
    ----------
    input_file : str, optional
        Input file containing the lists.
        The default is 'Inputs/Day1_Inputs.txt'.

    Returns
    -------
    list1 : list(int)
        Left sided list.

    list2 : list(int)
        Right sided list.

    """
    # Extract lines from input file
    with open(input_file) as f:
        lines = [l.strip().split() for l in f.readlines()]

    # Split up lists and convert to integers
    list1 = [int(l[0]) for l in lines]
    list2 = [int(l[1]) for l in lines]

    return list1, list2

def Day1_Part1(input_file: str='Inputs/Day1_Inputs.txt') -> int:
    """
    Pairs up the smallest numbers in a pair of lists given in an input file, then the second-
    smallest numbers, and so on. Then determines within each pair how far apart the two numbers are
    and find the total distance across the full lists.

    Parameters
    ----------
    input_file : str, optional
        Input file containing the lists.
        The default is 'Inputs/Day1_Inputs.txt'.

    Returns
    -------
    distance : int
        The total distance between the two lists.

    """
    # Parse input file
    list1, list2 = get_input(input_file)
    # Sort lists
    list1.sort()
    list2.sort()
    # Sum absolute differences between lists at each point
    distance = sum(abs(l2 - l1) for l1, l2 in zip(list1, list2))

    return distance

def Day1_Part2(input_file: str='Inputs/Day1_Inputs.txt') -> int:
    """
    Calculates the similarity score between a pair of lists given in an input file. This is found
    by multiplying each number in the left list by how often that number appears in the right list.
    This is then summed across the full lists.

    Parameters
    ----------
    input_file : str, optional
        Input file containing the lists.
        The default is 'Inputs/Day1_Inputs.txt'.

    Returns
    -------
    similarity_score : int
        The total similarity score between the two lists.

    """
    # Parse input file
    list1, list2 = get_input(input_file)
    # Sort lists
    list1.sort()
    list2.sort()
    # Sum similarity scores across the full lists
    similarity_score = sum(l*list2.count(l) for l in list1)

    return similarity_score
