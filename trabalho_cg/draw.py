from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from geometry.geometry import *

from viewport import Viewport
from geometry.geometry import *

class Draw(QWidget):
    newPoint = pyqtSignal(QPoint)
    viewport = Viewport(0, 1250, 0, 750)

    def __init__(self, parent=None):
        super(Draw, self).__init__(parent)
        self.path = QPainterPath()
        self.initUI()

    def initUI(self):
        self.points: list[Point] = []
        self.lines: list[Line] = []
        self.polygons: list[Polygon] = []

    def mouseMoveEvent(self, event):
        self.newPoint.emit(event.pos())
        self.update()

    def paintEvent(self, e):
        self.setMouseTracking(True)
        qp = QPainter()
        qp.begin(self)
        self.pal = self.palette()
        self.pal.setColor(QPalette.Background, Qt.black)
        self.setAutoFillBackground(True)
        self.setPalette(self.pal)
        penColor = QColor(255, 255, 255)
        pen = QPen(penColor)
        pen.setWidth(5)
        qp.setPen(pen)

        for point in self.points:
            qp.drawPoint(int(point.getPoint()[0]), int(point.getPoint()[1]))

        for line in self.lines:
            p1, p2 = line.getLine()
            x1, y1 = p1
            x2, y2 = p2
            qp.drawLine(int(x1), int(y1), int(x2), int(y2))

        for polygon in self.polygons:
            currentPolygon = []
            points = polygon.getPolygon()
            for point in points:
                currentPolygon.append(QPointF(QPoint(
                    int(point.getPoint()[0]),
                    int(point.getPoint()[1])
                )))
            qp.drawPolygon(QPolygonF(currentPolygon))

        self.qp = qp
        qp.end()

    def drawPoint(self, point: Point):
        self.points.append(point)
        self.update()

    def drawLine(self, line: Line):
        self.lines.append(line)
        self.update()

    def drawPolygon(self, polygon: Polygon):
        self.polygons.append(polygon)
        self.update()

    def setViewport(self, viewport : Viewport):
        self.viewport = viewport
