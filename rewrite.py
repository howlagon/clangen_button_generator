import pygame

pygame.font.init()
FONT = pygame.font.Font('clangen.ttf', 16)
class Palette():
    palette = [
        (0, 0, 0, 0), (47, 41, 24, 255), (121, 96, 69, 255), (101, 89, 52, 255), (87, 76, 45, 255)
    ]
    hover = [
        (0, 0, 0, 0), (14, 11, 4, 255), (41, 27, 15, 255), (30, 24, 9, 255), (23, 18, 7, 255)   
    ]
    unavailable = [
        (0, 0, 0, 0), (58, 56, 51, 255), (112, 107, 100, 255), (92, 88, 80, 255), (80, 78, 70, 255)
    ]

class SquareButton():
    def __init__(self, size: tuple):
        self.surface = pygame.Surface(size, pygame.SRCALPHA)
        self.size = (size[0] - 1, size[1] - 1)
        self.surface = self.surface.convert_alpha()
        self.palette = Palette.palette
        
        self.fill()
        self.outline()
        self.inline()

    def outline(self):
        # pygame.draw.rect(self.surface, self.palette[3], (0, 0, 100, 100))
        pygame.draw.line(self.surface, self.palette[1], (2, 0), (self.size[0]-2, 0))
        self.surface.set_at((1, 1), self.palette[1])
        self.surface.set_at((self.size[0]-1, 1), self.palette[1])
        pygame.draw.line(self.surface, self.palette[1], (0, 2), (0, self.size[1]-2))
        pygame.draw.line(self.surface, self.palette[1], (self.size[0], 2), (self.size[0], self.size[1]-2))
        self.surface.set_at((1, self.size[1]-1), self.palette[1])
        self.surface.set_at((self.size[0]-1, self.size[1]-1), self.palette[1])
        pygame.draw.line(self.surface, self.palette[1], (2, self.size[1]), (self.size[0]-2, self.size[1]))
    def inline(self):
        pygame.draw.line(self.surface, self.palette[2], (2, 1), (self.size[0]-2, 1))
        self.surface.set_at((2, 2), self.palette[2])
        self.surface.set_at((self.size[0]-2, 2), self.palette[2])
        pygame.draw.line(self.surface, self.palette[2], (1, 2), (1, self.size[1]-2))
        pygame.draw.line(self.surface, self.palette[2], (self.size[0]-1, 2), (self.size[0]-1, self.size[1]-2))
        self.surface.set_at((2, self.size[1]-2), self.palette[2])
        self.surface.set_at((self.size[0]-2, self.size[1]-2), self.palette[2])
        pygame.draw.line(self.surface, self.palette[2], (2, self.size[1]-1), (self.size[0]-2, self.size[1]-1))
    def fill(self):
        pygame.draw.rect(self.surface, self.palette[3], (2, 2, self.size[0]-2, self.size[1]-2))

class RectButton():
    def __init__(self, 
                 size: tuple, 
                 text: str = "",
                 shadow: list = [True, True, False, False]):
        self.size = (size[0], size[1])
        self.surface = pygame.Surface(self.size, pygame.SRCALPHA)
        self.surface = self.surface.convert_alpha()
        self.surface.fill((255, 255, 0))
        self.palette = Palette.palette
        self.shadow = shadow
        self.text = self.build_text(text)
        
        self.build()


    def corner(self, shadow_corner1, shadow_corner2):
        surface = pygame.Surface((5, 4), pygame.SRCALPHA)
        surface = surface.convert_alpha()
        # outline
        pygame.draw.line(surface, self.palette[1], (3, 1), (4, 1))
        surface.set_at((2, 2), self.palette[1])
        surface.set_at((1, 3), self.palette[1])
        # inline
        pygame.draw.line(surface, self.palette[2], (3, 2), (4, 2))
        surface.set_at((2, 3), self.palette[2])
        # fill
        if shadow_corner1 and shadow_corner2:
            pygame.draw.line(surface, self.palette[4], (3, 3), (4, 3))
        else:
            pygame.draw.line(surface, self.palette[3], (3, 3), (4, 3))
        return surface

    def edge(self, length: int, rotate: bool = False, flip: bool = False, shadow = False):
        surface = pygame.Surface((length, 3), pygame.SRCALPHA)
        surface = surface.convert_alpha()
        # outline
        pygame.draw.line(surface, self.palette[1], (0, 0), (length, 0))
        # inline
        pygame.draw.line(surface, self.palette[2], (0, 1), (length, 1))
        # fill
        if shadow:
            pygame.draw.line(surface, self.palette[4], (0, 2), (length, 2))
        else:
            pygame.draw.line(surface, self.palette[3], (0, 2), (length, 2))
        if rotate and flip:
            surface = pygame.transform.rotate(surface, 90)
            surface = pygame.transform.flip(surface, True, False)
        elif rotate:
            surface = pygame.transform.rotate(surface, 90)
        elif flip:
            surface = pygame.transform.flip(surface, False, True)

        return surface

    def build_text(self, text):
        text = FONT.render(text, False, (239, 229, 206))
        return text

    def build(self):
        # fill [5]
        pygame.draw.rect(self.surface, self.palette[3], (2, 2, self.size[0]-4, self.size[1]-4))
        # corners [1, 3, 7, 9]
        self.surface.blit(self.corner(self.shadow[0], self.shadow[1]), (0, 0))
        self.surface.blit(pygame.transform.flip(self.corner(self.shadow[0], self.shadow[2]), True, False), (self.size[0]-5, 0))
        self.surface.blit(pygame.transform.flip(self.corner(self.shadow[1], self.shadow[3]), False, True), (0, self.size[1] - 4))
        self.surface.blit(pygame.transform.flip(self.corner(self.shadow[2], self.shadow[3]), True, True), (self.size[0]-5, self.size[1] - 4))
        # edges [2, 4, 6, 8]
        self.surface.blit(self.edge(self.size[0]-10, shadow=self.shadow[0]), (5, 0))
        self.surface.blit(self.edge(self.size[1]-8, rotate=True, shadow=self.shadow[1]), (0, 4))
        self.surface.blit(self.edge(self.size[1]-8, rotate=True, flip=True, shadow=self.shadow[2]), (self.size[0]-3, 4))
        self.surface.blit(self.edge(self.size[0]-10, flip=True, shadow=self.shadow[3]), (5, self.size[1]-3))
        # text
        text_rect = self.text.get_rect(center=(self.size[0] / 2 + 1, self.size[1] / 2 + 1))
        self.surface.blit(self.text, text_rect)


        
    def fill(self):
        pygame.draw.rect(self.surface, self.palette[3], (2, 2, self.size[0]-2, self.size[1]-2))
