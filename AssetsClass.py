from functions import load_images

class Assets(object):
    def __init__(self):
        self.blocks = {'Normal' : load_images('Sprites/Blocks/Normal'),
                       'Bomb' : load_images('Sprites/Blocks/Bomb'),
                       'Tornado' : load_images('Sprites/Blocks/Tornado'),
                       'Freeze' : load_images('Sprites/Blocks/Freeze'),
                       'Solid' : load_images('Sprites/Blocks/Solid'),
                       'Pattern' : load_images('Sprites/Blocks/Pattern'),
                       'Buffer' : load_images('Sprites/Blocks/Buffer')}
        self.backgrounds = {'Temp' : load_images('Backgrounds')}