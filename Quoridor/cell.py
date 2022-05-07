import pygame


class Cell:
    # coordonatele nodurilor ()
    wall_width = 11  # numar impar
    cell_background = (255, 255, 255)
    wall_color = (0, 0, 0)

    def __init__(self, left, top, w, h, display, line, col, interface, code=0):
        self.square = pygame.Rect(left-2, top-2, w-2, h-2)
        self.display = display
        self.color = self.__class__.cell_background
        self.wall = [None, None, None, None]
        self.coord = (line, col)
        self.code = code

        if line > 0:
            self.wall[0] = pygame.Rect(
                left, top - 1 - self.__class__.wall_width // 2, w, self.__class__.wall_width)
        else:
            self.code += 2 ** 0
        if col < interface.columns - 1:
            self.wall[1] = pygame.Rect(
                left + w - self.__class__.wall_width // 2, top, self.__class__.wall_width, h)
        else:
            self.code += 2 ** 1
        if line < interface.lines - 1:
            self.wall[2] = pygame.Rect(
                left, top + h - self.__class__.wall_width // 2, w, self.__class__.wall_width)
        else:
            self.code += 2 ** 2
        if col > 0:
            self.wall[3] = pygame.Rect(
                left - 1 - self.__class__.wall_width // 2, top, self.__class__.wall_width, h)
        else:
            self.code += 2 ** 3

    def __repr__(self):
        return str(self.code)

    def draw(self, color=(255, 255, 255)):

        pygame.draw.rect(self.display, color, self.square)
        # bit masks=[1,2,4,8]
        self.draw_wall()

    def draw_wall(self):
        bit_mask = 1
        for i in range(4):
            if self.code & bit_mask:
                if self.wall[i]:
                    pygame.draw.rect(self.display, self.__class__.wall_color, self.wall[i])
            bit_mask *= 2

    def has_wall_up(self):
        # up mask = 1
        return self.code & 1 == 1

    def has_wall_right(self):
        # right mask = 2
        return self.code & 2 == 2

    def has_wall_down(self):
        # down mask = 4
        return self.code & 4 == 4

    def has_wall_left(self):
        return self.code & 8 == 8
