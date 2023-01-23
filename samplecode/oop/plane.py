# MCS 275 Spring 2023 Lecture 4
"Planar point and vector classes"


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

    def distance_to(self, other):
        "get distance between two points"
        if isinstance(other, Point2):
            return abs(self - other)
        else:
            raise TypeError("distance_to requires argument of type Point2")


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

    def __mul__(self, other):
        "vector-scalar multiplication"
        if isinstance(other, (float, int)):  # isinstance allows a tuple of types
            # vector*scalar is vector
            return Vector2(self.x * other, self.y * other)
        else:
            return NotImplemented

    def __rmul__(self, other):
        "scalar-vector multiplication"
        # Called if other*self already attempted but failed
        # for example if other is an int or float and self is a Vector2
        # This "second chance" reflected version of multiplication lets the
        # right hand operand decide what to do.  In this case, we just decide
        # that other*self is the same as self*other (handled by Vector2.__mul__ above)
        return self * other

    def __neg__(self):
        "unary minus"
        return Vector2(-self.x, -self.y)

    def __pos__(self):
        "unary plus: return a copy of the object"
        return self

    def __abs__(self):
        "abs means length of a vector"
        return (self.x * self.x + self.y * self.y) ** 0.5  # sqrt( deltax^2 + deltay^2 )

    def __str__(self):
        "human-readable string representation"
        return "Vector2({},{})".format(self.x, self.y)

    def __repr__(self):
        "unambiguous string representation"
        return str(self)
