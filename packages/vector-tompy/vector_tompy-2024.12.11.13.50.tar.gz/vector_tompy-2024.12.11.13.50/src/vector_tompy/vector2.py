import math
from dataclasses import dataclass
from decimal import Decimal
from math import sqrt
from typing import Self, Iterator

from math_tompy.symbolic import expr_to_calc
from sympy import Point2D, Expr

from .exceptions import EmptyIterableError


# Pi with 500 significant digits
# pi: Decimal = Decimal("3.14159265358979323846264338327950288419716939937510582097494459230781640628620899862803482534211706798214808651328230664709384460955058223172535940812848111745028410270193852110555964462294895493038196442881097566593344612847564823378678316527120190914564856692346034861045432664821339360726024914127372458700660631558817488152092096282925409171536436789259036001133053054882046652138414695194151160943305727036575959195309218611738193261179310511854807446237996274956735188575272489122793818301194912")
# Pi based on math float value for compatibility without requiring import of pi from here
pi: Decimal = Decimal(math.pi)


@dataclass
class Vector2:
    x: Decimal
    y: Decimal

    def __init__(self, x, y) -> None:
        if isinstance(x, Expr):
            self.x = expr_to_calc(expression=x).result()
            self.y = expr_to_calc(expression=y).result()
        else:
            self.x = Decimal(x)
            self.y = Decimal(y)

    def __add__(self, other: Self) -> Self:
        x_: Decimal = self.x + other.x
        y_: Decimal = self.y + other.y
        vector: Self = Vector2(x=x_, y=y_)
        return vector

    def __sub__(self, other: Self) -> Self:
        x_: Decimal = self.x - other.x
        y_: Decimal = self.y - other.y
        vector: Self = Vector2(x=x_, y=y_)
        return vector

    def __mul__(self, other: Self | Decimal) -> Self:
        if isinstance(other, Vector2):
            x_: Decimal = self.x * other.x
            y_: Decimal = self.y * other.y
        elif isinstance(other, Decimal):
            x_: Decimal = self.x * other
            y_: Decimal = self.y * other
        else:
            raise TypeError(f"Type '{type(other)}' of other is not supported for '{type(Self)}' multiplication.")
        vector: Self = Vector2(x=x_, y=y_)
        return vector

    def __abs__(self) -> Decimal:
        origin = Vector2Injector.from_decimal(x=Decimal(0), y=Decimal(0))
        distance = origin.distance(other=self)
        return distance

    def __iter__(self):
        return iter([self.x, self.y])

    def __len__(self) -> int:
        return 2

    def __getitem__(self, index: int | slice) -> Decimal:
        if isinstance(index, int):
            if int == 0:
                value: Decimal = self.x
            elif int == 1:
                value: Decimal = self.y
            else:
                raise IndexError(f"Index '{index}' out of valid range [0, 1].")
        elif isinstance(index, slice):
            # if wraparound:
            #     value: Self = self._get_slice_with_wraparound(slice_=index)
            # else:
            #     value: Self = self._get_slice(slice_=index)
            raise ValueError(f"__getitem__ does not support slice.")
        else:
            raise ValueError(f"__getitem__ requires an integer or a slice, not a {type(index)}.")
        return value

    def __eq__(self, other: Self) -> bool:
        equality: bool = False
        same_type: bool = isinstance(other, type(self))
        if same_type:
            same_x: bool = self.x == other.x
            same_y: bool = self.y == other.y
            equality = same_x and same_y
        return equality

    def __hash__(self):
        return hash(self.__repr__())

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.x}, {self.y})"

    @property
    def unit(self) -> Self:
        length: Decimal = abs(self)
        x_: Decimal = self.x / length
        y_: Decimal = self.y / length
        vector: Self = Vector2Injector.from_decimal(x=x_, y=y_)
        return vector

    def distance(self, other: Self) -> Decimal:
        pair_squares: list[Decimal] = [Decimal((value0 - value1) ** 2) for value0, value1 in zip(self, other)]
        square_sum: Decimal = Decimal(sum(pair_squares))
        root_of_pair_square_sum: Decimal = Decimal(sqrt(square_sum))
        return root_of_pair_square_sum


class Vector2Injector:
    @staticmethod
    def from_point(point: Point2D) -> Vector2:
        # x: Decimal = Decimal(expr_to_calc(expression=point.x).result())
        # y: Decimal = Decimal(expr_to_calc(expression=point.y).result())
        # vector: Vector2 = Vector2(x=x, y=y)
        # return vector
        vector: Vector2 = Vector2(x=point.x, y=point.y)
        return vector

    @staticmethod
    def from_decimal(x: Decimal, y: Decimal) -> Vector2:
        vector: Vector2 = Vector2(x=x, y=y)
        return vector


