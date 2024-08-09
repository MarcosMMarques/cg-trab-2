from typing import List
from geometry.geometry import *
from window import *
from viewport import *
import xml.etree.ElementTree as ET


class XmlReader:
    def __init__(self, filepath):
        self.filepath = filepath
        tree = ET.parse(self.filepath)
        self.root = tree.getroot()
        self.window = Window(0, 0, 0, 0)
        self.viewport = Viewport(0, 0, 0, 0)
        self.poitList = []
        self.lineList = []
        self.polygonList = []

        for wmin in self.root.findall("./window/wmin"):
            self.window.setXwMin(float(wmin.attrib.get('x')))
            self.window.setYwMin(float(wmin.attrib.get('y')))

        for wmax in self.root.findall("./window/wmax"):
            self.window.setXwMax(float(wmax.attrib.get('x')))
            self.window.setYwMax(float(wmax.attrib.get('y')))

        for vmin in self.root.findall("./viewport/vpmin"):
            self.viewport.setXvMin(float(vmin.attrib.get('x')))
            self.viewport.setYvMin(float(vmin.attrib.get('y')))

        for vmax in self.root.findall("./viewport/vpmax"):
            self.viewport.setXvMax(float(vmax.attrib.get('x')))
            self.viewport.setYvMax(float(vmax.attrib.get('y')))

        for ponto in self.root.findall("./ponto"):
            x0 = float(ponto.attrib.get('x'))
            y0 = float(ponto.attrib.get('y'))
            self.poitList.append(Point((x0, y0)))

        for reta in self.root.findall("./reta"):
            retaAtual = []
            for ponto in reta:
                x0 = float(ponto.attrib.get('x'))
                y0 = float(ponto.attrib.get('y'))
                retaAtual.append(Point((x0, y0)))
            self.lineList.append(Line(retaAtual[0], retaAtual[1]))

        for poligono in self.root.findall("./poligono"):
            poligonoAtual = []
            for ponto in poligono:
                x0 = float(ponto.attrib.get('x'))
                y0 = float(ponto.attrib.get('y'))
                poligonoAtual.append(Point((x0, y0)))
            polig = Polygon(*poligonoAtual)
            self.polygonList.append(polig)

    def getWindow(self) -> Window:
        return self.window

    def getViewport(self) -> Viewport:
        return self.viewport

    def getPontos(self) -> List[Point]:
        return self.poitList

    def getRetas(self) -> List[Line]:
        return self.lineList

    def getPoligonos(self) -> List[Polygon]:
        return self.polygonList
