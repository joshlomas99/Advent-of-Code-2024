def get_input(input_file: str='Inputs/Day9_Inputs.txt') -> str:
    """
    Extracts a disk map from an input file. The disk map uses a dense format to represent the
    layout of files and free space on the disk. The digits alternate between indicating the length
    of a file and the length of free space.

    Parameters
    ----------
    input_file : str, optional
        Input file giving the disk map.
        The default is 'Inputs/Day9_Inputs.txt'.

    Returns
    -------
    files : str
        Extracted disk map as a string.

    """
    # Extract lines from input file
    with open(input_file) as f:
        files = f.readlines()[0].strip()

    # If it ends with free space, disgard this so it is always odd in length
    if not len(files)%2:
        files = files[:-1]

    return files

def Day9_Part1(input_file: str='Inputs/Day9_Inputs.txt') -> int:
    """
    Calculates the checksum of a filesystem whose disk map is given in an input file, after it has
    undergone a compacting procedure. The disk map uses a dense format to represent the layout of 
    files and free space on the disk. The digits alternate between indicating the length of a file
    and the length of free space. Each file on disk also has an ID number based on the order of the
    files as they appear before they are rearranged, starting with ID 0. The compacting procedure
    moves file blocks one at a time from the end of the disk to the leftmost free space block,
    until there are no gaps remaining between file blocks. The checksum is the sum of the result of
    multiplying each of these blocks' position with the file ID number it contains. The leftmost
    block is in position 0. If a block contains free space, skip it instead.

    Parameters
    ----------
    input_file : str, optional
        Input file giving the disk map.
        The default is 'Inputs/Day9_Inputs.txt'.

    Returns
    -------
    checksum : int
        Checksum of the compacted filesystem.

    """
    # Parse input file to extract disk map
    files = get_input(input_file)

    # Move through the filesystem and whenever a free space is reached, move the next file
    # from the end of the disk map to this spot
    # Track position in filesystem and checksum
    pos = 0
    checksum = 0
    # Track position reached from the end of the filesystem, by file (n) and file block (i)
    end_n = len(files)-1
    end_i = int(files[end_n])
    # Track when we meet in the middle of the filesystem and should stop
    done = False
    # Loop through diskmap
    for n, f in enumerate(files):
        # If even, this is a file 
        if not n%2:
            # Loop over the length of the file 
            for i in range(int(f)):
                # Add the checksum of the current file block from this point in the filesystem to
                # the total and increment position
                checksum += (pos * n//2)
                pos += 1
                # If the progress from the start of the filesystem meets the progress from the end,
                # we have covered everything and should stop
                if end_n <= n and end_i - 1 <= i:
                    done = True
                    break
        # Else, this is free space
        else:
            # Loop over the length of the free space
            for i in range(int(f)):
                # Add the checksum of the current file from the end of the filesystem to the total
                # and increment position
                checksum += (pos * end_n//2)
                end_i -= 1
                # If we went past the beginning of the latest file from the end of the diskmap,
                # move down to the next latest file
                if end_i <= 0:
                    end_n -= 2
                    # Restart at the end of this file
                    end_i = int(files[end_n])
                pos += 1
                # If the progress from the start of the filesystem meets the progress from the end,
                # we have covered everything and should stop
                if end_n <= n and end_i - 1 <= i:
                    done = True
                    break
        if done:
            break

    return checksum

def Day9_Part2(input_file: str='Inputs/Day9_Inputs.txt') -> int:
    """
    Calculates the checksum of a filesystem whose disk map is given in an input file, after it has
    undergone a compacting procedure. The disk map uses a dense format to represent the layout of 
    files and free space on the disk. The digits alternate between indicating the length of a file
    and the length of free space. Each file on disk also has an ID number based on the order of the
    files as they appear before they are rearranged, starting with ID 0. The compacting procedure
    now moves whole files instead from the end of the disk to the leftmost span of free space
    blocks that could fit the file. Attempt to move each file exactly once in order of decreasing
    file ID number starting with the file with the highest file ID number. If there is no span of
    free space to the left of a file that is large enough to fit the file, the file does not move.
    The checksum is the sum of the result of multiplying each of these blocks' position with the
    file ID number it contains. The leftmost block is in position 0. If a block contains free
    space, skip it instead.

    Parameters
    ----------
    input_file : str, optional
        Input file giving the disk map.
        The default is 'Inputs/Day9_Inputs.txt'.

    Returns
    -------
    checksum : int
        Checksum of the compacted filesystem.

    """
    # Parse input file to extract disk map
    files = get_input(input_file)

    # Track uncompressed filesystem as a list of tuples of the form (start_pos, id, length)
    filesystem = []
    pos = 0
    # Loop over diskmap
    for n, f in enumerate(files):
        # If even, this is a file
        if not n%2:
            # Record start position, ID (half of n) and length
            filesystem.append([pos, n//2, int(f)])
        else:
            # Else this is free space, record with id of -1
            filesystem.append([pos, -1, int(f)])
        pos += int(f)
    
    from tqdm import tqdm

    # Loop over every second entry in the uncompressed filesystem (files)
    for n in tqdm(range(0, len(filesystem), 2)[::-1]):
        # Loop through free space from the start up to this point
        for n_empty in range(1, n, 2):
            # If the space is large enough to fit the file
            if filesystem[n_empty][2] >= filesystem[n][2]:
                # Move the start position of this file to the start of the free space
                filesystem[n][0] = filesystem[n_empty][0] + 0
                # Move the start position of the free space along by the length of the moved file
                filesystem[n_empty][0] += filesystem[n][2]
                # Decrease the length of the free space by the length of the moved file
                filesystem[n_empty][2] -= filesystem[n][2]
                break
    
    # Calculate checksum across the compacted filesystem
    checksum = sum(sum((filesystem[n][0] + i)*filesystem[n][1] for i in range(filesystem[n][2])) \
                   for n in range(0, len(filesystem), 2))
    
    return checksum
