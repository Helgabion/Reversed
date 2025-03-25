import pygame
from pygame.locals import VIDEOEXPOSE, VIDEORESIZE, RESIZABLE
import constant
from AssetsClass import Assets
from LevelClass import Level

class Game(object):
    def __init__(self):
        pygame.init()
        
        #screen is where i draw things
        self.screen = pygame.display.set_mode((constant.DISPLAY_WIDTH, constant.DISPLAY_HEIGHT))

        #display is where i draw the screen at the end
        self.display = pygame.display.set_mode((constant.DISPLAY_WIDTH, constant.DISPLAY_HEIGHT), RESIZABLE)
        pygame.display.set_caption('Reversed')
        
        self.clock = pygame.time.Clock()

        self.assets = Assets()

        self.level_test = Level(self, [[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]], [[1,1,1,1,1],[1,1,1,1,1],[1,1,1,1,1],[1,1,1,1,1],[1,1,1,1,1]], ["NNNNN","NNTFN","NNBNN","NNNNN","NNNNN"], ["SSSSS","SSSSS","SSSSS","SSSSS","SSSSS"])
        # self.level_test = Level(self, [[0,0],[0,0]], [[0,0],[0,0]], ["FN","NN"], ["NN","NN"])
        # self.level_test = Level(self, [[0,0,0],[0,0,0],[0,0,0]], [[0,0,0],[0,0,0],[0,0,0]], ["BNT","NTN","NNF"], ["NNN","NNN","NNN"])

        self.level_test.load()
        self.mouse_position = [0,0]

        self.running = True

    def update_display(self):
        self.display.blit(pygame.transform.scale(self.screen,self.display.get_size()),(0,0))
        pygame.display.update()

    


game = Game()

while game.running:
    game.clock.tick(constant.FRAME_RATE)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game.running = False

        elif event.type == pygame.KEYDOWN:
            key=pygame.key.name(event.key)
            if key == 't':
                pass
                    
                

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed(3):
                mouse_coords = [pygame.mouse.get_pos()[0]//constant.SQUARE_SIZE, pygame.mouse.get_pos()[1]//constant.SQUARE_SIZE]
                game.level_test.click(mouse_coords)
                

    game.level_test.draw()
    game.update_display()

pygame.quit()   