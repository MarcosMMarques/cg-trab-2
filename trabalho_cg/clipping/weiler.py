from geometry.geometry import Polygon, Point
from window import Window

class WeilerAtherton:
    
    def __init__(self, window: Window):
        self.window = window
    
    def is_inside(self, p, edge):
        return (edge[1][0] - edge[0][0]) * (p.getPoint()[1] - edge[0][1]) > (edge[1][1] - edge[0][1]) * (p.getPoint()[0] - edge[0][0])

    def compute_intersection(self, p1, p2, q1, q2):
        A1 = p2.getPoint()[1] - p1.getPoint()[1]
        B1 = p1.getPoint()[0] - p2.getPoint()[0]
        C1 = A1 * p1.getPoint()[0] + B1 * p1.getPoint()[1]

        A2 = q2[1] - q1[1]
        B2 = q1[0] - q2[0]
        C2 = A2 * q1[0] + B2 * q1[1]

        det = A1 * B2 - A2 * B1

        if det == 0:
            return None
        else:
            x = (B2 * C1 - B1 * C2) / det
            y = (A1 * C2 - A2 * C1) / det
            return Point((x, y))

    def weiler_atherton(self, subject_polygon: Polygon):
        output_list = subject_polygon.getPolygon()

        # Define the clipping window as a list of edges (pair of points)
        window_edges = [
            [(self.window.getXwMin(), self.window.getYwMin()), (self.window.getXwMax(), self.window.getYwMin())],  # Bottom edge
            [(self.window.getXwMax(), self.window.getYwMin()), (self.window.getXwMax(), self.window.getYwMax())],  # Right edge
            [(self.window.getXwMax(), self.window.getYwMax()), (self.window.getXwMin(), self.window.getYwMax())],  # Top edge
            [(self.window.getXwMin(), self.window.getYwMax()), (self.window.getXwMin(), self.window.getYwMin())]   # Left edge
        ]

        for edge in window_edges:
            input_list = output_list
            output_list = []

            if len(input_list) == 0:
                break

            S = input_list[-1]

            for E in input_list:
                if self.is_inside(E, edge):
                    if not self.is_inside(S, edge):
                        intersection_point = self.compute_intersection(S, E, edge[0], edge[1])
                        if intersection_point:
                            output_list.append(intersection_point)
                    output_list.append(E)
                elif self.is_inside(S, edge):
                    intersection_point = self.compute_intersection(S, E, edge[0], edge[1])
                    if intersection_point:
                        output_list.append(intersection_point)
                S = E

        # Convert output list to a Polygon object
        clipped_polygon = Polygon(*output_list)
        return clipped_polygon

# Example usage:
# window = Window(100, 300, 100, 300)
# subject_polygon = Polygon(
#     Point((50, 150)), Point((200, 50)), Point((350, 150)),
#     Point((350, 300)), Point((250, 300)), Point((200, 250)),
#     Point((150, 350)), Point((100, 250)), Point((100, 200))
# )

# weiler_atherton_clip = WeilerAtherton(window)
# clipped_polygon = weiler_atherton_clip.weiler_atherton(subject_polygon)
# print("Clipped polygon points:", [p.getPoint() for p in clipped_polygon.getPolygon()])