def positions_from(samples_x: int, samples_y: int, resolution: Decimal) -> Iterator[Vector2]:
    x_positions: list[Decimal] = [sample * resolution for sample in range(0, samples_x)]
    y_positions: list[Decimal] = [sample * resolution for sample in range(0, samples_y)]

    positions: Iterator[Vector2] = (Vector2Injector.from_decimal(x=x, y=y) for x in x_positions for y in y_positions)

    return positions


def bounding_box(points: list[Vector2]) -> tuple[Vector2, Decimal, Decimal]:
    # Calculates axis-oriented bounding box for point cloud
    # Outputs bottom-left point, height, and width
    if len(points) == 0:
        raise EmptyIterableError(f"Input list is empty.")

    x_min = Decimal('Infinity')
    x_max = Decimal('-Infinity')
    y_min = Decimal('Infinity')
    y_max = Decimal('-Infinity')

    for point in points:
        x = point.x
        y = point.y

        if x < x_min:
            x_min = x
        if x > x_max:
            x_max = x
        if y < y_min:
            y_min = y
        if y > y_max:
            y_max = y

    point = Vector2Injector.from_decimal(x=x_min, y=y_min)
    width: Decimal = x_max - x_min
    height: Decimal = y_max - y_min
    return point, width, height


def centroid(points: list[Vector2]) -> Vector2:
    point_amount: int = len(points)

    xs = [point.x for point in points]
    ys = [point.y for point in points]

    x = sum(xs) / point_amount
    y = sum(ys) / point_amount

    point: Vector2 = Vector2Injector.from_decimal(x=Decimal(x), y=Decimal(y))

    return point


def along_line(start: Vector2, end: Vector2, fraction: Decimal) -> Vector2:
    x_difference = end.x - start.x
    y_difference = end.y - start.y

    x_modified = x_difference * fraction
    y_modified = y_difference * fraction

    x = start.x + x_modified
    y = start.y + y_modified

    position: Vector2 = Vector2Injector.from_decimal(x=x, y=y)

    return position


def opposite(vector: Vector2) -> Vector2:
    return Vector2Injector.from_decimal(x=-vector.x, y=-vector.y)


def perpendicular_clockwise(vector: Vector2) -> Vector2:
    return Vector2Injector.from_decimal(x=vector.y, y=-vector.x)


def perpendicular_anticlockwise(vector: Vector2) -> Vector2:
    return Vector2Injector.from_decimal(x=-vector.y, y=vector.x)


def perpendicular_extrusion(start: Vector2, end: Vector2, fraction: Decimal) -> tuple[Vector2, Vector2, Vector2, Vector2]:
    base_vector: Vector2 = (start - end) * (fraction / Decimal(2))  # Halving fraction for diameter instead of radius
    perpendicular_cw: Vector2 = perpendicular_clockwise(vector=base_vector)
    perpendicular_acw: Vector2 = perpendicular_anticlockwise(vector=base_vector)

    point0: Vector2 = start + perpendicular_acw
    point1: Vector2 = end + perpendicular_acw
    point2: Vector2 = end + perpendicular_cw
    point3: Vector2 = start + perpendicular_cw

    return point0, point1, point2, point3


def shape_node_positions(edges: int, radius: Decimal, direction: Vector2) -> list[Vector2]:
    positions: list[Vector2] = []
    # angle_step_size: Angle = Angle(radian=2 * sp.pi / edges)
    angle_step_size: Decimal = 2 * pi / edges
    first_position: Vector2 = direction.unit * radius
    positions.append(first_position)
    for _ in range(edges-1):
        revolved_position: Vector2 = revolve_around(center=Vector2Injector.from_decimal(x=Decimal(0), y=Decimal(0)),
                                                     point=positions[-1],
                                                     angle=angle_step_size)
        positions.append(revolved_position)

    return positions


# def revolve_around(center: Vector2, point: Vector2, angle: Angle) -> Vector2:
def revolve_around(center: Vector2, point: Vector2, angle: Decimal) -> Vector2:
    """
    https://gamefromscratch.com/gamedev-math-recipes-rotating-one-point-around-another-point/
    """

    # x_revolved: Decimal = Decimal(math.cos(angle.as_radian())) * (point.x - center.x) - \
    #                       Decimal(math.sin(angle.as_radian())) * (point.y - center.y) + \
    #                       center.x
    # y_revolved: Decimal = Decimal(math.sin(angle.as_radian())) * (point.x - center.x) + \
    #                       Decimal(math.cos(angle.as_radian())) * (point.y - center.y) + \
    #                       center.y
    x_revolved: Decimal = Decimal(math.cos(float(angle))) * (point.x - center.x) - \
                          Decimal(math.sin(float(angle))) * (point.y - center.y) + \
                          center.x
    y_revolved: Decimal = Decimal(math.sin(float(angle))) * (point.x - center.x) + \
                          Decimal(math.cos(float(angle))) * (point.y - center.y) + \
                          center.y

    point_revolved: Vector2 = Vector2Injector.from_decimal(x=x_revolved, y=y_revolved)

    return point_revolved
