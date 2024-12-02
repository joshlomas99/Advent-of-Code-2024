import numpy as np

def get_input(input_file: str='Inputs/Day2_Inputs.txt') -> list:
    """
    Extracts a list of reports from an input file.

    Parameters
    ----------
    input_file : str, optional
        Input file containing the reports.
        The default is 'Inputs/Day1_Inputs.txt'.

    Returns
    -------
    reports : list(int)
        List of reports converted to integers.

    """
    # Extract lines from input file
    with open(input_file) as f:
        # Convert values to integers
        reports = [np.array([int(i) for i in l.strip().split()]) for l in f.readlines()]

    return reports

def passes(report: list) -> bool:
    """
    Returns whether a report passes the criteria for safety. A report only counts as safe if both:

    - The levels are either all increasing or all decreasing.
    - Any two adjacent levels differ by at least one and at most three.

    Parameters
    ----------
    report : list(int)
        Report to assess for safety.

    Returns
    -------
    status : bool
        Whether the report is safe.

    """
    # Calculate change between each level
    delta = report[1:] - report[:-1]
    # If all deltas are the same sign and are all between 1 and 3 in either direction, return True
    status = len(set(np.sign(delta))) == 1 and max(np.abs(delta)) <= 3 and min(np.abs(delta)) >= 1

    return status

def Day2_Part1(input_file: str='Inputs/Day2_Inputs.txt') -> int:
    """
    Determines the number of reports given in an input file which are safe. Each report consists of
    a series of levels. A report only counts as safe if both:

    - The levels are either all increasing or all decreasing.
    - Any two adjacent levels differ by at least one and at most three.

    Parameters
    ----------
    input_file : str, optional
        Input file containing the levels.
        The default is 'Inputs/Day2_Inputs.txt'.

    Returns
    -------
    safe : int
        The number of safe reports.

    """
    # Parse input file
    reports = get_input(input_file)
    # Count the number of reports passing the conditions
    safe = sum(passes(report) for report in reports)
    
    return safe

def Day2_Part2(input_file: str='Inputs/Day2_Inputs.txt') -> int:
    """
    Determines the number of reports given in an input file which are safe when at most one level
    is removed from the report. Each report consists of a series of levels. A report only counts as
    safe if both:

    - The levels are either all increasing or all decreasing.
    - Any two adjacent levels differ by at least one and at most three.

    Parameters
    ----------
    input_file : str, optional
        Input file containing the levels.
        The default is 'Inputs/Day2_Inputs.txt'.

    Returns
    -------
    safe_damped : int
        The number of safe reports with at most one level removed.

    """
    # Parse input file
    reports = get_input(input_file)
    # Count safe reports
    safe_damped = 0
    for report in reports:
        # Check if report already passes conditions
        if passes(report):
            safe_damped += 1
        else:
            # Else try removing each level in the report
            for i in range(len(report)):
                # Check in each case if the edited report passes the conditions
                if passes(np.delete(report, i)):
                    # If it passes, count and move on to the next report
                    safe_damped += 1
                    break
    
    return safe_damped
