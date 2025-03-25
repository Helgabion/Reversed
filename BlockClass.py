import pygame
import constant

class Block(object):
    def __init__(self, game, color):
        #tal vez puedo quitar el rect y las coords?
        self.game = game
        self.color = color
        
class Normal(Block):
    def __init__(self, game, color):
        super().__init__(game, color)
        self.sprite = self.game.assets.blocks['Normal']

    def __copy__(self):
        return Normal(self.game, self.color)


class Bomb(Block):
    def __init__(self, game, color):
        super().__init__(game, color)
        self.sprite = self.game.assets.blocks['Bomb']

    def __copy__(self):
        return Bomb(self.game, self.color)

class Tornado(Block):
    def __init__(self, game, color):
        super().__init__(game, color)
        self.sprite = self.game.assets.blocks['Tornado']
    
    def __copy__(self):
        return Tornado(self.game, self.color)


class Freeze(Block):
    def __init__(self, game, color):
        super().__init__(game, color)
        self.sprite = self.game.assets.blocks['Freeze']

    def __copy__(self):
        return Freeze(self.game, self.color)


class Solid(Block):
    def __init__(self, game, color):
        super().__init__(game, color)
        self.sprite = self.game.assets.blocks['Solid']

    def __copy__(self):
        return Solid(self.game, self.color)

