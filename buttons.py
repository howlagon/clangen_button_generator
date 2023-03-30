from PIL import Image
from numpy import array, uint8
from time import time
from typing import Union

COLORS_NORMAL = [
    (0, 0, 0, 0), (47, 41, 24, 255), (121, 96, 69, 255), (101, 89, 52, 255), (87, 76, 45, 255)
]
COLORS_HOVER = [
    (0, 0, 0, 0), (14, 11, 4, 255), (41, 27, 15, 255), (30, 24, 9, 255), (23, 18, 7, 255)
]
COLORS_UNAVAILABLE = [
    (0, 0, 0, 0), (58, 56, 51, 255), (112, 107, 100, 255), (92, 88, 80, 255), (80, 78, 70, 255)
]

class SquareButton():
    def __init__(self, size: int, hover=False, unavailable=False, rounded_corners: Union[bool, tuple, list]=(True, True, True, True)) -> None:
        self.size = size
        self.hover = hover
        self.unavailable = unavailable
        self.palette = COLORS_HOVER if unavailable else COLORS_HOVER if hover else COLORS_NORMAL
        self.bitmap = Bitmap(size, size)
    
    def corners(self):
        COLORS = self.palette
        size = self.size
        # 1
        self.bitmap.insert_at(0, 0, [
                              [COLORS[0], COLORS[0], COLORS[1], COLORS[1]], 
                              [COLORS[0], COLORS[1], COLORS[2], COLORS[2]],
                              [COLORS[1], COLORS[2], COLORS[2], COLORS[4]],
                              [COLORS[1], COLORS[2], COLORS[4], COLORS[3]]
        ])
        # 3
        self.bitmap.insert_at(size-4, 0, [
                                   [COLORS[1], COLORS[1], COLORS[0], COLORS[0]],
                                   [COLORS[2], COLORS[2], COLORS[1], COLORS[0]],
                                   [COLORS[4], COLORS[2], COLORS[2], COLORS[1]],
                                   [COLORS[3], COLORS[4], COLORS[2], COLORS[1]],
        ])
        # 7
        self.bitmap.insert_at(0, size-4, [
                                   [COLORS[1], COLORS[2], COLORS[3], COLORS[3]],
                                   [COLORS[1], COLORS[2], COLORS[2], COLORS[3]],
                                   [COLORS[0], COLORS[1], COLORS[2], COLORS[2]],
                                   [COLORS[0], COLORS[0], COLORS[1], COLORS[1]]
        ])
        # 9
        self.bitmap.insert_at(size-4, size-4, [
                                        [COLORS[3], COLORS[3], COLORS[2], COLORS[1]],
                                        [COLORS[3], COLORS[2], COLORS[2], COLORS[1]],
                                        [COLORS[2], COLORS[2], COLORS[1], COLORS[0]],
                                        [COLORS[1], COLORS[1], COLORS[0], COLORS[0]],
        ])
    def fill(self):
        COLORS = self.palette
        size = self.size
        # 2
        self.bitmap.insert_at(4, 0, [
                                [COLORS[1] for _ in range(0, size-8)],
                                [COLORS[2] for _ in range(0, size-8)],
                                [COLORS[4] for _ in range(0, size-8)],
                                [COLORS[3] for _ in range(0, size-8)],
        ])
        # 4
        self.bitmap.insert_at(0, 4, [[COLORS[1], COLORS[2], COLORS[3], COLORS[3]] for _ in range(0, size-8)])
        # 5
        self.bitmap.insert_at(4, 4, [[COLORS[3] for _ in range(0, size-8)] for i in range(0, size-8)])
        # 6
        self.bitmap.insert_at(size-4, 4, [[COLORS[3], COLORS[3], COLORS[2], COLORS[1]] for _ in range(0, size-8)])
        # 8
        self.bitmap.insert_at(4, size-4, [
                                     [COLORS[3] for _ in range(0, size-8)],
                                     [COLORS[3] for _ in range(0, size-8)],
                                     [COLORS[2] for _ in range(0, size-8)],
                                     [COLORS[1] for _ in range(0, size-8)]
        ])
        
    def build(self):
        self.corners()
        self.fill()
        return self.bitmap

