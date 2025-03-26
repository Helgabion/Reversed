import constant
import pygame
from random import randrange
from copy import deepcopy


class Level(object):
    def __init__(self, game, is_random, dificulty, colors_L=None, colors_R=None, layout_L=None, layout_R=None, pattern_list=None):
        self.game = game
        self.background = game.assets.backgrounds['Temp']
        self.current_background = 0
        self.is_random = is_random

        self.pattern_block = game.assets.blocks['Pattern'][0]

        self.state = []
        self.used_patterns = []

        if self.is_random:
            
            self.move_number = dificulty[0]
            self.block_number = dificulty[1]
            self.grid_size = dificulty[2]

            self.colors_L = []
            self.colors_R = []

            self.layout_L = []
            self.layout_R = []

            color_row = [0 for i in range(self.grid_size)]
            layout_row_L = ['N' for i in range(self.grid_size)]
            layout_row_R = ['S' for i in range(self.grid_size)]
            for i in range(self.grid_size):
                self.colors_L.append(color_row)
                self.colors_R.append(color_row)
                self.layout_L.append(layout_row_L)
                self.layout_R.append(layout_row_R)
            self.pattern_list = []
        else:

            self.colors_L = colors_L
            self.colors_R = colors_R

            self.layout_L = layout_L
            self.layout_R = layout_R

            self.pattern_list = pattern_list
            
            self.grid_size = len(self.colors_L)

            

    def load(self):
        self.blocks_L = []
        
        x = y = 0
        for row in self.layout_L:
            self.blocks_L.append([])
            for col in row:
                self.blocks_L[y].append([col,self.colors_L[y][x]])
                x += 1
            y += 1
            x = 0

        self.blocks_R = []

        x = y = 0
        for row in self.layout_R:
            self.blocks_R.append([])
            for col in row:
                self.blocks_R[y].append([col,self.colors_R[y][x]])
                x += 1
            y += 1
            x = 0
        
        if self.is_random:

            self.grid_size = len(self.colors_L)
            
            self.pattern_list = []
            rand_pattern_list = [[[1]],[[0,1,0],[1,1,1],[0,1,0]],[[1,1,1],[1,1,1],[1,1,1]]]
            for i in range(self.move_number):
                randint = randrange(len(rand_pattern_list))
                self.pattern_list.append(rand_pattern_list[randint])

            aux_pattern_list = deepcopy(self.pattern_list)
            
            block_list = ['B']
            for i in range(self.block_number):
                randx = randrange(self.grid_size)
                randy = randrange(self.grid_size)
                randint = randrange(len(block_list))
                self.blocks_L[randx][randy][0] = block_list[randint]
                
            aux_block_list = deepcopy(self.blocks_L)

            for i in range(self.move_number):
                randx = randrange(self.grid_size)
                randy = randrange(self.grid_size)
                print([randx,randy])
                self.click([randx,randy])

            self.pattern_list = aux_pattern_list
            for x in range(self.grid_size):
                for y in range(self.grid_size):
                    self.blocks_L[x][y][0] = aux_block_list[x][y][0]

            current_state = deepcopy(self.blocks_L)
            self.state = []
            self.state.append(current_state)
        else:
            
            current_state = deepcopy(self.blocks_L)
            self.state.append(current_state)
            
   

    def block_sprite(self, block, color):
        if block == 'N':
            return self.game.assets.blocks['Normal'][color]
        elif block == 'B':
            return self.game.assets.blocks['Bomb'][color]
        elif block == 'T':
            return self.game.assets.blocks['Tornado'][color]
        elif block == 'F':
            return self.game.assets.blocks['Freeze'][color]
        elif block == 'S':
            return self.game.assets.blocks['Solid'][color]

    def draw(self):
        self.game.screen.blit(self.background[self.current_background], (0,0))

        for x in range(self.grid_size):
            for y in range(self.grid_size):
                sprite = self.block_sprite(self.blocks_L[x][y][0],self.blocks_L[x][y][1])
                self.game.screen.blit(pygame.transform.scale(sprite, (constant.SQUARE_SIZE,constant.SQUARE_SIZE)), (y*constant.SQUARE_SIZE, x*constant.SQUARE_SIZE))

        for x in range(self.grid_size):
            for y in range(self.grid_size):
                sprite = self.block_sprite(self.blocks_R[x][y][0],self.blocks_R[x][y][1])
                self.game.screen.blit(pygame.transform.scale(sprite, (constant.SQUARE_SIZE,constant.SQUARE_SIZE)), ((y+self.grid_size)*constant.SQUARE_SIZE + 100, x*constant.SQUARE_SIZE))

        for i in range(len(self.pattern_list)):
            for x in range(len(self.pattern_list[i])):
                for y in range(len(self.pattern_list[i])):
                    if self.pattern_list[i][x][y]:
                        self.game.screen.blit(pygame.transform.scale(self.pattern_block, (constant.SQUARE_SIZE//2,constant.SQUARE_SIZE//2)), [(y-len(self.pattern_list[i])//2)*constant.SQUARE_SIZE//2 + i*5*constant.SQUARE_SIZE//2 + 100, ((x-len(self.pattern_list[i])//2)+self.grid_size*2)*constant.SQUARE_SIZE//2 + 100])



    def click(self, coords):
        pattern = self.pattern_list.pop(0)
        self.used_patterns.append(pattern)
        for x in range(len(pattern[0])):
            for y in range(len(pattern[0])):
                if pattern[y][x]:
                    self.flip([coords[0]+x-len(pattern[0])//2,coords[1]+y-len(pattern[0])//2])


        current_state = deepcopy(self.blocks_L)
        self.state.append(current_state)
        
        if self.check_puzzle():
            self.current_background = 1

    def backtrack(self):
        if len(self.state) > 1:
            self.state.pop()
            self.blocks_L = deepcopy(self.state[-1])
            self.pattern_list.insert(0, self.used_patterns.pop())


    def activate_bomb(self, coords):
        for i in range(self.grid_size-1):
            self.flip([(coords[0] + i+1) % self.grid_size,coords[1]])
            self.flip([coords[0],(coords[1] + i+1) % self.grid_size])

    def activate_tornado(self, coords):
        aux = self.blocks_L[coords[1]-1][coords[0]-1]
        self.blocks_L[coords[1]-1][coords[0]-1] = self.blocks_L[coords[1]+1][coords[0]-1]
        self.blocks_L[coords[1]+1][coords[0]-1] = self.blocks_L[coords[1]+1][coords[0]+1]
        self.blocks_L[coords[1]+1][coords[0]+1] = self.blocks_L[coords[1]-1][coords[0]+1]
        self.blocks_L[coords[1]-1][coords[0]+1] = aux

        aux = self.blocks_L[coords[1]-1][coords[0]]
        self.blocks_L[coords[1]-1][coords[0]] = self.blocks_L[coords[1]][coords[0]-1]
        self.blocks_L[coords[1]][coords[0]-1] = self.blocks_L[coords[1]+1][coords[0]]
        self.blocks_L[coords[1]+1][coords[0]] = self.blocks_L[coords[1]][coords[0]+1]
        self.blocks_L[coords[1]][coords[0]+1] = aux
               

    def activate_freeze(self, coords):
        for i in [-1,0,1]:
            for j in [-1,0,1]:
                if coords[0]+i in range(self.grid_size) and coords[1]+j in range(self.grid_size):
                    self.blocks_L[coords[1]+j][coords[0]+i][0] = 'S'


    def flip(self, coords):
        if coords[1] in range(self.grid_size) and coords[0] in range(self.grid_size):
            block = self.blocks_L[coords[1]][coords[0]][0]

            #normal
            if block == 'N':
                self.blocks_L[coords[1]][coords[0]][1] = 1 - self.blocks_L[coords[1]][coords[0]][1]

            # #bombas
            elif block == 'B':
                self.blocks_L[coords[1]][coords[0]][1] = 1 - self.blocks_L[coords[1]][coords[0]][1]

                self.blocks_L[coords[1]][coords[0]][0] = 'N'

                self.activate_bomb(coords)

            #tornados
            elif block == 'T':
                
                self.blocks_L[coords[1]][coords[0]][1] = 1 - self.blocks_L[coords[1]][coords[0]][1]
                self.blocks_L[coords[1]][coords[0]][0] = 'N'

                self.activate_tornado(coords)

            #freezes
            elif block == 'F':
                self.blocks_L[coords[1]][coords[0]][1] = 1 - self.blocks_L[coords[1]][coords[0]][1]

                #esto lo hago en activate_freeze()
                # self.blocks_L[coords[1]][coords[0]][0] = 'S'

                self.activate_freeze(coords)

    def check_puzzle(self):
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                if self.blocks_L[x][y][1] != self.blocks_R[x][y][1]:
                    return False
                    
        return True












