class Viewport:
    def __init__(self, xvMin, xvMax, yvMin, yvMax):
        self.xvMin = xvMin
        self.xvMax = xvMax
        self.yvMin = yvMin
        self.yvMax = yvMax

    def setXvMin(self, xvMin):
        self.xvMin = xvMin

    def setXvMax(self, xvMax):
        self.xvMax = xvMax

    def setYvMin(self, yvMin):
        self.yvMin = yvMin

    def setYvMax(self, yvMax):
        self.yvMax = yvMax

    def getXvMin(self):
        return self.xvMin

    def getXvMax(self):
        return self.xvMax

    def getYvMin(self):
        return self.yvMin

    def getYvMax(self):
        return self.yvMax
