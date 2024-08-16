from typing import Tuple
from typing_extensions import Optional, overload


class Geometry:
    _id_counter = 0

    def __init__(self):
        self.id = Geometry._generate_id()

    def setId(self, new_id: int):
        self.id = new_id

    @classmethod
    def _generate_id(cls) -> int:
        cls._id_counter += 1
        return cls._id_counter

    def getId(self) -> int:
        return self.id

    def getFigure(self) -> str:
        return self.__class__.__name__

    def __str__(self) -> str:
        raise NotImplementedError("Subclasses should implement this method")


class Point(Geometry):
    def __init__(self, point: Optional[Tuple[int, int]] = None):
        if point is not None:
            super().__init__()
            self.point = point
            return
        self.point = None

    def setPoint(self, new_point: Tuple[int, int]):
        self.point = new_point

    def getPoint(self) -> Optional[Tuple[int, int]]:
        return self.point

    def __str__(self) -> str:
            if self.point is None:
                return "Point is not set"
            return f"({self.point[0]},{self.point[1]})"

    def __iter__(self):
            if self.point is not None:
                yield from self.point
            else:
                raise ValueError("Point is not set")


class Line(Geometry):
    def __init__(self, point1: Optional[Point] = None, point2: Optional[Point] = None):
        if point1 is not None or point2 is not None:
            super().__init__()
            self.line = [point1, point2]

    def setLine(self, point1: Point, point2: Point):
        self.line = [point1, point2]

    def getLine(self):
        return self.line

    def __str__(self) -> str:
        if self.line[0] is None or self.line[1] is None:
            return "Line is not set"
        return f"{Point(self.line[0]).__str__()}, {Point(self.line[1]).__str__()}"


class Polygon(Geometry):
    def __init__(self, *points: Optional[Point]):
            self.polygon = []
            if points and len(points) > 0:
                super().__init__()
                self.polygon = list(points)

    def setPolygon(self, *points: Point):
        self.polygon = list(points)

    def getPolygon(self):
        return self.polygon

    def __len__(self):
        return len(self.polygon)

    def __str__(self) -> str:
        if self.polygon is None:
            return "Polygon is not set"
        return ", " . join(point.__str__() for point in self.polygon)
