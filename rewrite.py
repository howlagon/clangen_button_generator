from PIL import Image
from numpy import array, uint8
from typing import Union

class Bitmap():
    """Dynamic list (arr) storage that allows for inserting on multiple lines"""
    def __init__(self, width: int, height: int):
        self.storage = [
                        [(0, 0, 0, 0) for _ in range(width)] for _ in range(height)]
        self.width = width
        self.height = height
    def __call__(self): #is this used? idk
        return self.storage
    def insert_at(self, x: int, y: int, pixels: list):
        """Inserts pixels at x,y, where pixels MUST be a 2d array"""
        for y_axis in range(0, len(pixels)):
            for x_axis in range(0, len(pixels[y_axis])):
                if pixels[y_axis][x_axis] == None: continue
                self.storage[y + y_axis][x + x_axis] = pixels[y_axis][x_axis]

class ButtonLong():
    # oh dear god
    def __init__(self,
                 width: int,
                 height: int,
                 hover: bool = False,
                 unavailable: bool = False,
                 rounded_corners = True,
                 shadows = [True, True, False, False]
    ) -> None:
        self.width = width
        self.height = height
        self.hover = hover
        self.unavailable = unavailable
        self.palette = [(0, 0, 0, 0), (47, 41, 24, 255), (121, 96, 69, 255), (101, 89, 52, 255), (87, 76, 45, 255)]
        if type(rounded_corners) == bool:
            self.rounded_corners = (rounded_corners, rounded_corners, rounded_corners, rounded_corners)
        elif len(rounded_corners) == 4:
            self.rounded_corners = list(rounded_corners)
        else: exit('long err 1 please delete this howl when you commit')
        if type(shadows) == bool:
            self.shadows = (shadows, shadows, shadows, shadows)
        elif len(shadows) == 4:
            self.shadows = list(shadows)
        else: exit('long err 2 also delete this one too k thanks :)')
        self.bitmap = Bitmap(width, height)
    def generate_corner(self, round=True, shaded_one=False, shaded_two=False):
        shade_0 = self.palette[4] if shaded_one else self.palette[3]
        shade_1 = self.palette[4] if shaded_two else self.palette[3]
        shade_0_and_1 = self.palette[4] if shaded_one and shaded_two else self.palette[3]
        shade_0_or_1 = self.palette[4] if shaded_one or shaded_two else self.palette[3]
        if round:
            return [
                    [*[self.palette[0]]*5, *[self.palette[1]]*2],
                    [*[self.palette[0]]*3, *[self.palette[1]]*2, *[self.palette[2]]*2],
                    [*[self.palette[0]]*2, self.palette[1], *[self.palette[2]]*2, *[shade_0]*2],
                    [self.palette[0], self.palette[1], self.palette[2], *[shade_0_and_1]*2, *[self.palette[3]]*2],
                    [self.palette[1], self.palette[2], shade_1, *[self.palette[3]]*4]]
        return [
                [*[self.palette[1]]*7],
                [self.palette[1], *[self.palette[2]]*6],
                [self.palette[1], self.palette[2], shade_0_or_1, *[shade_0]*4],
                [self.palette[1], self.palette[2], shade_1, *[self.palette[3]]*4],
                [self.palette[1], self.palette[2], shade_1, *[self.palette[3]]*4]
            ]
    def corners(self):
        # corner 1
        if self.rounded_corners[0]:
            self.bitmap.insert_at(0, 0, self.generate_corner(True, self.shadows[0], self.shadows[1]))
        else:
            self.bitmap.insert_at(0, 0, self.generate_corner(False, self.shadows[0], self.shadows[1]))
        # corner 3
        if self.rounded_corners[1]:
            self.bitmap.insert_at(self.width-7, 0, [item[::-1] for item in self.generate_corner(True, self.shadows[0], self.shadows[2])])
        else:
            self.bitmap.insert_at(self.width-7, 0, [item[::-1] for item in self.generate_corner(False, self.shadows[0], self.shadows[2])])
        # corner 7
        if self.rounded_corners[2]:
            self.bitmap.insert_at(0, self.height-5, self.generate_corner(True, self.shadows[3], self.shadows[1])[::-1])
        else:
            self.bitmap.insert_at(0, self.height-5, self.generate_corner(False, self.shadows[3], self.shadows[1])[::-1])
        # corner 9
        if self.rounded_corners[3]:
            self.bitmap.insert_at(self.width-7, self.height-5, [item[::-1] for item in self.generate_corner(True, self.shadows[3], self.shadows[2])[::-1]])
        else:
            self.bitmap.insert_at(self.width-7, self.height-5, [item[::-1] for item in self.generate_corner(False, self.shadows[3], self.shadows[2])[::-1]])

    def fill(self):
        top_bottom = [
            [self.palette[1]]*(self.width-14),
            [self.palette[2]]*(self.width-14),
            *[[self.palette[3]]*(self.width-14)]*3,
        ]
        top_bottom_shaded = [
            [self.palette[1]]*(self.width-14),
            [self.palette[2]]*(self.width-14),
            [self.palette[4]]*(self.width-14),
            *[[self.palette[3]]*(self.width-14)]*2
        ]
        left_right = [
            *[[self.palette[1], self.palette[2], *[self.palette[3]]*5]]*(self.height-10)
        ]
        left_right_shaded = [
            *[[self.palette[1], self.palette[2], self.palette[4], *[self.palette[3]]*4]]*(self.height-10)
        ]
        # 2
        if self.shadows[0]:
            self.bitmap.insert_at(7, 0, top_bottom_shaded)
        else:
            self.bitmap.insert_at(7, 0, top_bottom)
        # 4
        if self.shadows[1]:
            self.bitmap.insert_at(0, 5, left_right_shaded)
        else:
            self.bitmap.insert_at(0, 5, left_right)
        # 6
        if self.shadows[2]:
            self.bitmap.insert_at(self.width-7, 5, [item[::-1] for item in left_right_shaded])
        else:
            self.bitmap.insert_at(self.width-7, 5, [item[::-1] for item in left_right])
        # 8
        if self.shadows[3]:
            self.bitmap.insert_at(7, self.height-5, top_bottom_shaded[::-1])
        else:
            self.bitmap.insert_at(7, self.height-5, top_bottom[::-1])
        # 5
        self.bitmap.insert_at(7, 5, [
            *[[*[self.palette[3]]*(self.width-14)]]*(self.height-10)
        ])
    
    def build(self):
        self.corners()
        self.fill()
        return self.bitmap

