import pygame, warnings
from typing import Union

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

class RectButton():
    def __init__(self, 
                 size: tuple, 
                 text: str = "",
                 hover: bool = False,
                 unavailable: bool = False,
                 rounded_corners: list = [True, True, True, True],
                 shadows: list = [True, True, False, False],
                 hanging: bool = False):
        self.size = (size[0], size[1])
        self.surface = pygame.Surface(self.size, pygame.SRCALPHA)
        self.surface = self.surface.convert_alpha()
        self.hover = hover
        self.unavailable = unavailable
        self.hanging = hanging
        if unavailable:
            self.palette = Palette.unavailable
        elif hover:
            self.palette = Palette.hover
        else:
            self.palette = Palette.palette
        self.rounded_corners = rounded_corners
        self.shadow = shadows
        self.text = self._build_text(text)
        
        self._build()
        if hanging:
            self._hang()

    def _corner(self, shadow_corner1: bool, shadow_corner2: bool, rounded: bool = True):
        surface = pygame.Surface((10, 8), pygame.SRCALPHA)
        surface = surface.convert_alpha()
        if rounded:
            # outline
            pygame.draw.rect(surface, self.palette[1], (6, 2, 4, 2))
            pygame.draw.rect(surface, self.palette[1], (4, 4, 2, 2))
            pygame.draw.rect(surface, self.palette[1], (2, 6, 2, 2))
            # inline
            pygame.draw.rect(surface, self.palette[2], (6, 4, 4, 2))
            pygame.draw.rect(surface, self.palette[2], (4, 6, 2, 2))
            # fill
            if shadow_corner1 and shadow_corner2:
                pygame.draw.rect(surface, self.palette[4], (6, 6, 4, 2))
            else:
                pygame.draw.rect(surface, self.palette[3], (6, 6, 4, 2))
            return surface

        # outline
        pygame.draw.rect(surface, self.palette[1], (0, 0, 10, 2))
        pygame.draw.rect(surface, self.palette[1], (0, 0, 2, 8))
        # inline
        pygame.draw.rect(surface, self.palette[2], (2, 2, 8, 2))
        pygame.draw.rect(surface, self.palette[2], (2, 2, 2, 6))
        # fill
        pygame.draw.rect(surface, self.palette[3], (4, 4, 6, 2))
        if shadow_corner1:
            pygame.draw.rect(surface, self.palette[4], (4, 4, 6, 2))
        if shadow_corner2:
            pygame.draw.rect(surface, self.palette[4], (4, 4, 2, 4))
        return surface

    def _edge(self, length: int, rotate: bool = False, flip: bool = False, shadow = False):
        odd = False
        if round(length / 2) != int(length / 2):
            length += 1
            odd = True
        surface = pygame.Surface((length, 6), pygame.SRCALPHA)
        surface = surface.convert_alpha()
        # outline
        pygame.draw.rect(surface, self.palette[1], (0, 0, length, 2))
        # inline
        pygame.draw.rect(surface, self.palette[2], (0, 2, length if not odd else length-1, 2))
        # fill
        if shadow:
            pygame.draw.rect(surface, self.palette[4], (0, 4, length if not odd else length-1, 2))
        else:
            pygame.draw.rect(surface, self.palette[3], (0, 4, length if not odd else length-1, 2))
        
        if rotate and flip:
            surface = pygame.transform.rotate(surface, 90)
            surface = pygame.transform.flip(surface, True, False)
        elif rotate:
            surface = pygame.transform.rotate(surface, 90)
        elif flip:
            surface = pygame.transform.flip(surface, False, True)

        return surface

    def _build_text(self, text):
        text = FONT.render(text, False, (239, 229, 206))
        return text

    def _build(self):
        # fill [5]
        pygame.draw.rect(self.surface, self.palette[3], (4, 4, self.size[0]-8, self.size[1]-8))
        # corners [1, 3, 7, 9]
        self.surface.blit(self._corner(self.shadow[0], self.shadow[1], rounded=self.rounded_corners[0]), (0, 0))
        self.surface.blit(pygame.transform.flip(self._corner(self.shadow[0], self.shadow[2], rounded=self.rounded_corners[1]), True, False), (self.size[0]-10, 0))
        self.surface.blit(pygame.transform.flip(self._corner(self.shadow[3], self.shadow[1], rounded=self.rounded_corners[2]), False, True), (0, self.size[1] - 8))
        self.surface.blit(pygame.transform.flip(self._corner(self.shadow[3], self.shadow[2], rounded=self.rounded_corners[3]), True, True), (self.size[0]-10, self.size[1] - 8))
        
        # edges [2, 4, 6, 8]
        self.surface.blit(self._edge(self.size[0]-20, shadow=self.shadow[0]), (10, 0))
        self.surface.blit(self._edge(self.size[1]-16, rotate=True, shadow=self.shadow[1]), (0, 8))
        self.surface.blit(self._edge(self.size[1]-16, rotate=True, flip=True, shadow=self.shadow[2]), (self.size[0]-6, 8))
        self.surface.blit(self._edge(self.size[0]-20, flip=True, shadow=self.shadow[3]), (10, self.size[1]-6))
        
        # text
        text_rect = self.text.get_rect(center=(self.size[0] / 2 + 1, self.size[1] / 2 + 2))
        
        if text_rect.width > self.size[0]:
            raise ValueError(f'Text width is too large to fit in the button! Minimum width is {text_rect.width}, recommended {text_rect.width + 12}')
        elif text_rect.width > self.size[0] - 8:
            warnings.warn(f'Text width is too small to fit in the button comfortably, minimum width is {text_rect.width + 12}')

        # yell at you if the text will be offset by 1px
        if text_rect.width % 2 != 0 and self.size[0] % 2 == 0:
            warnings.warn(f'Text has an odd width! Consider using an odd width instead of an even one.', Warning, stacklevel=3)
        elif text_rect.width % 2 == 0 and self.size[0] % 2 != 0:
            warnings.warn(f'Text has an even width! Consider using an even width instead of an odd one.', Warning, stacklevel=3)
        self.surface.blit(self.text, text_rect)
    
    def _hang(self):
        surface = pygame.Surface((self.size[0], self.size[1]+6), pygame.SRCALPHA)
        surface = surface.convert_alpha()
        surface.blit(self.surface, (0, 6))

        connector = pygame.Surface((10, 6))
        pygame.draw.rect(connector, Palette.palette[2], (0, 0, 10, 6))
        pygame.draw.rect(connector, Palette.palette[4], (2, 0, 6, 6))
        pygame.draw.rect(connector, Palette.palette[3], (4, 0, 2, 6))

        surface.blit(connector, (12, 0))
        surface.blit(connector, (self.size[0]-22, 0))
        self.surface = surface

