import re

def get_input(input_file: str='Inputs/Day17_Inputs.txt') -> tuple:
    """
    Extract the initial values of three registers (A, B and C) and a program from an input file.

    Parameters
    ----------
    input_file : str, optional
        Input file containing the program.
        The default is 'Inputs/Day17_Inputs.txt'.

    Returns
    -------
    program : list(int)
        Program as a list of integers.
    a : int
        Initial value of register A.
    b : int
        Initial value of register B.
    c : int
        Initial value of register C.

    """
    # Extract lines from input file
    with open(input_file) as f:
        lines = [l.strip() for l in f.readlines()]

    # Extract values of reigsters and program and convert to integers
    a = int(re.findall('\d+', lines[0])[0])
    b = int(re.findall('\d+', lines[1])[0])
    c = int(re.findall('\d+', lines[2])[0])
    program = [int(i) for i in re.findall('\d+', lines[4])]

    return program, a, b, c

def run_program(program, a, b, c):
    """
    Runs a given program with the three registers (A, B and C) taking the given initial values.
    The computer knows eight instructions, each identified by a 3-bit number (called the
    instruction's opcode). Each instruction also reads the 3-bit number after it as an input; this
    is called its operand. A number called the instruction pointer identifies the position in the
    program from which the next opcode will be read; it starts at 0, pointing at the first 3-bit
    number in the program. Except for jump instructions, the instruction pointer increases by 2
    after each instruction is processed (to move past the instruction's opcode and its operand).
    If the computer tries to read an opcode past the end of the program, it instead halts.

    There are two types of operands; each instruction specifies the type of its operand. The value
    of a literal operand is the operand itself.
        - Combo operands 0 through 3 represent literal values 0 through 3.
        - Combo operand 4 represents the value of register A.
        - Combo operand 5 represents the value of register B.
        - Combo operand 6 represents the value of register C.
        - Combo operand 7 is reserved and will not appear in valid programs.
    The eight instructions are as follows:
        - The adv instruction (opcode 0) performs division. The numerator is the value in the A
          register. The denominator is found by raising 2 to the power of the instruction's combo
          operand. (So, an operand of 2 would divide A by 4 (2^2); an operand of 5 would divide
          A by 2^B.) The result of the division operation is truncated to an integer and then
          written to the A register.
        - The bxl instruction (opcode 1) calculates the bitwise XOR of register B and the
          instruction's literal operand, then stores the result in register B.
        - The bst instruction (opcode 2) calculates the value of its combo operand modulo 8
          (thereby keeping only its lowest 3 bits), then writes that value to the B register.
        - The jnz instruction (opcode 3) does nothing if the A register is 0. However, if the A
          register is not zero, it jumps by setting the instruction pointer to the value of its
          literal operand; if this instruction jumps, the instruction pointer is not increased by
          2 after this instruction.
        - The bxc instruction (opcode 4) calculates the bitwise XOR of register B and register C,
          then stores the result in register B. (For legacy reasons, this instruction reads an
          operand but ignores it.)
        - The out instruction (opcode 5) calculates the value of its combo operand modulo 8, then
          outputs that value. (If a program outputs multiple values, they are separated by commas.)
        - The bdv instruction (opcode 6) works exactly like the adv instruction except that the
          result is stored in the B register. (The numerator is still read from the A register.)
        - The cdv instruction (opcode 7) works exactly like the adv instruction except that the
          result is stored in the C register. (The numerator is still read from the A register.)

    Parameters
    ----------
    program : list(int)
        Program as a list of integers.
    a : int
        Initial value of register A.
    b : int
        Initial value of register B.
    c : int
        Initial value of register C.

    Returns
    -------
    output : str
        Comma-seperated output of the program as a string.

    """
    # Start at instruction 0
    i = 0
    # Track output
    out = []
    # Until the instruction pointer goes past the end of the program
    while i < len(program):
        # Extract operation and operand
        op = program[i]
        n = program[i+1]
        # Find corresponding combo operand
        if n in [0, 1, 2, 3, 7]:
            combo = n
        else:
            combo = [a, b, c][[4, 5, 6].index(n)]
        # Implement each operation
        # adv
        if op == 0:
            a = a >> combo
        # bxl
        elif op == 1:
            b = b^n
        # bst
        elif op == 2:
            b = combo%8
        #jnz
        elif op == 3 and a > 0:
            i = n
            continue
        # bxc
        elif op == 4:
            b = b^c
        # out
        elif op == 5:
            out.append(combo%8)
        # bdv
        elif op == 6:
            b = a >> combo
        # cdv
        elif op == 7:
            c = a >> combo

        # Increment instruction pointer
        i += 2

    # Join output with commas and convert to string
    output = ','.join(str(i) for i in out)

    return output

