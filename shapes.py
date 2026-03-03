"""Shapes."""
from abc import ABC, abstractmethod
import math


class Shape(ABC):
    """General shape class."""

    def __init__(self, color: str):
        """Shape constructor."""
        self._color = color

    def set_color(self, color: str):
        """Set the color of the shape."""
        self._color = color

    def get_color(self) -> str:
        """Get the color of the shape."""
        return self._color

    @abstractmethod
    def get_area(self) -> float:
        """Get area method which every subclass has to override."""
        print("Implement area")


class Circle(Shape):
    """Circle is a subclass of Shape."""

    def __init__(self, color: str, radius: float):
        """
        Circle constructor.

        The color is stored using superclass constructor:
        super().__init__(color)

        The radius value is stored here.
        """
        super().__init__(color)
        self._radius = radius

    def __repr__(self) -> str:
        """
        Return representation of the circle.

        For this exercise, this should return a string:
        Circle (r: {radius}, color: {color})
        """
        return f"Circle (r: {self._radius}, color: {self._color})"

    def get_area(self) -> float:
        """
        Calculate the area of the circle.

        Area of the circle is pi * r * r.
        """
        return math.pi * self._radius * self._radius


class Square(Shape):
    """Square is a subclass of Shape."""

    def __init__(self, color: str, side: float):
        """
        Square constructor.

        The color is stored using superclass constructor:
        super().__init__(color)

        The side value is stored here.
        """
        super().__init__(color)
        self._side = side

    def __repr__(self) -> str:
        """
        Return representation of the square.

        For this exercise, this should return a string:
        Square (a: {side}, color: {color})
        """
        return f"Square (a: {self._side}, color: {self._color})"

    def get_area(self) -> float:
        """
        Calculate the area of the square.

        Area of the square is side * side.
        """
        return self._side * self._side


class Rectangle(Shape):
    """Rectangle is a subclass of Shape."""

    def __init__(self, color: str, length: float, width: float):
        """Rectangle is a subclass of Shape."""
        super().__init__(color)
        self._length = length
        self._width = width

    def __repr__(self) -> str:
        """
        Return representation of the square.

        For this exercise, this should return a string:
        rectangle (l: {length}, w: {width}, color: {color})
        """
        return f"Rectangle (l: {self._length}, w: {self._width}, color: {self._color})"

    def get_area(self) -> float:
        """
        Calculate the area of the square.

        Area of the square is side * width.
        """
        return self._length * self._width


class Paint:
    """The main program to manipulate the shapes."""

    def __init__(self):
        """Paint constructor."""
        self.shapes = []

    def add_shape(self, shape: Shape) -> None:
        """Add a shape to the program."""
        self.shapes.append(shape)

    def get_shapes(self) -> list:
        """Return all the shapes."""
        return self.shapes

    def calculate_total_area(self) -> float:
        """Calculate total area of the shapes."""
        return sum(shape.get_area() for shape in self.shapes)

    def get_circles(self) -> list:
        """Return only circles."""
        return [shape for shape in self.shapes if isinstance(shape, Circle)]

    def get_squares(self) -> list:
        """Return only squares."""
        return [shape for shape in self.shapes if isinstance(shape, Square)]

    def get_rectangles(self) -> list:
        """Return only rectangles."""
        return [shape for shape in self.shapes if isinstance(shape, Rectangle)]


if __name__ == '__main__':
    paint = Paint()
    circle = Circle("blue", 10)
    square = Square("red", 11)
    print(circle)
    print(square)
    paint.add_shape(circle)
    paint.add_shape(square)
    print(paint.shapes)
    print(paint.calculate_total_area())
    print(paint.get_circles())
