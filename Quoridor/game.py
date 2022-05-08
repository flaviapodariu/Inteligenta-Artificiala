from cell import Cell
import pygame

# starting lines of the players in the initial state
# reverse the values and you get the players' aimed line
PLAYER2_HOME = 0  # PMAX
PLAYER1_HOME = 8  # PMIN


class Game:
    PMIN = None
    PMAX = None
    screen_color = (140, 145, 146)
    cell_size = 70
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
                            line=lin,
                            col=col,
                            interface=self) for col in range(columns)]
                      for lin in range(lines)]
        # default values
        player1 = pygame.image.load('img/red_pawn.png')
        player2 = pygame.image.load('img/blue_pawn.png')

        self.player1 = pygame.transform.scale(
            player1, (self.__class__.img_size, self.__class__.img_size))
        self.player2 = pygame.transform.scale(
            player2, (self.__class__.img_size, self.__class__.img_size))

    def __repr__(self):
        debug_board = ""
        for line in self.board:
            for cell in line:
                debug_board += str(cell) + " "
            debug_board += "\n"

        return debug_board

    def set_pawns(self):
        if self.__class__.PMIN == "blue":
            player1 = pygame.image.load('img/blue_pawn.png')
            player2 = pygame.image.load('img/red_pawn.png')
        else:
            return

        self.player1 = pygame.transform.scale(
            player1, (self.__class__.img_size, self.__class__.img_size))
        self.player2 = pygame.transform.scale(
            player2, (self.__class__.img_size, self.__class__.img_size))

    def draw_pawn(self, pawn, cell):
        self.screen.blit(pawn, (cell.square.left + self.__class__.cell_padding,
                                cell.square.top + self.__class__.cell_padding))

    def draw_initial_state(self):
        self.screen.fill(self.__class__.screen_color)
        for line in self.board:
            for cell in line:
                cell.draw()

        self.draw_pawn(self.player1, self.board[self.lines - 1][self.columns // 2])
        self.draw_pawn(self.player2, self.board[0][self.columns // 2])
        pygame.display.update()

    def draw_vertical_wall(self, found_wall):
        i = found_wall[0]
        j = found_wall[1]
        wall_idx = found_wall[2]
        self.board[i][j].code |= 2 ** wall_idx
        self.board[i + 1][j].code |= 2 ** wall_idx
        self.board[i][j].draw_wall()
        self.board[i + 1][j].draw_wall()

    def draw_horizontal_wall(self, found_wall):
        i = found_wall[0]
        j = found_wall[1]
        wall_idx = found_wall[2]
        self.board[i][j].code |= 2 ** wall_idx
        self.board[i][j + 1].code |= 2 ** wall_idx
        self.board[i][j].draw_wall()
        self.board[i][j + 1].draw_wall()

    def is_wall_valid(self, found_wall, direction="horizontal"):
        i = found_wall[0]
        j = found_wall[1]
        wall_idx = found_wall[2]
        if direction == "horizontal":
            if self.board[i][j + 1].has_wall_type(wall_idx):
                # not enough space for a new wall
                return False
            if self.board[i][j].has_wall_right() and self.board[i + 1][j].has_wall_right():
                # new wall cannot be perforate an existing vertical wall
                return False
        elif direction == "vertical":
            if self.board[i + 1][j].has_wall_type(wall_idx):
                return False
            if self.board[i][j].has_wall_down() and self.board[i][j + 1].has_wall_down():
                return False
        else:
            print("Wrong wall type!")
            return False
        return True

    def pause(self):
        pass
