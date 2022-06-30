import pygame, pygame.freetype
BLACK = ("#000000")

class Box(pygame.sprite.Sprite):
    def __init__(self, color, width, height, letter, state):
        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)

        pygame.draw.rect(self.image, color, [0, 0, width, height], 2)

        self.rect = self.image.get_rect()