def Day17_Part1(input_file: str='Inputs/Day17_Inputs.txt') -> str:
    """
    Find the result if you use commas to join the values outputted by a program, given in an input
    file, into a single string. The program uses three reigsters whose initial values are given in
    the same input file.

    Parameters
    ----------
    input_file : str, optional
        Input file containing the program.
        The default is 'Inputs/Day17_Inputs.txt'.

    Returns
    -------
    output : str
        String output of program.

    """
    # Parse input file to extract program and initial register values
    program, a, b, c = get_input(input_file)
    # Run program and get output
    output = run_program(program, a, b, c)

    return output

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
        print(f'{func.__name__} ran in {t2:.7f} seconds')
        return out
    return wrapper

@time_function
def Day17_Part2(input_file: str='Inputs/Day17_Inputs.txt') -> int:
    """
    Find the lowest positive initial value for register A that causes a program, given in an input
    file, to output a copy of itself. The program uses three reigsters whose initial values are
    given in the same input file, although A is ignored in this case.

    Parameters
    ----------
    input_file : str, optional
        Input file containing the program.
        The default is 'Inputs/Day17_Inputs.txt'.

    Returns
    -------
    lowest_a_for_copy : int
        The lowest value of A which causes the program to output a copy of itself.

    """
    # Parse input file to extract program and initial register values
    program, a, b, c = get_input(input_file)

    # The program loops in a systematic way and uses a few key operands which appear after bxl
    # instructions (1), so extract these values
    i = 0
    bx1, bx2 = None, None
    while i < len(program):
        if program[i] == 1:
            if bx1 == None:
                bx1 = program[i+1]
            else:
                bx2 = program[i+1]
        i += 2

    # Keep track of the options for a which reproduce the program up to the current point
    # Track A as a dict mapping the position and value of each bit in its binary representation
    possible_a = [dict()]
    # Loop over each value of the program, as each loop over the program produces a single output
    for num_loops, p in enumerate(program):
        # Track new options for the next point in the program
        new_possible_a = []
        # For each current possibility from A
        for poss_a in possible_a:
            # Each loop, the final three bits of the binary version of the current value of A are
            # extracted and set to B, so loop through the possibilities for this
            for b in range(8):
                a = poss_a.copy()
                invalid = False
                b_bin = format(b, '03b')
                # Insert these three values into the dictionary tracking A
                for n, char in enumerate(b_bin[::-1]):
                    # If this value for B doesn't fit with this options for A, flag as invalid
                    if n+(3*num_loops) in a and a[n+(3*num_loops)] != char:
                        invalid = True
                        break
                    # Else insert this value into the A dictionary
                    else:
                        a[n+(3*num_loops)] = char
                # If the value is invalid, move on
                if invalid:
                    continue
                # The value for C must equal B XOR BX1 XOR BX2 XOR P where p is the desired value
                # for the next place in the program
                c_bin = format(b^bx1^bx2^p, '03b')
                # Insert these three values into the dictionary tracking A, where the lowest bit
                # is positioned at A (B XOR BX1) positions before the lowest bit in B, which is
                # the end of A at this point in the loop, which is the initial length of A minus
                # 3 times the number of loops, since A loses its last 3 bits every loop
                for n, char in enumerate(c_bin[::-1]):
                    # If this value for C doesn't fit with this options for A, flag as invalid
                    if n+(3*num_loops)+(b^bx1) in a and a[n+(3*num_loops)+(b^bx1)] != char:
                        invalid = True
                        break
                    # Else insert this value into the A dictionary
                    else:
                        a[n+(3*num_loops)+(b^bx1)] = char
    
                # If the value is not invalid, add to list of possibilities
                if not invalid:
                    new_possible_a.append(a)

        possible_a = new_possible_a.copy()

    all_a = []
    # Loop over remaining possibilities for A
    for a in possible_a:
        out = ''
        # Loop over each bit
        for n in range(max(a.keys())+1)[::-1]:
            # Where the bit at this position appears in the dict, add the value here
            if n in a:
                out += str(a[n])
            # Else insert a 0 since we want the lowest value
            else:
                out += '0'
        # If this value of A does reproduce the program, add to list (some valid possibilties at
        # this point are too large (>8^16) and have extra values after the required output
        if run_program(program, int(out, base=2), b, c) == ','.join(str(i) for i in program):
            all_a.append(int(out, base=2))

    # Find minimum valid value for A
    lowest_a_for_copy = min(all_a)

    assert run_program(program, lowest_a_for_copy, b, c) == ','.join(str(i) for i in program)

    return lowest_a_for_copy

