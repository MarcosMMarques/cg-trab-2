import numpy as np

class Window:
    def __init__(self, xwMin, xwMax, ywMin, ywMax):
        self.xwMin = xwMin
        self.xwMax = xwMax
        self.ywMin = ywMin
        self.ywMax = ywMax

    def getCenter(self):
        cx = (self.xwMax - self.xwMin) / 2
        cy = (self.ywMax - self.ywMin) / 2
        return (cx, cy)

    def zoom(self, factor):
        # Calcula o centro da window
        center_x = (self.xwMin + self.xwMax) / 2
        center_y = (self.ywMin + self.ywMax) / 2

        # Matriz de Translação para mover o centro para a origem
        T_to_origin = np.array([
            [1, 0, -center_x],
            [0, 1, -center_y],
            [0, 0, 1]
        ])

        # Matriz de Escala (zoom)
        S = np.array([
            [factor, 0, 0],
            [0, factor, 0],
            [0, 0, 1]
        ])

        # Matriz de Translação para mover de volta ao centro original
        T_back = np.array([
            [1, 0, center_x],
            [0, 1, center_y],
            [0, 0, 1]
        ])

        # Matriz de Transformação total
        M = T_back @ S @ T_to_origin

        # Coordenadas dos cantos da window
        coords = np.array([
            [self.xwMin, self.xwMax, self.xwMin, self.xwMax],
            [self.ywMin, self.ywMin, self.ywMax, self.ywMax],
            [1, 1, 1, 1]
        ])

        # Aplicar a transformação às coordenadas
        new_coords = M @ coords

        # Atualizar as coordenadas da window após o zoom
        self.xwMin, self.xwMax = np.min(new_coords[0, :]), np.max(new_coords[0, :])
        self.ywMin, self.ywMax = np.min(new_coords[1, :]), np.max(new_coords[1, :])

    def moveWindow(self, delta_x, delta_y):
        # Matriz de Translação
        T = np.array([
            [1, 0, delta_x],
            [0, 1, delta_y],
            [0, 0, 1]
        ])

        # Coordenadas dos cantos da window antes da translação
        coords = np.array([
            [self.xwMin, self.xwMax, self.xwMin, self.xwMax],
            [self.ywMin, self.ywMin, self.ywMax, self.ywMax],
            [1, 1, 1, 1]
        ])

        # Aplicar a translação às coordenadas
        new_coords = T @ coords

        # Atualizar as coordenadas da window após a translação
        self.xwMin, self.xwMax = np.min(new_coords[0, :]), np.max(new_coords[0, :])
        self.ywMin, self.ywMax = np.min(new_coords[1, :]), np.max(new_coords[1, :])
        # print("Novas coordenadas mundo: ", self.main_window.getXwMin(), self.main_window.getXwMax(), self.main_window.getYwMin(), self.main_window.getYwMax())

    def reset_position(self, xMin, yMin, xMax, yMax):
        self.setXwMax(xMax)
        self.setYwMax(yMax)
        self.setXwMin(xMin)
        self.setYwMin(yMin)

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
