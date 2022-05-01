import pygame
import sys


class Cell:
    # coordonatele nodurilor ()
    wall_width = 11  # numar impar
    cell_background = (255, 255, 255)
    gap_color = (0,  0, 0)

    def __init__(self, left, top, w, h, display, line, col, interface, code=0):
        self.square = pygame.Rect(left, top, w, h)
        self.display = display
        self.wall = [None, None, None, None]
        # wallurile vor fi pe pozitiile 0-sus, 1-dreapta, 2-jos, 3-stanga
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

        # print(self.wall)
        # 0001 wall doar sus
        # 0011 wall sus si dreapta etc

    def draw(self):
        pygame.draw.rect(self.display, self.__class__.cell_background, self.square)
        # bit masks=[1,2,4,8]
        bit_mask = 1
        for i in range(4):
            if self.code & bit_mask:
                if self.wall[i]:
                    pygame.draw.rect(self.display, self.__class__.gap_color, self.wall[i])
            bit_mask *= 2



class Interface:
    screen_color = (0, 0, 0)
    cell_size = 50
    cell_padding = 5
    img_size = cell_size - 2 * cell_padding

    def __init__(self, lines=9, columns=9, screen=None):
        self.lines = lines
        self.columns = columns
        self.screen = screen

        self.board = [[Cell(display=screen, left=col * (self.__class__.cell_size + 1),
                            top=lin * (self.__class__.cell_size + 1),
                            w=self.__class__.cell_size,
                            h=self.__class__.cell_size,
                            line=lines,
                            col=columns,
                            interface=self)
                       for col in range(columns)] for lin in range(lines)]

        player1 = pygame.image.load('blue_pawn.png')
        self.player1 = pygame.transform.scale(
            player1, (self.__class__.img_size, self.__class__.img_size))

        player2 = pygame.image.load('red_pawn.png')
        self.player2 = pygame.transform.scale(
            player2, (self.__class__.img_size, self.__class__.img_size))

    def draw_image(self, img, cell):
        self.screen.blit(img, (cell.square.left + self.__class__.cell_padding,
                               cell.square.top + self.__class__.cell_padding))

    def draw_initial_state(self):
        self.screen.fill(self.__class__.screen_color)
        for line in self.board:
            for cell in line:
                cell.draw()
        self.draw_image(self.player1, self.board[0][self.columns // 2])
        self.draw_image(self.player2, self.board[self.lines-1][self.columns // 2])
        pygame.display.update()


pygame.init()

screen = pygame.display.set_mode(size=(460, 460))

pygame.display.set_caption("Flavia Podariu - Quoridor")

interf = Interface(lines=9, columns=9, screen=screen)


interf.draw_initial_state()
# bucla jocului care imi permite sa tot fac mutari

while True:
    for ev in pygame.event.get():
        #daca utilizatorul face click pe x-ul de inchidere a ferestrei
        if ev.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_i:
                interf.draw_initial_state()
            pygame.display.update()
