import pygame as pg
from Game import *

game = Game()
while True:
    if not game.started:
        game.startScreen()
    else:
        game.playScreen()
        
    pg.display.flip()
