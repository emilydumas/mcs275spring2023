# MCS 275 Spring 2023 Lecture 4
"Planar point and vector classes"

# TODO: Add scalar multiplication


class Point2:
    "Point in the plane"

    def __init__(self, x, y):
        "Initialize new point from x and y coordinates"
        self.x = x
        self.y = y

    def __eq__(self, other):
        "points are equal if and only if they have same coordinates"
        if isinstance(other, Point2):
            return (self.x == other.x) and (self.y == other.y)
        else:
            return False

    def __add__(self, other):
        "point+vector addition"
        if isinstance(other, Vector2):
            # we have been asked to add this Point2 to another Vector2
            return Point2(self.x + other.x, self.y + other.y)
        else:
            # we have been asked to add this Point2 to some other object
            # we don't want to allow this
            return NotImplemented  # return this to forbid the requested operation

    # Planning __sub__ method:
    #   Q - P
    # becomes
    #   Q.__sub__(P)
    # which calls Point2.__sub__ with `self` equal to Q and `other` equal to P
    # The answer should have components Q.x-P.x and Q.y-P.y
    # So that's self.x-other.x and self.y-other.y
    def __sub__(self, other):
        "point-point subtraction, gives displacement vector"
        if isinstance(other, Point2):
            #                 Q.x - P.x        Q.y - P.y
            return Vector2(self.x - other.x, self.y - other.y)
        else:
            return NotImplemented

    def __str__(self):
        "human-readable string representation"
        return "Point2({},{})".format(self.x, self.y)

    def __repr__(self):
        "unambiguous string representation"
        return str(self)


class Vector2:
    "Displacement vector in the plane"

    def __init__(self, x, y):
        "Initialize new vector from x and y components"
        self.x = x
        self.y = y

    def __eq__(self, other):
        "vectors are equal if and only if they have same components"
        if isinstance(other, Vector2):
            return (self.x == other.x) and (self.y == other.y)
        else:
            return False

    def __add__(self, other):
        "vector addition"
        if isinstance(other, Vector2):
            # vector+vector = vector
            return Vector2(self.x + other.x, self.y + other.y)
        elif isinstance(other, Point2):
            # vector + point = point
            return Point2(self.x + other.x, self.y + other.y)
        else:
            # vector + anything else = nonsense
            return NotImplemented  # return this to forbid the requested operation

    def __str__(self):
        "human-readable string representation"
        return "Vector2({},{})".format(self.x, self.y)

    def __repr__(self):
        "unambiguous string representation"
        return str(self)
