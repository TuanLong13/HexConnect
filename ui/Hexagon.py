import math
from ui.const import *
import pygame as pg
from pygame import gfxdraw
class Hexagon:
    def __init__(self, radius, position) -> None:
        """Khởi tạo lục giác"""
        self.radius = radius  #Bán kính từ tâm đường tròn ngoại tiếp đến các đỉnh
        self.position = position    #Vị trí vẽ lục giác
        self.minimalRadius = math.cos(math.radians(30)) * radius #Bán kính đường tròn nội tiếp
        self.vertices = self.computeVertices() #Lấy về 1 list các tuple chứa toạ độ của các đỉnh
        self.centre = self.findCentre()
        self.state = 0 #Biến lưu trạng thái của lục giác(0: WHITE, 1: RED, 2: BLUE)
    def computeVertices(self):
        """Tìm list các tuple chứa toạ độ các đỉnh lục giác"""
        x, y = self.position
        halfRadius = self.radius / 2
        return [ (x,y), 
                     (x + halfRadius, y + self.minimalRadius),
                     (x + 3 * halfRadius, y + self.minimalRadius),
                     (x + 4 * halfRadius, y),
                     (x + 3 * halfRadius, y - self.minimalRadius),
                     (x + halfRadius, y - self.minimalRadius) ]
    def findCentre(self):
        """Trả về tuple toạ độ tâm lục giác"""
        x, y = self.position
        return (x + self.radius, y)
    def findNextPoint(self):
        """Trả về toạ độ đỉnh bắt đầu vẽ của lục giác tiếp theo (toạ độ đỉnh góc phải dưới)"""
        return self.vertices[2]
    def inHexagon(self, point):
        """"Kiểm tra đỉnh có nằm trong lục giác hay không"""
        distance = math.dist(self.centre, point)
        return distance < self.minimalRadius
    def render(self, screen):
        """Vẽ lục giác lên màn hình"""
        pg.draw.polygon(screen, BLACK, self.vertices, 5)
    def fillHexagon(self, screen, color):
        """Tô màu lục giác"""
        gfxdraw.filled_polygon(screen, self.vertices, color)
        self.color = color
    def captured(self, player):
        """Đánh dấu đã được chọn"""
        self.state = player
    def compareCentre(self, point):
        """So sánh tâm lục giác"""
        x, y = self.centre
        a, b = point
        return x == a and y == b
    def findAllNeighbour(self, listHex):
        """Tìm list các lục giác kế cạnh"""
        neighbour = []
        for hexagon in listHex:
            distance = math.dist(self.centre, hexagon.centre)
            if math.isclose(distance, 2*self.minimalRadius, rel_tol=0.05):
                neighbour.append(hexagon)
        return neighbour