class LongButton():
    def __init__(self, 
                 width: int, 
                 height: int, 
                 hover: bool = False, 
                 unavailable: bool = False, 
                 rounded_corners: Union[bool, tuple, list] = True, 
                 shadows: Union[bool, tuple, list] = [True, True, False, False]) -> None:
        self.width = width
        self.height = height
        self.hover = hover
        self.unavailable = unavailable
        self.palette = COLORS_HOVER if unavailable else COLORS_HOVER if hover else COLORS_NORMAL
        if type(rounded_corners) == bool:
            self.rounded_corners = (rounded_corners, rounded_corners, rounded_corners, rounded_corners)
        elif type(rounded_corners) in [tuple, list] and len(rounded_corners) == 4:
            self.rounded_corners = list(rounded_corners)
        else:
            exit("dev err temp")
        if type(shadows) == bool:
            self.shadows = (shadows, shadows, shadows, shadows)
        elif type(shadows) in [tuple, list] and len(shadows) == 4:
            self.shadows = list(shadows)
        else:
            exit("dev err temp 2")
        self.bitmap = Bitmap(width, height)
    def corners(self):
        width = self.width
        height = self.height
        COLORS = self.palette
        if self.rounded_corners[0]: 
            self.bitmap.insert_at(0, 0, [
                [COLORS[0], COLORS[0], COLORS[0], COLORS[0], COLORS[0], COLORS[1], COLORS[1]],
                [COLORS[0], COLORS[0], COLORS[0], COLORS[1], COLORS[1], COLORS[2], COLORS[2]],
                [COLORS[0], COLORS[0], COLORS[1], COLORS[2], COLORS[2], COLORS[4] if self.shadows[0] else COLORS[3], COLORS[4] if self.shadows[0] else COLORS[3]],
                [COLORS[0], COLORS[1], COLORS[2], COLORS[4] if self.shadows[0] and self.shadows[1] else COLORS[3], COLORS[4] if self.shadows[0] and self.shadows[1] else COLORS[3], COLORS[3], COLORS[3]],
                [COLORS[1], COLORS[2], COLORS[4] if self.shadows[1] else COLORS[3], COLORS[3], COLORS[3], COLORS[3], COLORS[3]]
            ])
        else:
            self.bitmap.insert_at(0, 0, [
                [COLORS[1] for _ in [0, 1, 2, 3, 4, 5, 6]],
                [COLORS[1], *[COLORS[2] for _ in [0, 1, 2, 3, 4, 5]]],
                (
                    [COLORS[1], COLORS[2], *[COLORS[4] for _ in [0, 1, 2, 3, 4]]] if self.shadows[0] 
                    else [COLORS[1], COLORS[2], COLORS[4], *[COLORS[3] for _ in [0, 1, 2, 3]]] if self.shadows[1]
                    else [COLORS[1], COLORS[2], *[COLORS[3] for _ in [0, 1, 2, 3, 4]]]
                ),
                [COLORS[1], COLORS[2], COLORS[4] if self.shadows[1] else COLORS[3], *[COLORS[3] for _ in [0, 1, 2, 3]]],
                [COLORS[1], COLORS[2], COLORS[4] if self.shadows[1] else COLORS[3], *[COLORS[3] for _ in [0, 1, 2, 3]]]
            ])
        if self.rounded_corners[1]:
            self.bitmap.insert_at(width-7, 0, [
                [COLORS[1], COLORS[1], COLORS[0], COLORS[0], COLORS[0], COLORS[0], COLORS[0]],
                [COLORS[2], COLORS[2], COLORS[1], COLORS[1], COLORS[0], COLORS[0], COLORS[0]],
                [COLORS[4] if self.shadows[0] else COLORS[3], COLORS[4] if self.shadows[0] else COLORS[3], COLORS[2], COLORS[2], COLORS[1], COLORS[0], COLORS[0]],
                [COLORS[3], COLORS[3], COLORS[4] if self.shadows[0] and self.shadows[2] else COLORS[3], COLORS[4] if self.shadows[0] and self.shadows[2] else COLORS[3], COLORS[2], COLORS[1], COLORS[0]],
                [COLORS[3], COLORS[3], COLORS[3], COLORS[3], COLORS[4] if self.shadows[2] else COLORS[3], COLORS[2], COLORS[1]]
            ])
        else:
            self.bitmap.insert_at(width-7, 0, [
                [COLORS[1] for _ in [0, 1, 2, 3, 4, 5, 6]],
                [*[COLORS[2] for _ in [0, 1, 2, 3, 4, 5]], COLORS[1]],
                (
                    [*[COLORS[4] for _ in [0, 1, 2, 3, 4]], COLORS[2], COLORS[1]] if self.shadows[0]
                    else [*[COLORS[3] for _ in [0, 1, 2, 3]], COLORS[4], COLORS[2], COLORS[1]] if self.shadows[2]
                    else [*[COLORS[3] for _ in [0, 1, 2, 3, 4]], COLORS[2], COLORS[1]]
                ),
                [*[COLORS[3] for _ in [0, 1, 2, 3]], COLORS[4] if self.shadows[2] else COLORS[3] , COLORS[2], COLORS[1]],
                [*[COLORS[3] for _ in [0, 1, 2, 3]], COLORS[4] if self.shadows[2] else COLORS[3] , COLORS[2], COLORS[1]]
            ])
        if self.rounded_corners[2]:
            self.bitmap.insert_at(0, height-5, [
                [COLORS[1], COLORS[2], COLORS[4] if self.shadows[1] else COLORS[3], COLORS[3], COLORS[3], COLORS[3], COLORS[3]],
                [COLORS[0], COLORS[1], COLORS[2], COLORS[4] if self.shadows[1] and self.shadows[3] else COLORS[3], COLORS[4] if self.shadows[1] and self.shadows[3] else COLORS[3], COLORS[3], COLORS[3]],
                [COLORS[0], COLORS[0], COLORS[1], COLORS[2], COLORS[2], COLORS[4] if self.shadows[3] else COLORS[3], COLORS[4] if self.shadows[3] else COLORS[3]],
                [COLORS[0], COLORS[0], COLORS[0], COLORS[1], COLORS[1], COLORS[2], COLORS[2]],
                [COLORS[0], COLORS[0], COLORS[0], COLORS[0], COLORS[0], COLORS[1], COLORS[1]]
            ])
        else:
            self.bitmap.insert_at(0, height-5, [
                [COLORS[1], COLORS[2], COLORS[4] if self.shadows[1] else COLORS[3], *[COLORS[3] for _ in [0, 1, 2, 3]]],
                [COLORS[1], COLORS[2], COLORS[4] if self.shadows[1] else COLORS[3], *[COLORS[3] for _ in [0, 1, 2, 3]]],
                [COLORS[1], COLORS[2], COLORS[4] if self.shadows[1] or self.shadows[3] else COLORS[3], *[COLORS[4] if self.shadows[3] else COLORS[3] for _ in [0, 1, 2, 3]]],
                [COLORS[1], *[COLORS[2] for _ in [0, 1, 2, 3, 4, 5]]],
                [COLORS[1] for _ in [0, 1, 2, 3, 4, 5, 6]]
            ])
        if self.rounded_corners[3]:
            self.bitmap.insert_at(width-7, height-5, [
                [COLORS[3], COLORS[3], COLORS[3], COLORS[3], COLORS[4] if self.shadows[2] else COLORS[3], COLORS[2], COLORS[1]],
                [COLORS[3], COLORS[3], COLORS[4] if self.shadows[2] and self.shadows[3] else COLORS[3], COLORS[4] if self.shadows[2] and self.shadows[3] else COLORS[3], COLORS[2], COLORS[1], COLORS[0]],
                [COLORS[4] if self.shadows[3] else COLORS[3], COLORS[4] if self.shadows[3] else COLORS[3], COLORS[2], COLORS[2], COLORS[1], COLORS[0], COLORS[0]],
                [COLORS[2], COLORS[2], COLORS[1], COLORS[1], COLORS[0], COLORS[0], COLORS[0]],
                [COLORS[1], COLORS[1], COLORS[0], COLORS[0], COLORS[0], COLORS[0], COLORS[0]]
            ])
        else:
            self.bitmap.insert_at(width-7, height-5, [
                [*[COLORS[3] for _ in [0, 1, 2, 3]], COLORS[4] if self.shadows[2] else COLORS[3], COLORS[2], COLORS[1]],
                [*[COLORS[3] for _ in [0, 1, 2, 3]], COLORS[4] if self.shadows[2] else COLORS[3], COLORS[2], COLORS[1]],
                [*[COLORS[4] if self.shadows[3] else COLORS[3] for _ in [0, 1, 2, 3]], COLORS[4] if self.shadows[2] or self.shadows[3] else COLORS[3], COLORS[2], COLORS[1]],
                [*[COLORS[2] for _ in [0, 1, 2, 3, 4, 5]], COLORS[1]],
                [COLORS[1] for _ in [0, 1, 2, 3, 4, 5, 6]]
            ])

    def fill(self):
        width = self.width
        height = self.height
        COLORS = self.palette
        # 2
        self.bitmap.insert_at(7, 0, [
                                [COLORS[1] for _ in range(0, width-14)],
                                [COLORS[2] for _ in range(0, width-14)],
                                [COLORS[4] if self.shadows[0] else COLORS[3] for _ in range(0, width-14)],
                                [COLORS[3] for _ in range(0, width-14)],
                                [COLORS[3] for _ in range(0, width-14)], 
        ])
        # 4
        self.bitmap.insert_at(0, 5, [[COLORS[1], COLORS[2], COLORS[4] if self.shadows[1] else COLORS[3], COLORS[3], COLORS[3], COLORS[3], COLORS[3]] for _ in range(0, height-10)])
        # 5
        self.bitmap.insert_at(7, 5, [[COLORS[3] for _ in range(0, width-14)] for i in range(0, height-10)])
        # 6
        self.bitmap.insert_at(width-7, 5, [[COLORS[3], COLORS[3], COLORS[3], COLORS[3], COLORS[4] if self.shadows[2] else COLORS[3], COLORS[2], COLORS[1]] for _ in range(0, height-10)])
        # 8
        self.bitmap.insert_at(7, height-5, [
                                     [COLORS[3] for _ in range(0, width-14)],
                                     [COLORS[3] for _ in range(0, width-14)],
                                     [COLORS[4] if self.shadows[3] else COLORS[3] for _ in range(0, width-14)],
                                     [COLORS[2] for _ in range(0, width-14)],
                                     [COLORS[1] for _ in range(0, width-14)]
        ])
    def build(self):
        self.corners()
        self.fill()
        return self.bitmap

