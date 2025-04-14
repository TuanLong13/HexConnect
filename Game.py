import sys
import pygame as pg
from os import path
from pygame.locals import QUIT
from ui.const import *
from ui.Board import *
from ui.TextButton import *

class Game:
    board: Board
    tiles = 11
    def __init__(self):
        pg.init()
        pg.display.set_caption('Hex game')
        self.clock = pg.time.Clock()
        self.screen = pg.display.set_mode((W, H))
        #Tạo đường dẫn đến thư mục other
        file_path = path.join(path.dirname(__file__), "other")
        #Load background
        self.background = pg.image.load(path.join(file_path, "bg1.jpg")).convert_alpha()
        #Load tiếng động khi click
        self.clickSound = pg.mixer.Sound(path.join(file_path, "click.wav"))
        self.started = False
            
    def startScreen(self):
        """Màn hình bắt đầu"""
        start = True
        title = TextButton(self.screen, "HEX GAME", (W/2, H/4), 100, GOLD)
        startGame = TextButton(self.screen, "Bắt đầu chơi", (W/2, H/2), 60, WHITE)
        rule = TextButton(self.screen, "Luật chơi", (W/2, H - H/2 + 100), 60, RED)
        setting = TextButton(self.screen, "Tuỳ chỉnh", (W/2, H - H/2 + 200), 60, BLUE)
        buttons = [startGame, rule, setting]
        while start:
            self.screen.fill(WHITE)
            self.screen.blit(self.background, (0, 0))
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == QUIT:
                    pg.quit()
                    sys.exit()    
                if event.type == pg.MOUSEBUTTONDOWN:
                    if startGame.click():
                        pg.mixer.Sound.play(self.clickSound)
                        self.started = True
                        start = False
                        self.board = Board(self.screen, self.tiles)
                        self.board.createBoard()
                        return True
                    elif rule.click():
                        pg.mixer.Sound.play(self.clickSound)
                        self.ruleScreen()
                        return True
                    elif setting.click():
                        pg.mixer.Sound.play(self.clickSound)
                        self.settingScreen()
                        return True
            title.printText(100)
            for b in buttons:
                b.render()
            pg.display.flip()

    def ruleScreen(self):
        """Màn hình luật chơi"""
        rule = True
        title = TextButton(self.screen, "Luật chơi", (W/2, H/5), 60, RED)
        line1 = TextButton(self.screen, "2 người chơi thay phiên nhau chọn 1", (W/2, H/3), 30, WHITE)
        line2 = TextButton(self.screen, " ô trắng trên board để chiếm đóng.", (W/2, H/3 + 50), 30, WHITE)
        line3 = TextButton(self.screen, "Người chơi nào tạo được 1 đường liên kết", (W/2, H/3 + 100), 30, WHITE)
        line4 = TextButton(self.screen, "2 cạnh đối diện nhau có màu đường viền", (W/2, H/3 + 150), 30, WHITE)
        line5 = TextButton(self.screen, "ứng với màu của người chơi đó sẽ là người chiến thắng", (W/2, H/3 + 200), 30, WHITE)
        back = TextButton(self.screen, "Quay lại", (W/8, H - H/15), 60, WHITE)
        text = [line1, line2, line3, line4, line5]
        while rule:
            self.clock.tick(FPS)
            self.screen.fill(WHITE)
            self.screen.blit(self.background, (0, 0))
            for event in pg.event.get():
                if event.type == QUIT:
                    pg.quit()
                    sys.exit()    
                if event.type == pg.MOUSEBUTTONDOWN:
                    if back.click():
                        pg.mixer.Sound.play(self.clickSound)
                        self.started = False
                        rule = False
            for t in text:
                t.printText(30)
            title.printText(80)
            back.render()
            pg.display.flip()
    
    def settingScreen(self):
        """Màn hình tuỳ chỉnh"""
        setting = True
        title = TextButton(self.screen, "Tuỳ chỉnh", (W/2, H/5), 100, BLUE)
        up = TextButton(self.screen, "^", (W/3, H/2-50), 100, GOLD)
        down = TextButton(self.screen, "^", (W/3, H/2+50), 100, GOLD)
        size = TextButton(self.screen, self.tiles, (W/2, H/2), 80, GOLD)
        tile = TextButton(self.screen, "Ô", (W/2+100, H/2), 80, GOLD)
        back = TextButton(self.screen, "Quay lại", (W/8, H - H/15), 60, WHITE)
        button = [up, back]
        text = [size, tile]
        while setting:
            self.clock.tick(FPS)
            self.screen.fill(WHITE)
            self.screen.blit(self.background, (0, 0))
            for event in pg.event.get():
                if event.type == QUIT:
                    pg.quit()
                    sys.exit()    
                if event.type == pg.MOUSEBUTTONDOWN:
                    if back.click():
                        pg.mixer.Sound.play(self.clickSound)
                        self.started = False
                        setting = False
                        return False
                    elif up.click():
                        pg.mixer.Sound.play(self.clickSound)
                        self.tiles = min(14, self.tiles+1)
                        size.text = self.tiles
                    elif down.click():
                        pg.mixer.Sound.play(self.clickSound)
                        self.tiles = max(8, self.tiles-1)
                        size.text = self.tiles
            for b in button:
                b.render()
            down.renderFlip()
            for t in text:
                t.printText(80)
            title.printText(100)
            pg.display.flip()


    def playScreen(self):
        """Màn hình chơi"""
        play = True
        pause = TextButton(self.screen, "||", (W/12, H/15), 40, WHITE)
        while play:
            self.clock.tick(FPS)
            self.screen.fill(WHITE)
            self.screen.blit(self.background, (0, 0))
            for event in pg.event.get():
                if event.type == QUIT:
                    pg.quit()
                    sys.exit()    
                if event.type == pg.MOUSEBUTTONDOWN:
                    self.board.capture(self.clickSound)
                    if pause.click():
                        pg.mixer.Sound.play(self.clickSound)
                        self.pauseScreen()
                        return True
            pause.render()
            self.board.showBoard()
            if  self.board.checkWin() == 1:
                self.winScreen("Player 1 win", RED)
                play = False
            if  self.board.checkWin() == 2:
                self.winScreen("Player 2 win", BLUE)
                play = False
            pg.display.flip()
        

    def shadow(self):
        """Đổ bóng cho màn hình"""
        shadow = pg.Surface((W, H))
        shadow.set_alpha(200)
        self.screen.blit(shadow, (0, 0))

    def pauseScreen(self):
        """Màn hình tạm dừng"""
        pause = True
        cont = TextButton(self.screen, "Tiếp tục", (W/2, H/3), 80, GOLD)
        back = TextButton(self.screen, "Quay về", (W/2, H/2), 80, GOLD)
        buttons = [cont, back]
        while pause:
            for event in pg.event.get():
                if event.type == QUIT:
                    pg.quit()
                    sys.exit()    
                if event.type == pg.MOUSEBUTTONDOWN:
                    if cont.click():
                        pg.mixer.Sound.play(self.clickSound)
                        self.screen.fill(WHITE)
                        self.screen.blit(self.background, (0, 0))
                        return True
                    elif back.click():
                        pg.mixer.Sound.play(self.clickSound)
                        self.started = False
                        self.board.resetBoard()
                        return False    
            self.screen.blit(self.background, (0, 0))
            self.board.showBoard()
            self.shadow()
            for b in buttons:
                b.render()
            pg.display.flip()
    
    def winScreen(self, txt, color):
        """Màn hình thông báo người chiến thắng"""
        win = True
        winner = TextButton(self.screen, txt, (W/2, H/10), 80, color)
        back = TextButton(self.screen, "Quay lại", (W/8, H - H/15), 60, WHITE)
        while win:
            self.clock.tick(FPS)
            self.screen.fill(WHITE)
            self.screen.blit(self.background, (0, 0))
            self.board.showBoard()
            self.shadow()
            for event in pg.event.get():
                if event.type == QUIT:
                    pg.quit()
                    sys.exit()    
                if event.type == pg.MOUSEBUTTONDOWN:
                    if back.click():
                        pg.mixer.Sound.play(self.clickSound)
                        self.started = False
                        win = False
                        self.board.resetBoard()
                        return True
            winner.printText(80)
            back.render()
            pg.display.flip()
        