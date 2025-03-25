import pygame
import constant
import os

def load_image(name): #thanks to DaFluffyPotato
    img = pygame.image.load(constant.ASSETS_PATH + name).convert_alpha()
    return img

def load_images(name): #thanks to DaFluffyPotato
    images = []
    for img_name in sorted(os.listdir(constant.ASSETS_PATH + name)):
        images.append(load_image(name + '/' +  img_name))
    return images

def collide(entity_a, entity_b, coord_x=0, coord_y=0):
    #tells if the first entity collides with the second one shifted by certain coords
    return (entity_a.rect.centerx // constant.SQUARE_SIZE, entity_a.rect.centery // constant.SQUARE_SIZE) ==\
           (entity_b.rect.centerx // constant.SQUARE_SIZE + coord_x, entity_b.rect.centery // constant.SQUARE_SIZE + coord_y)