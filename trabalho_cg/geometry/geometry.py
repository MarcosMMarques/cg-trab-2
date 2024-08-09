from typing import Tuple


class Point():
    def __init__(self, point: Tuple):
        self.point = point

    def getPoint(self):
        return self.point


class Line(Point):
    def __init__(self, point1: Point, point2: Point):
        self.line = [point1, point2]

    def getLine(self):
        return self.line


# class Polygon(Line):
#     def __init__(self, *points: Point):
#         self.polygon = []
#         for point in points:
#             self.polygon.append(point)

#     def getPolygon(self):
#         return self.polygon

class Polygon:
    def __init__(self, *points: Point):
        self.polygon = list(points)

    def getPolygon(self) -> list[Point]:
        return self.polygon