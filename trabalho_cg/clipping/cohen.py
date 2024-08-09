from window import *

class CohenSutherland:
    def __init__(self, window: Window):
        self.x_min = window.getXwMin()
        self.y_min = window.getYwMin()
        self.x_max = window.getXwMax()
        self.y_max = window.getYwMax()

        # Códigos de região
        self.INSIDE = 0  # 0000
        self.LEFT = 1    # 0001
        self.RIGHT = 2   # 0010
        self.BOTTOM = 4  # 0100
        self.TOP = 8     # 1000

    def compute_code(self,x, y):
        code = self.INSIDE
        if x < self.x_min:      # à esquerda da janela
            code |= self.LEFT
        elif x > self.x_max:    # à direita da janela
            code |= self.RIGHT
        if y < self.y_min:      # abaixo da janela
            code |= self.BOTTOM
        elif y > self.y_max:    # acima da janela
            code |= self.TOP
        return code

    def cohen_sutherland_clip(self,x1, y1, x2, y2):
        code1 = self.compute_code(x1, y1)
        code2 = self.compute_code(x2, y2)
        accept = False

        while True:
            if code1 == 0 and code2 == 0:
                # Ambos os pontos estão dentro da janela
                accept = True
                break
            elif (code1 & code2) != 0:
                # Ambos os pontos compartilham uma região fora da janela
                break
            else:
                # Pelo menos um ponto está fora da janela
                # Escolhe o ponto que está fora da janela
                if code1 != 0:
                    code_out = code1
                else:
                    code_out = code2

                x = 0
                y = 0
                # Encontra o ponto de interseção
                if code_out & self.TOP:
                    x = x1 + (x2 - x1) * (self.y_max - y1) / (y2 - y1)
                    y = self.y_max
                elif code_out & self.BOTTOM:
                    x = x1 + (x2 - x1) * (self.y_min - y1) / (y2 - y1)
                    y = self.y_min
                elif code_out & self.RIGHT:
                    y = y1 + (y2 - y1) * (self.x_max - x1) / (x2 - x1)
                    x = self.x_max
                elif code_out & self.LEFT:
                    y = y1 + (y2 - y1) * (self.x_min - x1) / (x2 - x1)
                    x = self.x_min

                # Atualiza o ponto fora da janela
                if code_out == code1:
                    x1, y1 = x, y
                    code1 = self.compute_code(x1, y1)
                else:
                    x2, y2 = x, y
                    code2 = self.compute_code(x2, y2)

        return accept

    # Exemplo de uso
    #cohen_sutherland_clip(5, 5, 150, 100)
    #cohen_sutherland_clip(50, 50, 250, 250)
