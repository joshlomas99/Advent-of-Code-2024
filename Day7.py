def get_input(input_file: str='Inputs/Day7_Inputs.txt') -> dict:
    """
    Extract a series of test values and corresponding calibration equations from an input file.

    Parameters
    ----------
    input_file : str, optional
        Input file giving the values.
        The default is 'Inputs/Day7_Inputs.txt'.

    Returns
    -------
    equations : dict(int: tuple(int))
        Dictionary mapping the test values onto the corresponding calibration equations.

    """
    # Extract lines from input file
    with open(input_file) as f:
        lines = [l.strip().split() for l in f.readlines()]
        # Arrange into dictionary and convert values to integers
        equations = {int(l[0][:-1]): tuple(int(i) for i in l[1:]) for l in lines}

    return equations

from itertools import product

def ops_are_valid(nums: tuple, ops: tuple, answer: int) -> bool:
    """
    Checks if an expression formed of a given series of numbers, split by a given series of
    operators evaluates to the given answer.

    Parameters
    ----------
    nums : tuple(int)
        List of numbers.
    ops : tuple(int)
        List of operator representors, where 0 = '+', 1 = '*' and 2 = '||'.
    answer : int
        Answer to check.

    Raises
    ------
    Exception
        If an unrecognised operator is found.

    Returns
    -------
    are_valid : bool
        Whether the expression evaluates to the answer given.

    """
    # Start with the first number
    output = nums[0]
    for n, op in enumerate(ops):
        # If the answer was already exceeded, exit early, since all valid operations increase the
        # value
        if output > answer:
            return False
        # Apply addition
        if op == 0:
            output += nums[n+1]
        # Apply multiplication
        elif op == 1:
            output *= nums[n+1]
        # Apply concatenation
        elif op == 2:
            output = int(str(output) + str(nums[n+1]))
        else:
            raise Exception(f"Unrecognised operation {op}!")
    # Return whether the output matches the answer given
    return output == answer

def ops_are_valid_fast(nums: tuple, ops: tuple, answer: int) -> bool:
    """
    Checks if an expression formed of a given series of numbers, split by a given series of
    operators evaluates to the given answer.

    Parameters
    ----------
    nums : tuple(int)
        List of numbers.
    ops : tuple(int)
        List of operator representors, where 0 = '+', 1 = '*' and 2 = '||'.
    answer : int
        Answer to check.

    Raises
    ------
    Exception
        If an unrecognised operator is found.

    Returns
    -------
    are_valid : bool
        Whether the expression evaluates to the answer given.

    """
    # Start with the answer
    next_output = 1*answer
    # Move through the operations in reverse order
    for n, op in list(enumerate(ops))[::-1]:
        # For addition
        if op == 0:
            # Subtract the previous value from this point in the expression:
            # If the result is positive, accept the change and move on
            if next_output - nums[n+1] >= 0:
                next_output -= nums[n+1]
            # Else if it is below zero then this solution isn't valid, return False
            else:
                return False
        # For multiplication
        elif op == 1:
            # If the previous value from this point in the expression doesn't divide into the
            # current subtotal, then this solution isn't valid, return False
            if next_output % nums[n+1]:
                return False
            # Else, accept the change and move on
            else:
                next_output /= nums[n+1]
        # For concatenation
        elif op == 2:
            # If the current subtotal ends with the previous value from this point in the
            # expression, and removing it still leaves some characters
            if str(int(next_output)).endswith(str(nums[n+1])) and \
                (rev_con := str(int(next_output))[:-len(str(nums[n+1]))]):
                # Accept the change and move on
                next_output = int(rev_con)
            # Else this solution isn't valid, return False
            else:
                return False
        else:
            raise Exception(f"Unrecognised operation {op}!")
    # Return whether the value after reversing all operations matches the first value in the
    # expression
    return next_output == nums[0]

def Day7_Part1(input_file: str='Inputs/Day7_Inputs.txt') -> int:
    """
    Determines the total of the results of a series of equations, given in an input file, which are
    possible to be made true when some combination of '+' and '*' operations are applied.

    Parameters
    ----------
    input_file : str, optional
        Input file giving the equations.
        The default is 'Inputs/Day7_Inputs.txt'.

    Returns
    -------
    total : int
        Sum of the outputs of equations which can be made valid.

    """
    # Parse input file and extract equations
    equations = get_input(input_file)

    total = 0
    # Loop over expressions and required answers
    for answer, expression in equations.items():
        # For each possible combination of the two operators (where 0 = '+' and 1 = '*')
        for ops in product([0, 1], repeat=len(expression)-1):
            # Find if the current operators make the expression valid
            if ops_are_valid(expression, ops, answer):
                # If a valid solution is found, add the total and stop checking for this equation
                total += answer
                break
    
    return total

from tqdm import tqdm

def Day7_Part2(input_file: str='Inputs/Day7_Inputs.txt') -> int:
    """
    Determines the total of the results of a series of equations, given in an input file, which are
    possible to be made true when some combination of '+', '*' and '||' operations are applied.
    '||' represents conctenation, where the digits from the left and right inputs are combined into
    a single number, e.g. 12 || 345 would become 12345.

    Parameters
    ----------
    input_file : str, optional
        Input file giving the equations.
        The default is 'Inputs/Day7_Inputs.txt'.

    Returns
    -------
    total : int
        Sum of the outputs of equations which can be made valid.

    """
    # Parse input file and extract equations
    equations = get_input(input_file)

    new_total = 0
    # Loop over expressions and required answers
    for answer, expression in tqdm(equations.items()):
        # For each possible combination of the two operators (where 0 = '+', 1 = '*' and 2 == '||')
        for ops in product([0, 1, 2], repeat=len(expression)-1):
            # Find if the current operators make the expression valid
            if ops_are_valid_fast(expression, ops, answer):
                # If a valid solution is found, add the total and stop checking for this equation
                new_total += answer
                break

    return new_total