class ButtonSquare():
    # oh dear god
    def __init__(self,
                 size: int,
                 hover: bool = False,
                 unavailable: bool = False,
                 rounded_corners = True,
                 shadows = [True, True, False, False]
    ) -> None:
        self.size = size
        self.calculated = size-4
        self.hover = hover
        self.unavailable = unavailable
        self.palette = [(0, 0, 0, 0), (47, 41, 24, 255), (121, 96, 69, 255), (101, 89, 52, 255), (87, 76, 45, 255)]
        if type(rounded_corners) == bool:
            self.rounded_corners = (rounded_corners, rounded_corners, rounded_corners, rounded_corners)
        elif len(rounded_corners) == 4:
            self.rounded_corners = list(rounded_corners)
        else: exit('long err 1 please delete this howl when you commit')
        if type(shadows) == bool:
            self.shadows = [shadows, shadows, shadows, shadows]
        elif len(shadows) == 4:
            self.shadows = list(shadows)
        else: exit('long err 2 also delete this one too k thanks :)')
        self.bitmap = Bitmap(size, size)
    def generate_corner(self, round=True, shaded_one=False, shaded_two=False):
        shade_0 = self.palette[4] if shaded_one else self.palette[3]
        shade_1 = self.palette[4] if shaded_two else self.palette[3]
        shade_0_or_1 = self.palette[4] if shaded_one or shaded_two else self.palette[3]
        if round:
            return [
                    [*[self.palette[0]]*2, *[self.palette[1]]*2],
                    [self.palette[0], self.palette[1], *[self.palette[2]]*2],
                    [self.palette[1], *[self.palette[2]]*2, shade_0_or_1],
                    [self.palette[1], self.palette[2], shade_0_or_1, self.palette[3]]]
        return [
                [*[self.palette[1]]*4],
                [self.palette[1], *[self.palette[2]]*3],
                [self.palette[1], self.palette[2], shade_0_or_1, shade_0],
                [self.palette[1], self.palette[2], shade_1, self.palette[3]]]
    def corners(self):
        # corner 1
        if self.rounded_corners[0]:
            self.bitmap.insert_at(0, 0, self.generate_corner(True, self.shadows[0], self.shadows[1]))
        else:
            self.bitmap.insert_at(0, 0, self.generate_corner(False, self.shadows[0], self.shadows[1]))
        # corner 3
        if self.rounded_corners[1]:
            self.bitmap.insert_at(self.calculated, 0, [item[::-1] for item in self.generate_corner(True, self.shadows[0], self.shadows[2])])
        else:
            self.bitmap.insert_at(self.calculated, 0, [item[::-1] for item in self.generate_corner(False, self.shadows[0], self.shadows[2])])
        # corner 7
        if self.rounded_corners[2]:
            self.bitmap.insert_at(0, self.calculated, self.generate_corner(True, self.shadows[3], self.shadows[1])[::-1])
        else:
            self.bitmap.insert_at(0, self.calculated, self.generate_corner(False, self.shadows[3], self.shadows[1])[::-1])
        # corner 9
        if self.rounded_corners[3]:
            self.bitmap.insert_at(self.calculated, self.calculated, [item[::-1] for item in self.generate_corner(True, self.shadows[3], self.shadows[2])[::-1]])
        else:
            self.bitmap.insert_at(self.calculated, self.calculated, [item[::-1] for item in self.generate_corner(False, self.shadows[3], self.shadows[2])[::-1]])

    def fill(self):
        top_bottom = [
            [self.palette[1]]*(self.size-8),
            [self.palette[2]]*(self.size-8),
            [self.palette[3]]*(self.size-8),
            [self.palette[3]]*(self.size-8),
        ]
        top_bottom_shaded = [
            [self.palette[1]]*(self.size-8),
            [self.palette[2]]*(self.size-8),
            [self.palette[4]]*(self.size-8),
            [self.palette[3]]*(self.size-8)
        ]
        left_right = [
            *[[self.palette[1], self.palette[2], *[self.palette[3]]*2]]*(self.size-8)
        ]
        left_right_shaded = [
            *[[self.palette[1], self.palette[2], self.palette[4], self.palette[3]]]*(self.size-8)
        ]
        # 2
        if self.shadows[0]:
            self.bitmap.insert_at(4, 0, top_bottom_shaded)
        else:
            self.bitmap.insert_at(4, 0, top_bottom)
        # 4
        if self.shadows[1]:
            self.bitmap.insert_at(0, 4, left_right_shaded)
        else:
            self.bitmap.insert_at(0, 4, left_right)
        # 6
        if self.shadows[2]:
            self.bitmap.insert_at(self.calculated, 4, [item[::-1] for item in left_right_shaded])
        else:
            self.bitmap.insert_at(self.calculated, 4, [item[::-1] for item in left_right])
        # 8
        if self.shadows[3]:
            self.bitmap.insert_at(4, self.calculated, top_bottom_shaded[::-1])
        else:
            self.bitmap.insert_at(4, self.calculated, top_bottom[::-1])
        # 5
        self.bitmap.insert_at(4, 4, [
            *[[*[self.palette[3]]*(self.size-8)]]*(self.size-8)
        ])
    
    def build(self):
        self.corners()
        self.fill()
        return self.bitmap

