# MCS 275 Spring 2023 Lecture 12
"Depth first recursive maze solution"

from plane import Point2, Vector2
import maze

def depth_first_maze_solution(M,path=None,verbose=False):
    """
    Find solution to Maze `M` that begins with `path` (if given),
    returning either that solution as a list of Point2 objects or
    None if no such solution exists.
    """
    if path == None:
        # no path was specified, initialize it with [M.start]
        path = [ M.start ]

    if verbose:
        print("Considering:",path)

    if path[-1] == M.goal:
        # path ends with goal, meaning it's a solution
        return path

    possible_next_locations = M.free_neighbors(path[-1])
    for x in possible_next_locations:
        if x in path:
            # skip x
            continue # do not execute the rest of the loop body
                     # immediately begin the next iteration.
        # x should be considered
        new_path = path + [x]
        # Ask for a solution that continues from new_path            
        solution = depth_first_maze_solution(M,new_path,verbose)
        if solution:  # None is falsy, while a nonempty list is truthy
            return solution

    # What now? If we end up here, it means no next step leads to a solution
    # Hence `path` leads to only dead ends
    # We therefore BACKTRACK
    if verbose:
        print("GIVING UP ON:",path)
    return None

if __name__=="__main__":
    # this code runs when solvemaze.py is run as a script
    # demo code goes here
    M = maze.PrimRandomMaze(127,127)
    soln = depth_first_maze_solution(M)
    M.save_svg("maze.svg")
    M.save_svg("maze_solved.svg",highlight=soln)
    print("Saved to maze.svg and maze_solved.svg")