class SquareButton(RectButton):
    def _corner(self, shadow_corner1: bool, shadow_corner2: bool, rounded: bool = True):
        surface = pygame.Surface((10, 8), pygame.SRCALPHA)
        surface = surface.convert_alpha()
        if rounded:
            # outline
            pygame.draw.rect(surface, self.palette[1], (4, 0, 6, 2))
            pygame.draw.rect(surface, self.palette[1], (2, 2, 2, 2))
            pygame.draw.rect(surface, self.palette[1], (0, 4, 2, 4))
            # fill
            pygame.draw.rect(surface, self.palette[3], (4, 4, 4, 4))
            # inline
            pygame.draw.rect(surface, self.palette[2], (4, 2, 6, 2))
            pygame.draw.rect(surface, self.palette[2], (2, 4, 4, 2))
            pygame.draw.rect(surface, self.palette[2], (2, 4, 2, 4))
            # shadow
            if shadow_corner1:
                pygame.draw.rect(surface, self.palette[4], (6, 4, 4, 2))
                pygame.draw.rect(surface, self.palette[4], (4, 6, 2, 2))
            elif shadow_corner2:
                pygame.draw.rect(surface, self.palette[4], (4, 6, 2, 2))
                pygame.draw.rect(surface, self.palette[4], (6, 4, 2, 2))
            return surface

        # outline
        pygame.draw.rect(surface, self.palette[1], (0, 0, 10, 2))
        pygame.draw.rect(surface, self.palette[1], (0, 0, 2, 8))
        # inline
        pygame.draw.rect(surface, self.palette[2], (2, 2, 8, 2))
        pygame.draw.rect(surface, self.palette[2], (2, 2, 2, 6))
        # fill
        pygame.draw.rect(surface, self.palette[3], (4, 4, 6, 2))
        if shadow_corner1:
            pygame.draw.rect(surface, self.palette[4], (4, 4, 6, 2))
        if shadow_corner2:
            pygame.draw.rect(surface, self.palette[4], (4, 4, 2, 4))
        return surface

class Button():
    @staticmethod
    def new(size: tuple,
            text: str = "",
            hover: bool = False,
            unavailable: bool = False,
            rounded_corners: Union[bool, list] = [True, True, True, True],
            shadows: Union[bool, list] = [True, True, False, False],
            hanging: bool = False) -> pygame.Surface:
        if type(rounded_corners) == bool:
            rounded_corners = [rounded_corners]*4
        elif len(rounded_corners) == 4:
            rounded_corners = rounded_corners
        else:
            raise ValueError("rounded_corners must be of type bool or list[bool; 4]")

        if type(shadows) == bool:
            shadows = [shadows]*4
        elif len(shadows) == 4:
            shadows = shadows
        else:
            raise ValueError("shadows must be of type bool or list[bool; 4]")
        
        if size[0] == size[1]:
            button = SquareButton(size, text, hover, unavailable, rounded_corners, shadows, hanging)
        else:
            button = RectButton(size, text, hover, unavailable, rounded_corners, shadows, hanging)
        
        return button.surface
    
    @staticmethod
    def new_auto_pad(text: str = "",
                     padding: int = 6,
                     hover: bool = False,
                     unavailable: bool = False,
                     rounded_corners: Union[bool, list] = [True, True, True, True],
                     shadows: Union[bool, list] = [True, True, False, False],
                     hanging: bool = False) -> pygame.Surface:
        _text = FONT.render(text, False, (239, 229, 206))

        width = _text.get_width()
        height = _text.get_height()
        size = (width + padding + 12, height + padding + 10)

        button = Button.new(size, text, hover, unavailable, rounded_corners, shadows, hanging)
        return button