class NewButtonImage():
    @staticmethod
    def new_long_button(
                        width: int, 
                        height: int, 
                        hover: bool = False, 
                        unavailable: bool = False, 
                        rounded_corners: Union[bool, tuple, list] = [True, True, True, True], 
                        shadows: Union[bool, tuple, list] = [True, True, False, False]) -> Image.Image:
        button = ButtonLong(width, height, hover, unavailable, rounded_corners, shadows)
        bitmap = button.build()
        arr = array(bitmap(), dtype=uint8)
        new_image = Image.fromarray(arr)
        return new_image

    @staticmethod
    def new_square_button(
                          size: int,
                          hover: bool = False,
                          unavailable: bool = False,
                          rounded_corners: Union[bool, tuple, list] = [True, True, True, True],
                          shadows: Union[bool, tuple, list] = [True, False, False, False]) -> Image.Image:
        button = ButtonSquare(size, hover, unavailable, rounded_corners, shadows=shadows)
        bitmap = button.build()
        arr = array(bitmap(), dtype=uint8)
        new_image = Image.fromarray(arr)
        return new_image
    
    @staticmethod
    def new(
            width: int,
            height: int,
            hover: bool = False,
            unavailable: bool = False,
            rounded_corners: Union[bool, tuple, list] = [True, True, True, True],
            shadows: Union[bool, tuple, list] = [True, False, False, False]) -> Image.Image:
        if width == height:
            button = ButtonSquare(width, hover, unavailable, rounded_corners, shadows)
        else:
            button = ButtonLong(width, height, hover, unavailable, rounded_corners, shadows)
        bitmap = button.build()
        arr = array(bitmap(), dtype=uint8)
        new_image = Image.fromarray(arr)
        return new_image
