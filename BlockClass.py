import pygame
import constant

class Block(object):
    def __init__(self, game, coords, color):
        #tal vez puedo quitar el rect y las coords?
        self.game = game
        self.coords = coords
        self.rect = pygame.Rect(self.coords[0] * constant.SQUARE_SIZE, self.coords[1] * constant.SQUARE_SIZE, constant.SQUARE_SIZE, constant.SQUARE_SIZE)
        self.color = color
        

class Normal(Block):
    def __init__(self, game, coords, color):
        super().__init__(game, coords, color)
        self.sprite = self.game.assets.blocks['Normal']

class Bomb(Block):
    def __init__(self, game, coords, color):
        super().__init__(game, coords, color)
        self.sprite = self.game.assets.blocks['Bomb']

class Tornado(Block):
    def __init__(self, game, coords, color):
        super().__init__(game, coords, color)
        self.sprite = self.game.assets.blocks['Tornado']

class Freeze(Block):
    def __init__(self, game, coords, color):
        super().__init__(game, coords, color)
        self.sprite = self.game.assets.blocks['Freeze']

class Solid(Block):
    def __init__(self, game, coords, color):
        super().__init__(game, coords, color)
        self.sprite = self.game.assets.blocks['Solid']
