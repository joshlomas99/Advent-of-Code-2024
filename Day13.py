import re

def get_input(input_file: str='Inputs/Day13_Inputs.txt') -> list:
    """
    Extract the properties of a series of claw machines from an input file. Each machine has two
    buttons labelled A and B. The buttons are configured to move the claw a specific amount to the
    right (along the X axis) and a specific amount forward (along the Y axis) each time that button
    is pressed. Each machine contains one prize. The input file gives the X and Y shifts for button
    A, then button B and then the X,Y position of the prize for each machine, with each machine
    separated by a newline.

    Parameters
    ----------
    input_file : str, optional
        Input file giving the machine properties.
        The default is 'Inputs/Day13_Inputs.txt'.

    Returns
    -------
    machines : list(list(tuple(int, int)))
        List of machine properties, in the form [(ax, ay), (bx, by), (px, py)].

    """
    # Extract lines from input file
    with open(input_file) as f:
        lines = [l.strip() for l in f.readlines()]

    # Initialise list of machines
    machines =  [[]]
    for l in lines:
        # For each newline, add a new machine to the end of the list
        if not l:
            machines.append([])
        # Else extract the digits from the next line, convert to int and add to the latest machine
        else:
            machines[-1].append(tuple(int(i) for i in re.findall('\d+', l)))

    return machines

def Day13_Part1(input_file: str='Inputs/Day13_Inputs.txt') -> int:
    """
    Determines the fewest tokens required to win all possible prizes in a series of claw machines
    whose properties are given in an input file. Each machine has two buttons labelled A and B. The
    buttons are configured to move the claw a specific amount to the right (along the X axis) and a
    specific amount forward (along the Y axis) each time that button is pressed. Each machine
    contains one prize; to win the prize, the claw must be positioned exactly above the prize on
    both the X and Y axes. It costs 3 tokens to push the A button and 1 token to push the B button.

    Parameters
    ----------
    input_file : str, optional
        Input file giving the machine properties.
        The default is 'Inputs/Day13_Inputs.txt'.

    Returns
    -------
    cost : int
        Total cost in tokens to win every prize possibly for the fewest tokens total.

    """
    # Parse input file to extract machine properties
    machines = get_input(input_file)
    # Track total cost
    cost = 0
    # Loop over machine properties
    for (ax, ay), (bx, by), (px, py) in machines:
        # Solve set of simultaneous equatuions defined by machine properties to find only valid
        # solution for n_a and n_b, and round to the nearest integer (to handle floating point
        # errors)
        n_a = round((py - ((by*px)/bx))/(ay-((ax*by)/bx)))
        n_b = round((px - (ax*n_a))/bx)
        # If both n values are positive and they give the correct exact result (i.e. both values
        # evaluated to exact integers minus floating point errors)
        if n_a >= 0 and n_b >= 0 and ax*n_a + bx*n_b == px and ay*n_a + by*n_b == py:
            # Then add the corresponding cost in tokens to the total
            cost += int((3*n_a) + n_b)
    
    return cost

def Day13_Part2(input_file: str='Inputs/Day13_Inputs.txt') -> int:
    """
    Determines the fewest tokens required to win all possible prizes in a series of claw machines
    whose properties are given in an input file. Each machine has two buttons labelled A and B. The
    buttons are configured to move the claw a specific amount to the right (along the X axis) and a
    specific amount forward (along the Y axis) each time that button is pressed. Each machine
    contains one prize; to win the prize, the claw must be positioned exactly above the prize on
    both the X and Y axes. It costs 3 tokens to push the A button and 1 token to push the B button.
    However, due to a unit conversion error in your measurements, the position of every prize is
    now actually 10000000000000 higher on both the X and Y axis than is given in the input file.

    Parameters
    ----------
    input_file : str, optional
        Input file giving the machine properties.
        The default is 'Inputs/Day13_Inputs.txt'.

    Returns
    -------
    cost : int
        Total cost in tokens to win every prize possibly for the fewest tokens total.

    """
    # Parse input file to extract machine properties
    machines = get_input(input_file)
    # Track total cost
    cost = 0
    for (ax, ay), (bx, by), (px, py) in machines:
        # Solve set of simultaneous equatuions defined by machine properties to find only valid
        # solution for n_a and n_b, and round to the nearest integer (to handle floating point
        # errors) - with prize positions shifted by 1e13 in both axis
        n_a = round(((py+1e13) - ((by*(px+1e13))/bx))/(ay-((ax*by)/bx)))
        n_b = round(((px+1e13) - (ax*n_a))/bx)
        # If both n values are positive and they give the correct exact result (i.e. both values
        # evaluated to exact integers minus floating point errors)
        if n_a >= 0 and n_b >= 0 and ax*n_a + bx*n_b == px + 1e13 and ay*n_a + by*n_b == py + 1e13:
            # Then add the corresponding cost in tokens to the total
            cost += int((3*n_a) + n_b)
    
    return cost
