from cell import Cell
import pygame
from statistics import median

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
    pawn_size = cell_size - 2 * cell_padding

    def __init__(self, lines=9, columns=9, screen=None):
        self.lines = lines
        self.columns = columns
        self.screen = screen

        self.board = [[Cell(display=screen, left=col * (self.__class__.cell_size + 1),
                            top=lin * (self.__class__.cell_size + 1),
                            w=self.__class__.cell_size,
                            h=self.__class__.cell_size,
                            line=lin,
                            col=col) for col in range(columns)]
                      for lin in range(lines)]
        # default values
        player1 = pygame.image.load('img/orang.png')
        player2 = pygame.image.load('img/meme_man.png')
        pause_backgr = pygame.image.load("img/paused.png")

        self.player1 = pygame.transform.scale(
            player1, (self.__class__.pawn_size, self.__class__.pawn_size))
        self.player2 = pygame.transform.scale(
            player2, (self.__class__.pawn_size, self.__class__.pawn_size))
        self.pause_backgr = pygame.transform.scale(
            pause_backgr, (pygame.display.get_surface().get_size()))

    @staticmethod
    def copy_game(game):
        new_game = Game(game.lines, game.columns, game.screen)
        new_game.board = [[game.board[lin][col].copy_cell() for col in range(game.columns)] for lin in
                          range(game.lines)]

        return new_game

    def __repr__(self):
        debug_board = ""
        for line in self.board:
            for cell in line:
                debug_board += str(cell) + " "
            debug_board += "\n"

        return debug_board

    def set_pawns(self):
        if self.__class__.PMIN == "Man":
            player1 = pygame.image.load('img/meme_man.png')
            player2 = pygame.image.load('img/orang.png')
        else:
            return

        self.player1 = pygame.transform.scale(
            player1, (self.__class__.pawn_size, self.__class__.pawn_size))
        self.player2 = pygame.transform.scale(
            player2, (self.__class__.pawn_size, self.__class__.pawn_size))

    def draw_pawn(self, pawn, cell):
        self.screen.blit(pawn, (cell.square.left + self.__class__.cell_padding,
                                cell.square.top + self.__class__.cell_padding))
        pygame.display.update()

    def draw_initial_state(self):
        self.screen.fill(self.__class__.screen_color)
        for line in self.board:
            for cell in line:
                cell.draw()

        self.draw_pawn(self.player1, self.board[self.lines - 1][self.columns // 2])
        self.draw_pawn(self.player2, self.board[0][self.columns // 2])
        pygame.display.update()

    def add_vertical_wall(self, found_wall, draw=False):
        i = found_wall[0]
        j = found_wall[1]
        wall_idx = found_wall[2]
        if i >= self.lines - 1:
            return False
        self.board[i][j].code |= 2 ** wall_idx
        self.board[i + 1][j].code |= 2 ** wall_idx
        if draw:
            self.board[i][j].draw_wall()
            self.board[i + 1][j].draw_wall()
        return True

    def add_horizontal_wall(self, found_wall, draw=False):
        i = found_wall[0]
        j = found_wall[1]
        wall_idx = found_wall[2]
        if j >= self.columns - 1:
            return False
        self.board[i][j].code |= 2 ** wall_idx
        self.board[i][j + 1].code |= 2 ** wall_idx
        if draw:
            self.board[i][j].draw_wall()
            self.board[i][j + 1].draw_wall()
        return True

    def is_wall_valid(self, found_wall, direction="horizontal"):
        i = found_wall[0]
        j = found_wall[1]
        wall_idx = found_wall[2]

        if self.board[i][j].has_wall_type(wall_idx):
            return False

        if i == 0 and wall_idx == 0:
            return False
        if j == 0 and wall_idx == 3:
            return False
        if i == self.lines - 1 and wall_idx == 2:
            return False
        if j == self.columns - 1 and wall_idx == 1:
            return False

        if direction == "horizontal":
            if j < self.columns - 1 and self.board[i][j + 1].has_wall_type(wall_idx):
                # not enough space for a new wall
                return False
            if i < self.lines - 1:
                if self.board[i][j].has_wall_right() and self.board[i + 1][j].has_wall_right():
                    # new wall cannot perforate an existing vertical wall
                    return False
        elif direction == "vertical":
            if i < self.lines - 1 and self.board[i + 1][j].has_wall_type(wall_idx):
                return False
            if j < self.columns - 1:
                if self.board[i][j].has_wall_down() and self.board[i][j + 1].has_wall_down():
                    return False
        else:
            print("Wrong wall type!")
            return False
        return True

    def jumps_over(self, player, opp, cell):
        ip = player.position[0]
        jp = player.position[1]
        io = opp.position[0]
        jo = opp.position[1]
        if player.type == self.__class__.PMIN:
            if cell.coord == (io - 1, jo) == (ip - 2, jp):
                if not cell.has_wall_down() and not self.board[ip][jp].has_wall_up():
                    return True
        else:
            if cell.coord == (io + 1, jo) == (ip + 2, jp):
                if not cell.has_wall_up() and not self.board[ip][jp].has_wall_down():
                    return True
        return False

    def jumps_diagonally(self, player, opp, cell):
        ip = player.position[0]
        jp = player.position[1]
        pawn = self.board[ip][jp]
        io = opp.position[0]
        jo = opp.position[1]
        other_pawn = self.board[io][jo]

        if pawn.has_wall_left() and pawn.has_wall_right():
            if not self.jumps_over(player, opp, cell):
                if not other_pawn.has_wall_left() and not other_pawn.has_wall_right():
                    if cell.coord == (io, jo - 1) or cell.coord == (io, jo + 1):
                        return True
                elif other_pawn.has_wall_left() and not other_pawn.has_wall_right():
                    if cell.coord == (io, jo + 1):
                        return True
                elif other_pawn.has_wall_right() and not other_pawn.has_wall_left():
                    if cell.coord == (io, jo - 1):
                        return True
        return False

    def pause(self, ai_times, nodes, h_moves, ai_moves):
        self.screen.blit(self.pause_backgr, (0, 0))
        pygame.font.init()
        pause_text = pygame.font.SysFont("Comic Sans", 20)
        pause_surface = pause_text.render("Press 'p' to resume game", False, (249, 120, 22))
        self.screen.blit(pause_surface, (40, 5))
        self.get_generic_stats("PC computed thinking times:", "ms", ai_times)
        self.get_generic_stats("Tree nodes stats:", "", nodes, 5, 70)
        self.get_player_moves(h_moves)
        self.get_ai_moves(ai_moves)
        pygame.display.update()
        return True

    def get_generic_stats(self, message, v_type, values, h=0, space=0):
        t = self.__class__.generic_stats(values)
        if t is None:
            return
        pygame.font.init()
        values = pygame.font.SysFont("Comic Sans", 20)
        gen_surf = values.render(message, False, (249, 120, 22))
        gen_val_surf = values.render(f"MIN= {t[0]} {v_type}, MED= {t[1]}{v_type}, MAX= {t[2]}{v_type}, MEDIAN= {t[3]}{v_type}", False, (249, 120, 22))
        self.screen.blit(gen_surf, (15, 40+space))
        self.screen.blit(gen_val_surf, (15, 65+h+space))

    def get_player_moves(self, h_moves, p=""):
        pygame.font.init()
        moves_text = pygame.font.SysFont("Comic Sans", 20)
        moves_surf = moves_text.render(f"Player{p} number of moves: {h_moves}", True, (249, 120, 22))
        self.screen.blit(moves_surf, (15, 180))

    def get_ai_moves(self, ai_moves):
        pygame.font.init()
        moves_text = pygame.font.SysFont("Comic Sans", 20)
        moves_surf = moves_text.render(f"Computer number of moves: {ai_moves}", True, (249, 120, 22))
        self.screen.blit(moves_surf, (15, 200))

    @staticmethod
    def generic_stats(values):
        if not values:
            return 0, 0, 0, 0
        maxi = max(values)
        mini = min(values)
        med = (maxi + mini) // 2
        mediann = median(values)
        print("Computer stats (thinking time):")
        print(f"Minimum: {mini}")
        print(f"Medium: {med}")
        print(f"Maximum: {maxi}")
        print(f"Median: {mediann}")
        return mini, med, maxi, mediann

    def end_of_game(self, ai_times, nodes, game_type="p-ai"):
        self.screen.fill((43, 44, 73))
        pygame.font.init()
        game_over = pygame.font.SysFont("Comic Sans", 40)
        game_over_text = game_over.render("GAME OVER", False, (249, 120, 22))
        self.screen.blit(game_over_text, (100, 200))
        if game_type == "p-ai":
            self.get_generic_stats("PC computed thinking times:", "ms", ai_times)
            self.get_generic_stats("Tree nodes stats:", "", nodes, 5, 70)
        elif game_type == "p-p":
            # self.get_player_moves(h_moves, "1")
            self.get_player_moves(ai_times, "2")
