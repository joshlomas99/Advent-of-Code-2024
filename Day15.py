def get_input(input_file: str='Inputs/Day15_Inputs.txt', widen: bool=False) -> tuple:
    """
    Extract a map of a set of boxes, walls and a robot, along with a series of instructions for the
    robot, given in an input file.

    Parameters
    ----------
    input_file : str, optional
        Input file giving the map and instructions.
        The default is 'Inputs/Day15_Inputs.txt'.
    widen : bool, optional
        Whether to widen the map by a factor of 2.
        The default is False.

    Returns
    -------
    robot : tuple(int)
        Initial position of the robot.
    boxes : set(tuple(int))
        Set of initial box positions.
    walls : set(tuple(int))
        Set of wall positions.
    moves : str
        Series of characters describing the robot instructions.

    """
    # Extract lines from input file
    with open(input_file) as f:
        lines = [l.strip() for l in f.readlines()]

    robot, boxes, walls, moves, reading_moves = (-1, -1), set(), set(), '', False
    # Loop through input file and collect coordinates
    for r, l in enumerate(lines):
        if not l:
            # After newline, start collecting movement instructions
            reading_moves = True
        elif not reading_moves:
            if widen:
                l = l.replace('#', '##').replace('O', '[]').replace('.', '..').replace('@', '@.')
            for c, t in enumerate(l):
                if t == '#':
                    walls.add((r, c))
                elif t == 'O':
                    boxes.add((r, c))
                elif t == '[':
                    boxes.add(((r, c), (r, c+1)))
                elif t == ']':
                    continue
                elif t == '@':
                    robot = (r, c)
        else:
            moves += l

    return robot, boxes, walls, moves

# Map of instruction symbols to the corresponding shift of robot position
MOVES = {'v': (1, 0), '>': (0, 1), '^': (-1, 0), '<': (0, -1)}

def Day15_Part1(input_file: str='Inputs/Day15_Inputs.txt') -> int:
    """
    Find the sum of GPS coordinates of a set of boxes laid out in a room after a series of 
    instructions, given in an input file, are followed by a robot. As the robot (@) attempts to
    move, if there are any boxes (O) in the way, the robot will also attempt to push those boxes.
    However, if this action would cause the robot or a box to move into a wall (#), nothing moves
    instead, including the robot. The initial positions of these are shown on the map at the top of
    the input file. The rest of the document describes the moves (^ for up, v for down, < for left,
    > for right) that the robot will attempt to make, in order. The GPS coordinate of a box is
    equal to 100 times its distance from the top edge of the map plus its distance from the left
    edge of the map (including wall tiles).

    Parameters
    ----------
    input_file : str, optional
        Input file giving the map and instructions.
        The default is 'Inputs/Day15_Inputs.txt'.

    Returns
    -------
    total_gps : int
        The sum of all boxes' GPS coordinates after the robot has finished moving.

    """
    # Parse input file to extract initial robot and box positions, wall positions and moves
    robot, boxes, walls, moves = get_input(input_file)

    # Loop over moves
    for m in moves:
        # Find next position
        next_pos = (robot[0]+MOVES[m][0], robot[1]+MOVES[m][1])
        # If we hit a wall, don't move
        if next_pos in walls:
            continue
        # Else if we hit a box
        elif next_pos in boxes:
            # Count moving boxes
            num_boxes = 1
            # While we keep finding boxes in this direction, keep adding them
            while (last_pos := (next_pos[0] + (num_boxes*MOVES[m][0]),
                                next_pos[1] + (num_boxes*MOVES[m][1]))) in boxes:
                num_boxes += 1
            # If we hit a wall, don't move
            if last_pos in walls:
                continue
            # Else move robot and all boxes counted
            else:
                robot = next_pos
                boxes.discard(next_pos)
                boxes.add(last_pos)
        # Else just move the robot
        else:
            robot = next_pos

    # Calculate sum of GPS coordinates
    total_gps = sum((100*x)+y for x, y in boxes)
    
    return total_gps

def other(this: tuple, left: list, right: list) -> tuple:
    """
    Find the coordinates of the other half of a wide box, given the coordinates of one half.

    Parameters
    ----------
    this : tuple(int)
        Coordinates of the given half of the wide box.
    left : list(tuple(int))
        Ordered list of the coordinates of the left halves of boxes.
    right : list(tuple(int))
        Ordered list of the coordinates of the right halves of boxes.

    Returns
    -------
    other : tuple(int)
        Coordinates of the other half of the wide box.

    """
    # Find this coordinate in either list, and return the corrsponding index of the other
    if this in left:
        return right[left.index(this)]
    elif this in right:
        return left[right.index(this)]

