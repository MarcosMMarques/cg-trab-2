from typing import Tuple


class Geometry:
    _id_counter = 0

    def __init__(self):
        self.id = Geometry._generate_id()

    @classmethod
    def _generate_id(cls) -> int:
        cls._id_counter += 1
        return cls._id_counter

    def getId(self) -> int:
        return self.id

    def getFigure(self) -> str:
        return self.__class__.__name__

    def toString(self) -> str:
        raise NotImplementedError("Subclasses should implement this method")


class Point(Geometry):
    def __init__(self, point: Tuple[int, int]):
        super().__init__()
        self.point = point

    def getPoint(self):
        return self.point

    def toString(self) -> str:
        return f"({self.point[0]},{self.point[1]})"


class Line(Geometry):
    def __init__(self, point1: Point, point2: Point):
        super().__init__()
        self.line = [point1, point2]

    def getLine(self):
        return self.line

    def toString(self) -> str:
        return f"{Point(self.line[0]).toString()}, {Point(self.line[1]).toString()}"


class Polygon(Geometry):
    def __init__(self, *points: Point):
        super().__init__()
        self.polygon = list(points)

    def getPolygon(self) -> list[Point]:
        return self.polygon

    def toString(self) -> str:
        return ", ".join(point.toString() for point in self.polygon)
