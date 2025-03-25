import BlockClass
import constant
import pygame
from functions import object_copy



class Level(object):
    def __init__(self, game, colors_L, colors_R, layout_L, layout_R, pattern_list):
        self.game = game
        self.background = game.assets.backgrounds['Temp']
        self.current_background = 0

        self.colors_L = colors_L
        self.colors_R = colors_R

        self.layout_L = layout_L
        self.layout_R = layout_R

        self.grid_size = len(self.colors_L)

        self.pattern_list = pattern_list
        self.pattern_block = game.assets.blocks['Pattern'][0]

        self.state = []
        self.used_patterns = []

    def load(self):
        self.blocks_L = []
        
        x = y = 0
        for row in self.layout_L:
            self.blocks_L.append([])
            for col in row:
                if col == 'B':
                    self.blocks_L[y].append(BlockClass.Bomb(self.game, self.colors_L[x][y]))
                elif col == 'T':
                    self.blocks_L[y].append(BlockClass.Tornado(self.game, self.colors_L[x][y]))
                elif col == 'F':
                    self.blocks_L[y].append(BlockClass.Freeze(self.game, self.colors_L[x][y]))
                elif col == 'S':
                    self.blocks_L[y].append(BlockClass.Solid(self.game, self.colors_L[x][y]))
                else:
                    self.blocks_L[y].append(BlockClass.Normal(self.game, self.colors_L[x][y]))
                x += 1
            y += 1
            x = 0
 
        self.blocks_R = []

        x = self.grid_size
        y = 0
        for row in self.layout_R:
            self.blocks_R.append([])
            for col in row:
                if col == 'B':
                    self.blocks_R[y].append(BlockClass.Bomb(self.game, self.colors_R[x-self.grid_size][y]))
                elif col == 'T':
                    self.blocks_R[y].append(BlockClass.Tornado(self.game, self.colors_R[x-self.grid_size][y]))
                elif col == 'F':
                    self.blocks_R[y].append(BlockClass.Freeze(self.game, self.colors_R[-self.grid_size][y]))
                elif col == 'S':
                    self.blocks_R[y].append(BlockClass.Solid(self.game, self.colors_R[x-self.grid_size][y]))
                else:
                    self.blocks_R[y].append(BlockClass.Normal(self.game, self.colors_R[x-self.grid_size][y]))
                x += 1
            y += 1
            x = self.grid_size
        
        current_state = []
        for x in range(self.grid_size):
            current_state.append([])
            for y in range(self.grid_size):
                block = object_copy(self.blocks_L[x][y], {'game' : self.game, 'color' : self.blocks_L[x][y].color})
                current_state[x].append(block)
        
        self.state.append(current_state)
        

    def draw(self):
        self.game.screen.blit(self.background[self.current_background], (0,0))

        for x in range(self.grid_size):
            for y in range(self.grid_size):
                self.game.screen.blit(pygame.transform.scale(self.blocks_L[x][y].sprite[self.blocks_L[x][y].color], (constant.SQUARE_SIZE,constant.SQUARE_SIZE)), (y*constant.SQUARE_SIZE, x*constant.SQUARE_SIZE))

        for x in range(self.grid_size):
            for y in range(self.grid_size):
                self.game.screen.blit(pygame.transform.scale(self.blocks_R[x][y].sprite[self.blocks_R[x][y].color], (constant.SQUARE_SIZE,constant.SQUARE_SIZE)), ((y+self.grid_size)*constant.SQUARE_SIZE + 100, x*constant.SQUARE_SIZE))

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

        current_state = []
        for x in range(self.grid_size):
            current_state.append([])
            for y in range(self.grid_size):
                block = object_copy(self.blocks_L[x][y], {'game' : self.game, 'color' : self.blocks_L[x][y].color})
                current_state[x].append(block)
        self.state.append(current_state)
        
        if self.check_puzzle():
            self.current_background = 1

    def backtrack(self):
        if len(self.state) > 1:
            self.state.pop()
            self.blocks_L = self.state[-1].copy()
            self.pattern_list.insert(0, self.used_patterns.pop())

            # current_state = []
            # for x in range(self.grid_size):
            #     current_state.append([])
            #     for y in range(self.grid_size):
            #         block = self.blocks_L[x][y].copy()
            #         current_state[x].append(block)
            # self.state.append(current_state)


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
        self.blocks_L[coords[1]+1][coords[0]] = BlockClass.Solid(self.game,[coords[0]+1,coords[1]], self.blocks_L[coords[1]+1][coords[0]].color)
        self.blocks_L[coords[1]-1][coords[0]] = BlockClass.Solid(self.game,[coords[0]-1,coords[1]], self.blocks_L[coords[1]-1][coords[0]].color)
        self.blocks_L[coords[1]][coords[0]+1] = BlockClass.Solid(self.game,[coords[0],coords[1]+1], self.blocks_L[coords[1]][coords[0]+1].color)
        self.blocks_L[coords[1]][coords[0]-1] = BlockClass.Solid(self.game,[coords[0],coords[1]-1], self.blocks_L[coords[1]][coords[0]-1].color)
        self.blocks_L[coords[1]+1][coords[0]+1] = BlockClass.Solid(self.game,[coords[0]+1,coords[1]+1], self.blocks_L[coords[1]+1][coords[0]+1].color)
        self.blocks_L[coords[1]+1][coords[0]-1] = BlockClass.Solid(self.game,[coords[0]+1,coords[1]-1], self.blocks_L[coords[1]+1][coords[0]-1].color)
        self.blocks_L[coords[1]-1][coords[0]+1] = BlockClass.Solid(self.game,[coords[0]-1,coords[1]+1], self.blocks_L[coords[1]-1][coords[0]+1].color)
        self.blocks_L[coords[1]-1][coords[0]-1] = BlockClass.Solid(self.game,[coords[0]-1,coords[1]-1], self.blocks_L[coords[1]-1][coords[0]-1].color)


    def flip(self, coords):
        if coords[1] in range(self.grid_size) and coords[0] in range(self.grid_size):
            block = self.blocks_L[coords[1]][coords[0]]

            #normal
            if type(block) == BlockClass.Normal:
                block.color = 1 - block.color

            # #bombas
            if type(block) == BlockClass.Bomb:
                block.color = 1 - block.color

                self.blocks_L[coords[1]][coords[0]] = BlockClass.Normal(self.game, block.color)

                self.activate_bomb(coords)

            #tornados
            elif type(block) == BlockClass.Tornado:
                
                block.color = 1 - block.color
                self.blocks_L[coords[1]][coords[0]] = BlockClass.Normal(self.game, block.color)

                self.activate_tornado(coords)

            #freezes
            elif type(block) == BlockClass.Freeze:
                block.color = 1 - block.color
                self.blocks_L[coords[1]][coords[0]] = BlockClass.Solid(self.game, block.color)

                self.activate_freeze(coords)

    def check_puzzle(self):
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                if self.blocks_L[x][y].color != self.blocks_R[x][y].color:
                    return False
                    
        return True












