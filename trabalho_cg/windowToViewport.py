from typing import Union
from typing import List
from geometry.geometry import *

from viewport import Viewport
from window import Window


class WindowToViewportConversor:
    def __transform(self, pontos, window: Window, viewport: Viewport):
        Xw, Yw = pontos
        XwMin = window.getXwMin()
        XwMax = window.getXwMax()
        YwMin = window.getYwMin()
        YwMax = window.getYwMax()
        XvpMin = viewport.getXvMin()
        XvpMax = viewport.getXvMax()
        YvpMin = viewport.getYvMin()
        YvpMax = viewport.getYvMax()
        Xvp = XvpMin + ((Xw - XwMin) / (XwMax - XwMin)) * (XvpMax - XvpMin) # Encontra o X do viewport
        Yvp = YvpMin + (1 - ((Yw - YwMin) / (YwMax - YwMin))) * (YvpMax - YvpMin) # Encontra o Y do viewport
        return (Xvp, Yvp)

    def convertToViewport(self, element: Union[Point, Line, Polygon], window: Window, viewport: Viewport):
        if (type(element) == Point):
            point = self.__transform(
                element.getPoint(), window, viewport)
            return Point(point)

        if (type(element) == Line):
            line = []
            for i in range(2):
                line.append(self.__transform(
                    element.getLine()[i], window, viewport))
            return Line(*(line))

        if (type(element) == Polygon):
            polygon = []
            for point in element.getPolygon():
                polygon.append(Point(self.__transform(
                    point.getPoint(), window, viewport)))
            return Polygon(*polygon)
