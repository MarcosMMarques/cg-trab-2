import numpy as np

class Window:
    def __init__(self, xwMin, xwMax, ywMin, ywMax):
        self.xwMin = xwMin
        self.xwMax = xwMax
        self.ywMin = ywMin
        self.ywMax = ywMax
        self.angle = 0

    def getCenter(self):
        cx = (self.xwMax - self.xwMin) / 2
        cy = (self.ywMax - self.ywMin) / 2
        return (cx, cy)

    def rotate(self, angle):
        self.angle += angle
        if (self.angle >= 360):
            self.angle = self.angle % 360
        if (self.angle <= -360):
            self.angle = (self.angle * -1) % 360
        center = self.getCenter()
        self.apply_rotation(self.angle, center[0], center[1])

    def apply_rotation(self, angle, cx, cy):
        # Transladar para que o centro da janela seja a origem
        T_to_origin = np.array([
            [1, 0, -cx],
            [0, 1, -cy],
            [0, 0, 1]
        ])

        # Matriz de rotação
        R = np.array([
            [np.cos(angle), -np.sin(angle), 0],
            [np.sin(angle), np.cos(angle), 0],
            [0, 0, 1]
        ])

        # Transladar de volta à posição original
        T_back = np.array([
            [1, 0, cx],
            [0, 1, cy],
            [0, 0, 1]
        ])

        # Matriz de transformação total
        M = T_back @ R @ T_to_origin

        # Aplicar a matriz de transformação às coordenadas da self
        coords = np.array([
            [self.xwMin, self.xwMax, self.xwMin, self.xwMax],
            [self.ywMin, self.ywMin, self.ywMax, self.ywMax],
            [1, 1, 1, 1]
        ])

        new_coords = M @ coords

        # Atualizar as coordenadas da self
        self.xwMin, self.xwMax = np.min(new_coords[0, :]), np.max(new_coords[0, :])
        self.ywMin, self.ywMax = np.min(new_coords[1, :]), np.max(new_coords[1, :])


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

    def setAngle(self, angle):
        self.angle += angle
        # if (self.angle >= 360):
        #     self.angle = self.angle % 360
        # if (self.angle <= -360):
        #     self.angle = self.angle % -360

    def getAngle(self):
        return self.angle
