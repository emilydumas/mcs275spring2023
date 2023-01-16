# MCS 275 Spring 2023 Lecture 3
"Classes representing 3-dimensional geometric objects"  # module docstring

# math module in the standard library
# contains constant math.pi
import math

# Think about: Should Sphere and Cube be subclasses
# of some base class?  If so, what methods would
# that class have, and what would they do?

class Sphere:
    "Sphere in 3D space specified by center and radius"  # class docstring

    def __init__(self, cx, cy, cz, r):  # constructor: sets things up
        "Initialize a new sphere with center (cx,cy,cz) and radius r"  # method docstring
        self.cx = cx  # make a new attribute self.cx, set equal to the argument cx
        self.cy = cy
        self.cz = cz
        self.r = r

    def __str__(self):
        "Human-readable string representation"
        return "Sphere(cx={},cy={},cz={},r={})".format(
            self.cx, self.cy, self.cz, self.r
        )

    def __repr__(self):
        "Unambiguous string representation"
        return str(self)  # str(self) -->  self.__str__()

    def volume(self):
        "Return the volume of the sphere"  # method docstring
        return (4 / 3) * math.pi * (self.r**3)

    def surface_area(self):
        "Return the surface area of the sphere"
        return 4 * math.pi * (self.r**2)


# S = Sphere(1,2,3,50)  # make sphere of radius 50 centered at (1,2,3)


class Cube:
    "Cube in 3D space specified by center and side length"

    def __init__(self, cx, cy, cz, side):
        self.cx = cx
        self.cy = cy
        self.cz = cz
        self.side = side

    def __str__(self):
        "Human-readable string representation"
        return "Cube(cx={},cy={},cz={},side={})".format(
            self.cx, self.cy, self.cz, self.side
        )

    def __repr__(self):
        "Unambiguous string representation"
        return str(self)

    def volume(self):
        return self.side**3
