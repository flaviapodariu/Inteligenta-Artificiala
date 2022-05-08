import pygame
import sys
from game import Game
from state import *
from menu import *
from player import Player
from copy import deepcopy
from time import time, sleep

MAX_DEPTH = 4
LINES = 9
COLUMNS = 9
ORANG = 'img/orang.png'
MAN = 'img/meme_man.png'

"""
TO DO:
    -> fix timer on pause
    -> in: State, valid_pawn_move(), treat case to jump over pawn
    -> BUG in: game_over(), press 'r' to play again  
"""


def set_game():
    pygame.init()
    size = 70 * 9 + 5
    screen = pygame.display.set_mode(size=(size, size))

    pygame.display.set_caption("Flavia Podariu - Quoridor")
    board = Game(lines=LINES, columns=COLUMNS, screen=screen)
    # settings made by player
    algo, Game.PMIN, depth = draw_options_screen(screen, board)  # player is PMIN
    board.set_pawns()

    Game.PMAX = "Orang" if Game.PMIN == "Man" else "Man"  # assign other pawn to computer
    pawn_h = ORANG if Game.PMIN == "Orang" else MAN
    pawn_ai = ORANG if Game.PMAX == "Orang" else MAN
    human = Player((LINES - 1, COLUMNS // 2), Game.PMIN, PLAYER2_HOME, pawn_h)
    ai = Player((0, COLUMNS // 2), Game.PMAX, PLAYER1_HOME, pawn_ai)

    curr_state = State(board, human, ai, depth)

    curr_state.board.draw_initial_state()
    print("Game has started!\n", board)
    return board, curr_state, algo


def play(board, curr_state, algorithm):
    pawn_selected = False
    paused = False
    t1 = int(round(time()))
    while True:
        if curr_state.player.type == Game.PMIN:
            print("It's player's turn!\n")
            paused, pawn_selected, curr_state = player_turn(paused, pawn_selected, curr_state, board, t1)

            curr_state.player.type = Game.PMAX  # change player's turn
            curr_state.opponent.type = Game.PMIN
        #
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
        #
        #     curr_state.player = Game.PMIN


def player_turn(paused, pawn_selected, curr_state, board, t1):
    ignore_time = 0
    not_done = True
    while not_done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # #################  KEY EVENTS  #######################
            if event.type == pygame.KEYDOWN:
                if event.type == pygame.K_a:
                    print(curr_state.is_final_state())
                    if curr_state.game_over():
                        new_board, new_state, algo = set_game()
                        play(new_board, new_state, algo)
                        pygame.quit()
                        sys.exit()
                    # pygame.quit()
                    # sys.exit()

                if event.key == pygame.K_p:
                    if not paused:
                        t2 = int(round(time()))
                        paused = curr_state.pause()
                        print(f"Current game time is: {t2 - t1 - ignore_time} seconds")
                        print("Game is paused.Press 'p' to resume.")
                    else:
                        paused = curr_state.resume()
                        # ignore_time = int(round(time())) - t2  t2 referenced before assignment
                        print("Game is resumed.")

            # ####################### CLICK ###########################################
            if event.type == pygame.MOUSEBUTTONDOWN and not paused:
                pos = pygame.mouse.get_pos()
                found_walls = []
                for line_idx, line in enumerate(curr_state.board.board):
                    for cell_idx, cell in enumerate(line):
                        if cell.square.collidepoint(pos):
                            if cell.coord == curr_state.player.position:
                                if not pawn_selected:
                                    pawn_selected = True
                                    curr_state.show_valid_moves()
                                else:
                                    pawn_selected = False
                                    curr_state.stop_showing_valid_moves()
                            elif pawn_selected and curr_state.valid_pawn_move(cell):
                                curr_state.move_pawn(cell)
                                pawn_selected = False
                                not_done = False

                        # WALL PLACEMENT
                        for wall_idx, wall in enumerate(cell.wall):
                            if wall and wall.collidepoint(pos) and not pawn_selected:
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
                    not_done = False
    return paused, pawn_selected, curr_state


init_board, init_state, algorithm = set_game()
play(init_board, init_state, algorithm)