def test_inputs(bx1, bx2, n, order):
    """
    Test if a program corresponding to the given parameters can be made to reproduce itself
    if the register A takes a certain value. The program takes the form 

        ``[2, 4, 1, bx1, 7, 5, 1, bx2, 0, 3, 4, n, 5, 5, 3, 0]``

    where the three sections ``(1, bx2)``, ``(0, 3)``, ``(4, n)`` can be in any order, determined
    by the ``order`` parameter.

    Parameters
    ----------
    bx1 : int
        Operand for first B XOR instruction.
    bx2 : int
        Operand for second B XOR instruction.
    n : int
        Operand for bxc (4) instruction.
    order : int
        Order for three free positioned instructions.

    Returns
    -------
    program : list(int)
        Program corresponding to the input parameters.
    lowest_a_for_copy : int
        The lowest value of A which causes the program to output a copy of itself.
    total_num_sol : int
        The number of possible values for A which causes the program to output a copy of itself.

    """
    # Set parameters, including order of the free positioned instructions
    if order == 0:
        program = [2, 4, 1, bx1, 7, 5, 1, bx2, 0, 3, 4, n, 5, 5, 3, 0]
    if order == 1:
        program = [2, 4, 1, bx1, 7, 5, 1, bx2, 4, n, 0, 3, 5, 5, 3, 0]
    if order == 2:
        program = [2, 4, 1, bx1, 7, 5, 0, 3, 1, bx2, 4, n, 5, 5, 3, 0]
    if order == 3:
        program = [2, 4, 1, bx1, 7, 5, 0, 3, 4, n, 1, bx2, 5, 5, 3, 0]
    if order == 4:
        program = [2, 4, 1, bx1, 7, 5, 4, n, 1, bx2, 0, 3, 5, 5, 3, 0]
    if order == 5:
        program = [2, 4, 1, bx1, 7, 5, 4, n, 0, 3, 1, bx2, 5, 5, 3, 0]

    # Run algorithm to find every value of A which causes the program to reproduce itself
    possible_a = [dict()]
    for num_loops, p in enumerate(program):
        new_possible_a = []
        for poss_a in possible_a:
            for b in range(8):
                a = poss_a.copy()
                invalid = False
                b_bin = format(b, '03b')
                for n, char in enumerate(b_bin[::-1]):
                    if n+(3*num_loops) in a and a[n+(3*num_loops)] != char:
                        invalid = True
                        break
                    else:
                        a[n+(3*num_loops)] = char
                if invalid:
                    continue
                c_bin = format(b^bx1^bx2^p, '03b')
                for n, char in enumerate(c_bin[::-1]):
                    if n+(3*num_loops)+(b^bx1) in a and a[n+(3*num_loops)+(b^bx1)] != char:
                        invalid = True
                        break
                    else:
                        a[n+(3*num_loops)+(b^bx1)] = char
    
                if not invalid:
                    new_possible_a.append(a)
    
        possible_a = new_possible_a.copy()

    all_a = []
    total_num_sol = 0
    for a in possible_a:
        out, num_sol = '', 1
        for n in range(max(a.keys())+1)[::-1]:
            if n in a:
                out += str(a[n])
            else:
                out += '0'
                num_sol *= 2
        if run_program(program, int(out, base=2), 0, 0) == ','.join(str(i) for i in program):
            all_a.append(int(out, base=2))
            total_num_sol += num_sol

    # If there are no valid solutions for this program, return None
    if not all_a:
        return None
    lowest_a_for_copy = min(all_a)

    return program, lowest_a_for_copy, total_num_sol

from tqdm import tqdm

@time_function
def find_all_programs():
    """
    Find all the possible programs for this problem which have possible values for register A
    which cause the program to output itself.

    Returns
    -------
    all_programs : list(tuple(list(int), int, int))
        List of all valid programs, which for each program gives: the program, the lowest value of
        A which causes the program to output itself and the number of valid values for A.

    """
    # Loop over all values of every parameter and store the properties of each valid one
    all_programs = []
    for bx1 in tqdm(range(8)):
        for bx2 in range(8):
            for n in range(8):
                for order in range(6):
                    sol = test_inputs(bx1, bx2, n, order)
                    if sol:
                        all_programs.append(sol)

    all_programs = sorted(all_programs, key=lambda p: p[0])

    return all_programs 
