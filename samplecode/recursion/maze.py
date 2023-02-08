# MCS 275 Spring 2023 - David Dumas
"""Module for dealing with mazes represented as
rectangular arrays of cells, each of which can be
marked "free" or "blocked"."""

from plane import Point2, Vector2
import random


class Maze:
    """Rectangular grid of free/blocked cells.
    Optionally, can store a starting point and goal."""

    neighbor_disps = [Vector2(-1, 0), Vector2(0, -1), Vector2(1, 0), Vector2(0, 1)]

    def __init__(self, xsize, ysize, start=None, goal=None):
        """Initialize new empty maze"""
        self.xsize = xsize
        self.ysize = ysize
        self.start = start
        self.goal = goal
        self.grid = [[" "] * self.xsize for _ in range(self.ysize)]

    def __str__(self):
        """Crude text picture"""
        return "\n".join("".join(r) for r in self.grid)

    def __repr__(self):
        """Default to using str() for everything"""
        return str(self)

    def is_valid(self, p):
        """Is `p` a valid position for this maze?"""
        if not isinstance(p, Point2):
            raise ValueError("Location must be specified as Point2 instance")
        if p.x < 0 or p.x >= self.xsize:
            return False
        if p.y < 0 or p.y >= self.ysize:
            return False
        return True

    def insist_valid(self, p):
        """Raise exception if `p` not a valid position"""
        if not self.is_valid(p):
            raise ValueError(
                "Position {} invalid for this maze with (xsize,ysize)=({},{})".format(
                    p, self.xsize, self.ysize
                )
            )

    def is_free(self, p):
        """Is the cell at point `p` free?"""
        self.insist_valid(p)
        return self.grid[p.y][p.x] == " "

    def is_blocked(self, p):
        """Is the cell at point `p` blocked?"""
        return not self.is_free(p)

    def set_free(self, p):
        """Clear the cell at point `p`"""
        self.insist_valid(p)
        self.grid[p.y][p.x] = " "

    def set_blocked(self, p):
        """Put a wall at point `p`"""
        self.insist_valid(p)
        self.grid[p.y][p.x] = "@"

    def free_neighbors(self, p):
        """Return list of neighbors of point `p` that
        are currently free"""
        nbrs = []
        for v in self.neighbor_disps:
            try:
                if self.is_free(p + v):
                    nbrs.append(p + v)
            except ValueError:
                continue
        return nbrs

    def apply_border(self):
        """Make all edge cells into walls"""
        self.grid[0] = ["@"] * self.xsize
        self.grid[-1] = ["@"] * self.xsize
        for y in range(1, self.ysize - 1):
            self.grid[y][0] = "@"
            self.grid[y][-1] = "@"

    def save_png(self, fn, scale=1, highlight=[]):
        """
        Save maze to a PNG file (requires PIL or Pillow module).
        If given, `highlight` is expected to be a list of `Point2`
        objects that are locations in the maze to be highlighted in
        blue.
        """
        m = scale
        try:
            import PIL.Image
            import PIL.ImageDraw
        except ImportError:
            raise RuntimeError(
                "This feature requires PIL or Pillow to be installed; try `python3 -m pip install pillow`."
            )
        img = PIL.Image.new("RGB", (m * self.xsize, m * self.ysize))
        draw = PIL.ImageDraw.Draw(img)
        for x in range(self.xsize):
            for y in range(self.ysize):
                p = Point2(x, y)
                fillcolor = (255, 255, 255)
                if self.is_blocked(p):
                    fillcolor = (50, 50, 50)
                elif self.start == p:
                    fillcolor = (200, 150, 100)
                elif self.goal == p:
                    fillcolor = (0, 200, 0)
                elif p in highlight:
                    fillcolor = (150, 150, 240)
                draw.rectangle(
                    [(x * m, y * m), ((x + 1) * m - 1, (y + 1) * m - 1)], fill=fillcolor
                )
        img.save(fn, format="PNG")

    def save_svg(self, fn, highlight=[]):
        """
        Save maze to a SVG file
        If given, `highlight` is expected to be a list of `Point2`
        objects that are locations in the maze to be highlighted in
        blue.
        """
        rmax = max(self.xsize, self.ysize)
        m = max(1, 720 // rmax)
        with open(fn, "wt") as outfile:
            outfile.write('<?xml version="1.0" standalone="no"?>\n')
            outfile.write(
                '<svg width="{}" height="{}" version="1.1" xmlns="http://www.w3.org/2000/svg">\n'.format(
                    m * self.xsize, m * self.ysize
                )
            )
            outfile.write(
                '<rect x="{}" y="{}" width="{}" height="{}" stroke="none" fill="white"/>\n'.format(
                    0, 0, m * self.xsize, m * self.ysize
                )
            )
            for x in range(self.xsize):
                for y in range(self.ysize):
                    p = Point2(x, y)
                    fillcolor = None
                    if self.is_blocked(p):
                        fillcolor = (50, 50, 50)
                    elif self.start == p:
                        fillcolor = (200, 150, 100)
                    elif self.goal == p:
                        fillcolor = (0, 200, 0)
                    elif p in highlight:
                        fillcolor = (150, 150, 240)
                    if fillcolor:
                        outfile.write(
                            '<rect x="{}" y="{}" width="{}" height="{}" stroke="none" fill="{}"/>\n'.format(
                                x * m, y * m, m, m, tohexcolor(fillcolor)
                            )
                        )
            outfile.write("</svg>")


class PrimRandomMaze(Maze):
    """Randomly generated maze using Prim's algorithm:
    https://en.wikipedia.org/wiki/Prim%27s_algorithm
    (Known for producing mazes with lots of short dead
    ends, only moderately challenging for humans.)"""

    frontier_disps = [Vector2(-2, 0), Vector2(0, -2), Vector2(2, 0), Vector2(0, 2)]

    def __init__(self, xsize, ysize):
        """Create a new random maze of size (xsize,ysize).
        Both dimensions must be odd."""
        super().__init__(xsize, ysize)
        if self.xsize % 2 == 0 or self.ysize % 2 == 0:
            raise ValueError("xsize and ysize must be odd")
        self.grid = [["@"] * self.xsize for _ in range(self.ysize)]
        self.generate()
        self.start = Point2(1, 1)
        self.goal = Point2(self.xsize - 2, self.ysize - 2)
        assert self.is_free(self.start)
        assert self.is_free(self.goal)

    def generate(self):
        """Make the maze using Prim's algorithm"""
        sx = 2 * random.randrange(self.xsize // 2) + 1
        sy = 2 * random.randrange(self.ysize // 2) + 1
        s = Point2(sx, sy)
        self.set_free(s)
        frontier = self.cell_frontier(s)
        while frontier:
            p = frontier.pop(random.randrange(len(frontier)))
            nbrs2 = self.cell_neighbors2(p)
            if nbrs2:
                p2 = random.choice(nbrs2)
                qx = (p.x + p2.x) // 2
                qy = (p.y + p2.y) // 2
                q = Point2(qx, qy)
                self.set_free(p)
                self.set_free(q)
                nf = self.cell_frontier(p)
                for r in nf:
                    if r not in frontier:
                        frontier.append(r)

    def cell_frontier(self, p):
        """Return cells at +-2 in x or y that are blocked"""
        F = []
        for v in self.frontier_disps:
            q = p + v
            if self.is_valid(q) and self.is_blocked(q):
                F.append(q)
        return F

    def cell_neighbors2(self, p):
        """Return cells at +-2 in x or y that are free"""
        F = []
        for v in self.frontier_disps:
            q = p + v
            if self.is_valid(q) and self.is_free(q):
                F.append(q)
        return F


class MazeExample1(Maze):
    """7x7 example maze from lecture 15"""

    def __init__(self):
        """Set blocked cells for 7x7 example from lecture 15"""
        super().__init__(xsize=7, ysize=7, start=Point2(1, 1), goal=Point2(5, 5))
        self.apply_border()
        for p in [
            Point2(2, 1),
            Point2(2, 2),
            Point2(3, 2),
            Point2(4, 2),
            Point2(1, 4),
            Point2(2, 4),
            Point2(4, 4),
            Point2(5, 4),
        ]:
            self.set_blocked(p)


def tohexcolor(rgbtuple):
    """Convert 8-bit RGB color tuple to hex color"""
    r, g, b = rgbtuple
    return "#{:02x}{:02x}{:02x}".format(r, g, b)


if __name__ == "__main__":
    # Run as a script
    # First command line argument gives the size (odd integer, default 31)
    # Second command line argument gives output filename (SVG or PNG, defaults to write both as "random_maze.svg" and "random_maze.png")
    import sys

    if len(sys.argv) > 1:
        n = int(sys.argv[1])
    else:
        n = 31
    print("Generating a random {}x{} maze".format(n, n))
    M = PrimRandomMaze(n, n)

    # Determine output filename and type to write (svg, png, both)
    if len(sys.argv) > 2:
        outfn = sys.argv[2]
        if outfn.endswith(".svg"):
            mode = "svg"
        elif outfn.endswith(".png"):
            mode = "png"
        else:
            print(
                "Filename {} does not end with png or svg, so the output format is not known.".format(
                    outfn
                )
            )
            exit(1)
    else:
        outfn = "random_maze.svg"
        mode = "both"

    # Write image

    # SVG
    if mode == "svg" or mode == "both":
        M.save_svg(outfn)
    print("Saved SVG file {}".format(outfn))

    # PNG
    try:
        if mode == "both":
            outfn = outfn[:-4] + ".png"
        if mode == "png" or mode == "both":
            M.save_png(outfn, scale=10)
            print("Saved PNG file {}".format(outfn))
    except ImportError:
        print("Tried to write a PNG file, but something went wrong.  This probably")
        print("means that PIL/Pillow is not installed.  Install it with a command")
        print("such as 'python3 -m pip install pillow' and try again.")
