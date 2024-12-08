def get_input(input_file: str='Inputs/Day5_Inputs.txt') -> tuple:
    """
    Extract a series of rules followed after a newline by a series of lists from an input file.

    Parameters
    ----------
    input_file : str, optional
        Input file containing the rules and lists.
        The default is 'Inputs/Day5_Inputs.txt'.

    Returns
    -------
    lists : list((list(int))
        List of lists converted to integers.

    rules : list(tuple(int))
        List of tuples of integers describing the rules.

    """
    # Extract lines from input file
    with open(input_file) as f:
        # Extract all lines
        lines = [l.strip() for l in f.readlines()]
        i = 0
        # Extract and convert rules before the first newline
        rules = []
        while lines[i]:
            rules.append(tuple(int(i) for i in lines[i].split('|')))
            i += 1
        i += 1
        # Extract and convert lists until the end of the file
        lists = []
        while i < len(lines):
            lists.append([int(i) for i in lines[i].split(',')])
            i += 1

    return lists, rules

def Day5_Part1(input_file: str='Inputs/Day5_Inputs.txt') -> int:
    """
    Calculates the total of all the middle numbers from a series of lists given in an input file,
    which are correctly ordered according to a series of rules also given in the input file. Rules
    take the form n|m, meaning that n must come before m in any list in which they both appear.

    Parameters
    ----------
    input_file : str, optional
        Input file giving the lists and rules.
        The default is 'Inputs/Day5_Inputs.txt'.

    Returns
    -------
    total : int
        Total of the middle numbers from all correctly ordered lists.

    """
    # Parse input file to extract lists and rules
    lists, rules = get_input(input_file)

    total = 0
    # Loop over all lists
    for l in lists:
        # Default that list is correct
        passed = True
        # Loop over all rules
        for r_l, r_h in rules:
            # If both numbers are in the list and the rule isn't followed, record the fail and stop
            # checking further rules
            if r_l in l and r_h in l and l.index(r_l) > l.index(r_h):
                passed = False
                break
        # If the list passed every rule, add its middle number to the total
        if passed:
            total += l[(len(l)-1)//2]
    
    return total

def Day5_Part2(input_file: str='Inputs/Day5_Inputs.txt') -> int:
    """
    Calculates the total of all the middle numbers from a series of lists given in an input file,
    which are initially incorrectly ordered, after they have been rearranged to the correct order,
    according to a series of rules also given in the input file. Rules take the form n|m, meaning
    that n must come before m in any list in which they both appear.

    Parameters
    ----------
    input_file : str, optional
        Input file giving the lists and rules.
        The default is 'Inputs/Day5_Inputs.txt'.

    Returns
    -------
    total : int
        Total of the middle numbers from initially incorrectly ordered lists, once they have been
        correctly arranged.

    """
    # Parse input file to extract lists and rules
    lists, rules = get_input(input_file)

    total_corr = 0
    # Loop over all lists
    for l in lists:
        # Default that list is correct
        passed = True
        # Loop over all rules
        for r_l, r_h in rules:
            # If both numbers are in the list and the rule isn't followed, record the fail and stop
            # checking further rules
            if r_l in l and r_h in l and l.index(r_l) > l.index(r_h):
                passed = False
                break
        # If the list is not initially correctly ordered
        if not passed:
            # Find only the rules where both numbers are contained in this list
            sub_rules = [r for r in rules if r[0] in l and r[1] in l]
            # Extract the first number in each of the rules
            first = [s[0] for s in sub_rules]
            # For their to be a unique solution to the ordering of each list, the extracted rules
            # which apply must form a complete and consistent set, such that the ordering can be
            # found by checking how often each number comes first in a rule. The number which comes
            # first in every rule must be first overall, and so on...
            l = sorted(l, key=lambda n: first.count(n), reverse=True)
            # Once the list is correctly rearranged, add its middle number to the total
            total_corr += l[(len(l)-1)//2]
    
    return total_corr
