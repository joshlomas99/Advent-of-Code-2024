import re

def get_input(input_file: str='Inputs/Day3_Inputs.txt') -> list:
    """
    Extracts the contents of a computer's memory from an input file.

    Parameters
    ----------
    input_file : str, optional
        Input file containing the memory.
        The default is 'Inputs/Day1_Inputs.txt'.

    Returns
    -------
    memory : list(int)
        Extracted memory entries.

    """
    # Extract lines from input file
    with open(input_file) as f:
        memory = [l.strip() for l in f.readlines()]
    return memory

def Day3_Part1(input_file: str='Inputs/Day3_Inputs.txt') -> int:
    """
    Finds the sum of the results of all valid multiplication instructions in a computer's memory,
    given in an input file. A valid instruction takes the form "mul(a,b)" with the result being a*b.

    Parameters
    ----------
    input_file : str, optional
        Input file giving the computer's memory.
        The default is 'Inputs/Day3_Inputs.txt'.

    Returns
    -------
    total : int
        Sum of all multiplication instruction results.

    """
    # Parse input file
    memory = get_input(input_file)
    # Extract all instructions of the correct form
    muls = [re.findall('mul\(\d+,\d+\)', l) for l in memory]
    # Determine sum of the results of all extracted instructions
    total = sum(sum(int(m[4:-1].split(',')[0])*int(m[4:-1].split(',')[1]) for m in mul) for mul in muls)
    
    return total

def Day3_Part2(input_file: str='Inputs/Day3_Inputs.txt') -> int:
    """
    Finds the sum of the results of all valid multiplication instructions in a computer's memory,
    given in an input file. A valid instruction takes the form "mul(a,b)" with the result being a*b.
    However, results are only added if the mul instructions are enabled. At the beginning of the
    program, mul instructions are enabled and this state can be changed by two condition statements
    also in the program:
        - The do() instruction enables future mul instructions.
        - The don't() instruction disables future mul instructions.

    Parameters
    ----------
    input_file : str, optional
        Input file giving the computer's memory.
        The default is 'Inputs/Day3_Inputs.txt'.

    Returns
    -------
    total : int
        Sum of all enabled multiplication instruction results.

    """
    # Parse input file
    memory = get_input(input_file)
    # Extract all instructions of the correct form, including condition statements
    muls_with_cond = [re.findall('mul\(\d+,\d+\)|do\(\)|don\'t\(\)', l) for l in memory]
    # Instructions start as enabled
    enabled = True
    total = 0
    for mul in muls_with_cond:
        for m in mul:
            # If enabled, add multiplication instruction results
            if m.startswith('mul') and enabled:
                total += int(m[4:-1].split(',')[0])*int(m[4:-1].split(',')[1])
            # For conditional statements, switch the enabled flag on and off accordingly
            elif m == 'do()':
                enabled = True
            elif m == 'don\'t()':
                enabled = False
    
    return total
