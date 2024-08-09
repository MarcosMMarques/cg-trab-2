class Window:
    def __init__(self, xwMin, xwMax, ywMin, ywMax):
        self.xwMin = xwMin
        self.xwMax = xwMax
        self.ywMin = ywMin
        self.ywMax = ywMax

    def setXwMin(self, xwMin):
        self.xwMin = xwMin

    def setXwMax(self, xwMax):
        self.xwMax = xwMax

    def setYwMin(self, ywMin):
        self.ywMin = ywMin

    def setYwMax(self, ywMax):
        self.ywMax = ywMax

    def getXwMin(self):
        return self.xwMin

    def getXwMax(self):
        return self.xwMax

    def getYwMin(self):
        return self.ywMin

    def getYwMax(self):
        return self.ywMax