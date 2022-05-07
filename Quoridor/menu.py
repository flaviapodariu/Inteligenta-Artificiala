import pygame
import sys


class Button:
    def __init__(self, display=None, left=0, top=0, w=0, h=0, backgr_color=(53, 80, 115),
                 selected_color=(0, 100, 55), text="",
                 font="arial", font_size=16, text_color=(255, 255, 255),
                 value=""):
        self.display = display
        self.backgr_color = backgr_color
        self.selected_color = selected_color
        self.text = text
        self.font = font
        self.w = w
        self.h = h
        self.selected = False
        self.font_size = font_size
        self.text_color = text_color
        # creez obiectul font
        font_object = pygame.font.SysFont(self.font, self.font_size)
        self.rendered_text = font_object.render(self.text, True, self.text_color)
        self.box = pygame.Rect(left, top, w, h)
        # aici centram textul
        self.box_text = self.rendered_text.get_rect(center=self.box.center)
        self.value = value

    def select(self, sel):
        self.selected = sel
        self.draw()

    def select_by_coord(self, coord):
        if self.box.collidepoint(coord):
            self.select(True)
            return True
        return False

    def update_box(self):
        self.box.left = self.left
        self.box.top = self.top
        self.box_text = self.rendered_text.get_rect(center=self.box.center)

    def draw(self):
        option_color = self.selected_color if self.selected else self.backgr_color

        pygame.draw.rect(self.display, option_color, self.box)
        self.display.blit(self.rendered_text, self.box_text)


class ButtonGroup:
    def __init__(self, button_lst=[], selected_idx=0, button_space=10, left=0, top=0):
        self.button_lst = button_lst
        self.selected_idx = selected_idx
        self.button_lst[self.selected_idx].selected = True
        self.top = top
        self.left = left
        leftCurent = self.left
        for b in self.button_lst:
            b.top = self.top
            b.left = leftCurent
            b.update_box()
            leftCurent += (button_space + b.w)

    def select_by_coord(self, coord):
        for ib, b in enumerate(self.button_lst):
            if b.select_by_coord(coord):
                self.button_lst[self.selected_idx].select(False)
                self.selected_idx = ib
                return True
        return False

    def draw(self):
        # atentie, nu face wrap
        for b in self.button_lst:
            b.draw()

    def get_value(self):
        return self.button_lst[self.selected_idx].value


def draw_options_screen(display, initial_board):
    algo_btn = ButtonGroup(
        top=30,
        left=30,
        button_lst=[
            Button(display=display, w=80, h=30, text="MINIMAX", value="minimax"),
            Button(display=display, w=120, h=30, text="ALPHA-BETA", value="alphabeta")
        ],
        selected_idx=1)

    player_btn = ButtonGroup(
        top=100,
        left=30,
        button_lst=[
            Button(display=display, w=45, h=30, text="RED", value="red"),
            Button(display=display, w=55, h=30, text="BLUE", value="blue")
        ],
        selected_idx=0)

    difficulty_btn = ButtonGroup(
        top=170,
        left=30,
        button_lst=[
            Button(display=display, w=55, h=30, text="EASY", value="easy"),
            Button(display=display, w=80, h=30, text="MEDIUM", value="med"),
            Button(display=display, w=55, h=30, text="HARD", value="hard")
        ],
        selected_idx=0)

    start = Button(display=display, top=240, left=30, w=65, h=30, text="START", backgr_color=(155, 0, 55))
    algo_btn.draw()
    player_btn.draw()
    difficulty_btn.draw()
    start.draw()
    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif ev.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if not algo_btn.select_by_coord(pos):
                    if not player_btn.select_by_coord(pos):
                        if not difficulty_btn.select_by_coord(pos):
                            if start.select_by_coord(pos):
                                display.fill((0, 0, 0))  # stergere ecran
                                initial_board.draw_initial_state()
                                return algo_btn.get_value(), player_btn.get_value(), difficulty_btn.get_value()
        pygame.display.update()
