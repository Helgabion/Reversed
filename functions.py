import pygame
import constant
import os
import copy

def object_copy(instance, init_args=None):
    if init_args:
        new_obj = instance.__class__(**init_args)
    else:
        new_obj = instance.__class__()
    if hasattr(instance, '__dict__'):
        for k in instance.__dict__ :
            try:
                attr_copy = copy.deepcopy(getattr(instance, k))
            except Exception as e:
                attr_copy = object_copy(getattr(instance, k))
            setattr(new_obj, k, attr_copy)

        new_attrs = list(new_obj.__dict__.keys())
        for k in new_attrs:
            if not hasattr(instance, k):
                delattr(new_obj, k)
        return new_obj
    else:
        return instance

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