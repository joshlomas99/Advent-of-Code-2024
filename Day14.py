import re
import numpy as np

def get_input(input_file: str='Inputs/Day14_Inputs.txt') -> tuple:
    """
    Extract the states of a collection of robots from an input file.    

    Parameters
    ----------
    input_file : str, optional
        Input file giving the robot states.
        The default is 'Inputs/Day14_Inputs.txt'.

    Returns
    -------
    pos : numpy.ndarray
        Numpy array with the (x, y) positions of each robot.
    vel : numpy.ndarray
        Numpy array with the (vx, vy) velocities of each robot.
    bounds : numpy.ndarray
        Numpy array giving the boundaries in which the robots are confined.

    """
    # Extract lines from input file
    with open(input_file) as f:
        lines = [l.strip() for l in f.readlines()]
    
    # Initialise lists of robot properties
    pos, vel =  [], []
    for l in lines:
        # Extract digits and convert to integers
        prop = tuple(int(i) for i in re.findall('[-+]?\d+', l))
        pos.append(prop[:2])
        vel.append(prop[2:])
    
    pos, vel = np.array(pos), np.array(vel)

    # Find bounds of robot positions
    bounds = np.max(pos, axis=0)+1

    return pos, vel, bounds

def Day14_Part1(input_file: str='Inputs/Day14_Inputs.txt') -> int:
    """
    Determines the safety factor of a collection of robots, whose initial positions and velocities
    are given in an input file, after exactly 100 seconds have elapsed. Each robot's position is
    given as p=x,y where x represents the number of tiles the robot is from the left wall and y
    represents the number of tiles from the top wall (when viewed from above). Each robot's 
    velocity is given as v=x,y where x and y are given in tiles per second. Positive x means the
    robot is moving to the right, and positive y means the robot is moving down. The robots are
    confined to a boundary defined by the maximum initial positions in both axes across all the
    robots. When a robot would run into an edge of the space they're in, they instead teleport to
    the other side, effectively wrapping around the edges. Multiple robots can occupy the same tile.
    The safety score is found by multiplying together the numbers of robots in each tile quadrant.
    Robots that are exactly in the middle (horizontally or vertically) don't count as being in any
    quadrant.

    Parameters
    ----------
    input_file : str, optional
        Input file giving the initial robot states.
        The default is 'Inputs/Day14_Inputs.txt'.

    Returns
    -------
    safety_score : int
        The safety score of the robots after 100 seconds have elapsed.

    """
    # Parse input file to extract robot properties
    pos, vel, bounds = get_input(input_file)

    # Move every robot 100 steps and wrap around with modulo by the bounds
    pos = (pos + (100*vel))%bounds
    # Find the middle row and column
    middle = bounds//2

    # Count the number of robots in each quadrant
    top_left = np.sum((pos[:, 0] < middle[0]).T * (pos[:, 1] < middle[1]).T)
    top_right = np.sum((pos[:, 0] > middle[0]).T * (pos[:, 1] < middle[1]).T)
    bottom_left = np.sum((pos[:, 0] < middle[0]).T * (pos[:, 1] > middle[1]).T)
    bottom_right = np.sum((pos[:, 0] > middle[0]).T * (pos[:, 1] > middle[1]).T)

    # Calculate safety score
    safety_score = top_left*top_right*bottom_left*bottom_right

    return safety_score
    
import matplotlib.pyplot as plt

def Day14_Part2(input_file: str='Inputs/Day14_Inputs.txt') -> int:
    """
    Determines the fewest number of seconds that must elapse for a collection of robots, whose
    initial positions and velocities are given in an input file, to display an Easter egg where
    they arrange themselves into a picture of a Christmas tree. Each robot's initial position is
    given as p=x,y where x represents the number of tiles the robot is from the left wall and y
    represents the number of tiles from the top wall (when viewed from above). Each robot's 
    velocity is given as v=x,y where x and y are given in tiles per second. Positive x means the
    robot is moving to the right, and positive y means the robot is moving down. The robots are
    confined to a boundary defined by the maximum initial positions in both axes across all the
    robots. When a robot would run into an edge of the space they're in, they instead teleport to
    the other side, effectively wrapping around the edges. Multiple robots can occupy the same tile.

    Parameters
    ----------
    input_file : str, optional
        Input file giving the initial robot states.
        The default is 'Inputs/Day14_Inputs.txt'.

    Returns
    -------
    tree_time : int
        The smallest time before the robots arrange into the shape of a tree.

    """
    # Parse input file to extract robot properties
    pos, vel, bounds = get_input(input_file)

    # Track the variance of robot positions over a large period of time
    var = []
    for n in range(10000):
        # Find new positions and variance at each time
        pos = (pos + vel)%bounds
        var.append(np.var(pos))

    # The minimum variance will correspond to the tight arrangement of robots into the tree
    tree_time = np.argmin(var) + 1

    # Plot the corresponding robot layout to confirm
    pos, vel, bounds = get_input(input_file)
    pos = (pos + (tree_time*vel))%bounds

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.axis("off")
    fig.patch.set_facecolor((0, 0, 0))
    ax.scatter(pos[:, 0], pos[:, 1], s=1.1, color=(1, 1, 1), marker='s')
    ax.text(1, 0, f"t = {tree_time} s", color=(1, 1, 1), fontsize=10,
            horizontalalignment='right', verticalalignment='bottom', transform=ax.transAxes)
    plt.gca().invert_yaxis()
    ax.set_xlim(0, bounds[0])
    ax.set_ylim(bounds[1], 0)
    ax.set_aspect('equal')
    plt.show()

    return tree_time

import matplotlib.animation as animation

def make_gif(input_file: str='Inputs/Day14_Inputs.txt', tree_time: int=8006) -> None:
    """
    Simulate robot movement in small time window around the tree formation and save as a GIF.

    Parameters
    ----------
    input_file : str, optional
        Input file giving the initial robot states.
        The default is 'Inputs/Day14_Inputs.txt'.
    tree_time : int, optional
        Time at which the tree is formed.
        The default is 8006.

    Returns
    -------
    None.

    """
    # Parse input file to extract robot states
    pos, vel, bounds = get_input(input_file)
    # Find robot positions 1 second before tree formation
    pos = (pos + ((tree_time-1)*vel))%bounds

    # Make plot
    fig = plt.figure(figsize=(5, 5))
    ax = fig.add_subplot(1, 1, 1)
    ax.axis("off")
    fig.patch.set_facecolor((0, 0, 0))
    scat = ax.scatter(pos[:, 0], pos[:, 1], s=1.1, color=(1, 1, 1), marker='s')
    text = ax.text(1, -0.06, f"t = {tree_time:.2f} s", color=(1, 1, 1), fontsize=10,
                   horizontalalignment='right', verticalalignment='bottom', transform=ax.transAxes)
    plt.gca().invert_yaxis()
    ax.set_xlim(0, bounds[0])
    ax.set_ylim(bounds[1], 0)

    # Animate in 0.01s increments
    def animate(i, pos, vel, bounds):
        scat.set_offsets((pos + (i*0.01*vel))%bounds)
        text.set_text(f"t = {(tree_time-1)+(i*0.01):.2f} s")

    # Make animation
    ani = animation.FuncAnimation(fig, animate, repeat=True,
                                  frames=200, interval=50, fargs=(pos, vel, bounds))
    
    # Save as GIF
    writer = animation.PillowWriter(fps=15,
                                    metadata=dict(artist='Me'),
                                    bitrate=1800)
    writer.setup(fig, "Day14.gif", dpi = 300)
    ani.save('Day14.gif', writer=writer, dpi = "figure")
    
    plt.show()