def Day15_Part2(input_file: str='Inputs/Day15_Inputs.txt') -> int:
    """
    Find the sum of GPS coordinates of a set of boxes laid out in a room after a series of 
    instructions, given in an input file, are followed by a robot. As the robot (@) attempts to
    move, if there are any boxes (O) in the way, the robot will also attempt to push those boxes.
    However, if this action would cause the robot or a box to move into a wall (#), nothing moves
    instead, including the robot. The initial positions of these are shown on the map at the top of
    the input file. The rest of the document describes the moves (^ for up, v for down, < for left,
    > for right) that the robot will attempt to make, in order. The GPS coordinate of a box is
    equal to 100 times its distance from the top edge of the map plus its distance from the left
    edge of the map (including wall tiles). However, now every object on the initial map is twice
    as wide, so for each tile the following change is made:
        - If the tile is #, the new map contains ## instead.
        - If the tile is O, the new map contains [] instead.
        - If the tile is ., the new map contains .. instead.
        - If the tile is @, the new map contains @. instead.

    The two halves of wide boxes ([]) always move together, even if only one half is contacted.

    Parameters
    ----------
    input_file : str, optional
        Input file giving the map and instructions.
        The default is 'Inputs/Day15_Inputs.txt'.

    Returns
    -------
    total_gps : int
        The sum of all boxes' GPS coordinates after the robot has finished moving.

    """
    # Parse input file to extract initial robot and box positions, wall positions and moves, with
    # new widening also performed
    robot, boxes, walls, moves = get_input(input_file, True)

    # Store coordinates of left and right halves of boxes at the same point in corresponding lists
    left, right = [b[0] for b in boxes], [b[1] for b in boxes]
    
    # Loop over moves
    for m in moves:
        # Find next position
        next_pos = (robot[0]+MOVES[m][0], robot[1]+MOVES[m][1])
        # If we hit a wall, don't move
        if next_pos in walls:
            continue
        # Else if we hit a box
        elif next_pos in left or next_pos in right:
            # Start list of boxes which move, adding both halves of this box
            moving_boxes = {next_pos, other(next_pos, left, right)}
            # Track if we hit a wall
            hit_wall = False
            # Track the last set of boxes considered
            last_layer = {next_pos, other(next_pos, left, right)}
            # While there are boxes to consider
            while last_layer:
                # Track boxes ahead of the ones currently being pushed
                next_layer = set()
                # Loop over the last layer of pushed boxes
                for bx, by in last_layer:
                    # If there is a wall ahead of any boxes, record and break so we can not move
                    if (next_test := (bx + MOVES[m][0], by + MOVES[m][1])) in walls:
                        hit_wall = True
                        break
                    # Else if we're checking the other half of the current box, ignore
                    elif next_test == other((bx, by), left, right):
                        continue
                    # Else if the next position also contains a box half, add both halves of that
                    # box to the next layer to check
                    elif next_test in left or next_test in right:
                        next_layer.add(next_test)
                        next_layer.add(other(next_test, left, right))
                # If we hit a wall, stop checking
                if hit_wall:
                    break
                # Else add all new boxes to the set of moving boxes and update the last layer
                moving_boxes.update(next_layer)
                last_layer = next_layer.copy()
            # If we hit a wall, don't move
            if hit_wall:
                continue
            else:
                # Else loop over all moving boxes in set and perform the movement, tracking
                # boxes which already moved. We need to move both halves of each box at the same
                # time so they stay at the same index of the "left" and "right" lists as each other
                moved_left = []
                moved_right = []
                for box in moving_boxes:
                    # Find the other half of this box
                    other_box = other(box, left, right)
                    # Move both box halves
                    if box in left:
                        left.remove(box)
                        moved_left.append((box[0]+MOVES[m][0], box[1]+MOVES[m][1]))
                        right.remove(other_box)
                        moved_right.append((other_box[0]+MOVES[m][0], other_box[1]+MOVES[m][1]))
                    elif box in right:
                        right.remove(box)
                        moved_right.append((box[0]+MOVES[m][0], box[1]+MOVES[m][1]))
                        left.remove(other_box)
                        moved_left.append((other_box[0]+MOVES[m][0], other_box[1]+MOVES[m][1]))

                # Move robot
                robot = next_pos
                # Add moved positions of boxes
                left += moved_left
                right += moved_right

        # Else just move the robot
        else:
            robot = next_pos

    # Calculate sum of GPS coordinates
    total_gps = sum((100*x)+y for x, y in left)
    
    return total_gps
    