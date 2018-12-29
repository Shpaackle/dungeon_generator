class Point:
    """
    A simple container to represent a single point in the map's grid
    added functionality for adding, subtracting, or comparing equality of two points
    can be iterated to get x- and y-coordinates

    Args:
        x- and y-coordinate for the point

    Attributes:
        x: x-coordinate of the point
        y: y-coordinate of the point
    """
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        return self.x != other.x and self.y != other.y

    def __hash__(self):
        return self.x ^ self.y

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __repr__(self):
        return f"({self.__class__.__name__}) x={self.x}, y={self.y}"

    def __iter__(self):
        yield self.x
        yield self.y

    def in_grid(self):
        return self.y, self.x
