from collections import deque
import pygame as pg
from ui.const import *
from ui.Hexagon import *   
class Board():
    def __init__(self, surface, size):
        self.surface = surface
        self.TILES = size
        self.HEXRADIUS = H/(20 + self.TILES*2)
        #Khởi tạo toạ độ board
        self.coordinate = [[0 for i in range(self.TILES)] for j in range(self.TILES)]
        #Danh sách các ô trong board
        self.listHexagon = []
        #Danh sách các ô giáp đường viền đỏ
        self.redBorder = []
        #Danh sách các ô giáp đường viền xanh
        self.blueBorder = []
        self.PLAYER = 1

    def drawRect(self, surface, pos, height, boardSize):
        """Vẽ đường viền cho board"""
        x, y = pos
        pg.draw.polygon(surface, RED, [(x,y), (x, y+height), (x+height-height/boardSize, y+height/2), (x+height-height/boardSize ,y+height/2+height)])
        pg.draw.polygon(surface, BLUE, [(x,y), (x+height-height/boardSize, y+height/2), (x, y+height), (x+height-height/boardSize, y+height/2+height)])

    def createBoard(self):   
        """Tạo board"""
        x, y = STARTPOS
        for i in range(self.TILES):
            distance = 0
            for j in range(self.TILES):
                self.coordinate[i][j] = Hexagon(self.HEXRADIUS, (x, y+distance))
                distance += self.coordinate[i][j].minimalRadius * 2
                self.listHexagon.append(self.coordinate[i][j])
                if i == self.TILES-1:
                    self.redBorder.append(self.coordinate[i][j])
                if j == self.TILES-1:
                    self.blueBorder.append(self.coordinate[i][j])
            x, y = self.coordinate[i][0].findNextPoint()

    def resetBoard(self):
        """Reset trạng thái board"""
        for hexagon in self.listHexagon:
            hexagon.state = 0

    def showBoard(self):
        """Vẽ board ra màn hình"""
        x, y = STARTPOS
        self.drawRect(self.surface,(x-2*self.coordinate[0][0].minimalRadius, y - 4 * self.coordinate[0][0].minimalRadius), self.coordinate[0][0].minimalRadius * (self.TILES+2) * 2, self.TILES)
        for col in range(self.TILES):
            for row in range(self.TILES):
                if self.coordinate[col][row].state == 0:
                    self.coordinate[col][row].fillHexagon(self.surface, WHITE)
                    self.coordinate[col][row].render(self.surface)
                    if self.coordinate[col][row].inHexagon(pg.mouse.get_pos()):
                        if self.PLAYER == 1 :
                            self.coordinate[col][row].fillHexagon(self.surface, RED)
                            self.coordinate[col][row].render(self.surface)
                        else:
                            self.coordinate[col][row].fillHexagon(self.surface, BLUE)
                            self.coordinate[col][row].render(self.surface)
                elif self.coordinate[col][row].state == 1:
                    self.coordinate[col][row].fillHexagon(self.surface, RED)
                    self.coordinate[col][row].render(self.surface)
                else:
                    self.coordinate[col][row].fillHexagon(self.surface, BLUE)
                    self.coordinate[col][row].render(self.surface)

    def capture(self, sound):
        """Khi người chơi click vào 1 ô trắng thì ô sẽ chuyển màu thành màu của ng chơi đó"""
        for col in range(self.TILES):
            for row in range(self.TILES):
                if self.coordinate[col][row].inHexagon(pg.mouse.get_pos())\
                    and self.coordinate[col][row].state == 0:
                        if self.PLAYER == 1:
                            pg.mixer.Sound.play(sound)
                            self.coordinate[col][row].captured(self.PLAYER)
                            print("Red capture ("+str(col)+","+str(row)+")")
                        else:
                            pg.mixer.Sound.play(sound)
                            self.coordinate[col][row].captured(self.PLAYER)
                            print("Blue capture ("+str(col)+","+str(row)+")")
                        self.PLAYER = 3 - self.PLAYER
    
    def DFS(self, start, finish, player):
        """Thuật toán tìm theo chiều sâu"""
        stack = deque()
        stack.append(start)
        visited = []
        while len(stack):
            current = stack.pop()
            for hexagon in finish:
                if current is hexagon:
                    return True
            visited.append(current)
            listNeighbour = current.findAllNeighbour(self.listHexagon)
            for hexagon in listNeighbour:
                if hexagon not in visited and hexagon.state == player:
                    stack.append(hexagon)
        return False
    
    def checkWin(self):
        """TÌm người chiến thắng bằng thuật toán DFS"""
        for row in range(self.TILES):
            if self.coordinate[0][row].state == 1:
                if self.DFS(self.coordinate[0][row], self.redBorder, 1):
                    return 1
        for col in range(self.TILES):
            if self.coordinate[col][0].state == 2:
                if self.DFS(self.coordinate[col][0], self.blueBorder, 2):
                    return 2
        return 0