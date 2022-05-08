import pygame
import sys
from game import Game
from state import *
from menu import *
from player import Player
import time

MAX_DEPTH = 4
LINES = 9
COLUMNS = 9
RED = 'img/red_pawn.png'
BLUE = 'img/blue_pawn.png'

"""
TO DO:
    -> BUG: wall placement when pawn is selected
    -> class Game functions
    -> in: State, valid_pawn_move(), treat case to jump over pawn
    -> pause button
    
    
    -> in: game_over(), TEST press 'r' to play again 
"""


# only start checking for wall placement validity when player has 5 walls left


def set_game():
    pygame.init()
    size = 70 * 9 + 5
    screen = pygame.display.set_mode(size=(size, size))

    pygame.display.set_caption("Flavia Podariu - Quoridor")
    board = Game(lines=LINES, columns=COLUMNS, screen=screen)
    # settings made by player
    algorithm, Game.PMIN, depth = draw_options_screen(screen, board)  # player is PMIN
    board.set_pawns()

    Game.PMAX = "red" if Game.PMIN == "blue" else "blue"  # assign other pawn to computer
    pawn_color_h = RED if Game.PMIN == "red" else BLUE
    pawn_color_ai = RED if Game.PMAX == "red" else BLUE
    human = Player((LINES - 1, COLUMNS // 2), "PMIN", PLAYER2_HOME, pawn_color_h)
    ai = Player((0, COLUMNS // 2), "PMAX", PLAYER1_HOME, pawn_color_ai)

    curr_state = State(board, human, ai, depth)

    board.draw_initial_state()
    print("Game has started!\n", board)
    return board, curr_state


def play(board, curr_state):
    while True:
        # if curr_state.player == Game.PMIN:
        #     print("It's player's turn!\n")

        # if curr_state.game_over():
        #     for event in pygame.event.get():
        #         if event.type == pygame.K_r:
        #             set_game()
        #             play()
        #     return

        # curr_state.player = Game.PMAX  # change player's turn

        for event in pygame.event.get():
            # daca utilizatorul face click pe x-ul de inchidere a ferestrei
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # #################  KEY EVENTS  #######################
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    board.pause()
                    print("Game is paused.Press 'p' to resume.")
                pygame.display.update()
            if event.type == pygame.MOUSEMOTION:
                pass
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                found_walls = []
                for line_idx, line in enumerate(curr_state.board.board):
                    for cell_idx, cell in enumerate(line):
                        if cell.square.collidepoint(pos):
                            if cell.coord == curr_state.player.position:
                                curr_state.show_valid_moves()
                            if curr_state.valid_pawn_move(cell):
                                curr_state.move_pawn(cell)

                        for wall_idx, wall in enumerate(cell.wall):
                            if wall and wall.collidepoint(pos):
                                found_walls.append((line_idx, cell_idx, wall_idx))
                if len(found_walls) == 2:
                    if found_walls[0][1] == found_walls[1][1] and found_walls[0][1] < board.columns - 1:
                        if curr_state.board.is_wall_valid(found_walls[0]):
                            curr_state.board.draw_horizontal_wall(found_walls[0])
                            curr_state.board.draw_horizontal_wall(found_walls[1])
                    elif found_walls[0][0] < board.lines - 1:
                        if curr_state.board.is_wall_valid(found_walls[0], "vertical"):
                            curr_state.board.draw_vertical_wall(found_walls[0])
                            curr_state.board.draw_vertical_wall(found_walls[1])
                    pygame.display.update()

    # else:
    #     print("It's computer's turn!\n")
    #     pc_t1 = int(round(time() * 1000))
    #     if algorithm == "MINIMAX":
    #         pc_move = curr_state.mini_max()
    #     else:
    #         pc_move = curr_state.alpha_beta()
    #
    #     curr_state.board = pc_move.best_move.board
    #
    #     pc_t2 = int(round(time() * 1000))
    #     print(f"Computer took {pc_t2 - pc_t1} ms to make a move.\n")
    #
    #     print("Board after computer's move:\n", curr_state.board)
    #     if curr_state.game_over():
    #         for event in pygame.event.get():
    #             if event.type == pygame.K_r:
    #                 set_game()
    #                 play()
    #         return
    #
    #     curr_state.player = Game.PMIN


init_board, init_state = set_game()
play(init_board, init_state)