class Bitmap():
    def __init__(self, width, height) -> None:
        self.storage = [[(0, 0, 0, 0) for _ in range(width)] for _ in range(height)]
        self.width = width
        self.height = height
    
    def __call__(self):
        return self.storage

    def insert_at(self, x, y, pixels):
        for y_axis in range(0, len(pixels)):
            for item in range(0, len(pixels[y_axis])):
                self.storage[y + y_axis][x + item] = pixels[y_axis][item]
        
class TextButton():
    @staticmethod
    def new_square_button(size: int, hover=False, unavailable=False):
        button = SquareButton(size, hover, unavailable)
        bitmap = button.build()
        arr = array(bitmap(), dtype=uint8)
        new_image = Image.fromarray(arr)
        return new_image
    
    @staticmethod
    def new_long_button(
                        width: int, 
                        height: int, 
                        hover: bool = False, 
                        unavailable: bool = False, 
                        rounded_corners: Union[bool, tuple, list] = [True, True, True, True], 
                        shadows: Union[bool, tuple, list] = [True, True, False, False]) -> Image.Image:
        button = LongButton(width, height, hover, unavailable, rounded_corners, shadows)
        bitmap = button.build()
        arr = array(bitmap(), dtype=uint8)
        new_image = Image.fromarray(arr)
        return new_image
