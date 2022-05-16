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
    -> BUG in: game_over(), press 'r' to play again  
"""


def set_game():
    pygame.init()
    size = 70 * 9 + 5
    screen = pygame.display.set_mode(size=(size, size))

    pygame.display.set_caption("Flavia Podariu - Quoridor")
    board = Game(lines=LINES, columns=COLUMNS, screen=screen)
    # settings made by player
    algo, Game.PMIN, depth, game_type = draw_options_screen(screen, board)  # player is PMIN
    board.set_pawns()

    Game.PMAX = "Orang" if Game.PMIN == "Man" else "Man"  # assign other pawn to computer
    pawn_h = ORANG if Game.PMIN == "Orang" else MAN
    pawn_ai = ORANG if Game.PMAX == "Orang" else MAN
    human = Player((LINES - 1, COLUMNS // 2), Game.PMIN, PLAYER2_HOME, pawn_h)
    ai = Player((0, COLUMNS // 2), Game.PMAX, PLAYER1_HOME, pawn_ai)

    curr_state = State(board, human, ai, int(depth))

    curr_state.board.draw_initial_state()
    print("Game has started!\n", board)
    return board, curr_state, algo, game_type


def p_vs_ai(board, curr_state, algorithm):
    t_start = int(round(time()))
    ai_thinking_times = []
    nodes_stats = []
    human_moves = 0
    ai_moves = 0
    depth = curr_state.tree_depth
    while True:
        if curr_state.player.type == Game.PMIN:
            t1_h = int(round(time()))
            human_moves += 1
            print("It's player's turn!\n")
            curr_state = player_turn(curr_state, board, t_start, human_moves, ai_moves,
                                     ai_thinking_times, nodes_stats)
            t2_h = int(round(time()))
            print(f"Player took {t2_h - t1_h}s to make a move.")
            print("Board after player's move:\n", curr_state.board)

            curr_state.game_over(t_start, ai_thinking_times, nodes_stats)
            if not curr_state.is_final_state():
                curr_state.change_turns()

        else:
            curr_state.tree_depth = depth
            ai_moves += 1
            print("It's computer's turn!\n")
            pc_t1 = int(round(time() * 1000))
            if algorithm == "minimax":
                new_state, nodes = curr_state.mini_max()
            else:
                new_state, nodes = curr_state.alpha_beta(-500, 500)

            curr_state = new_state.best_move
            curr_state.draw_changes()
            nodes_stats.append(nodes)

            pc_t2 = int(round(time() * 1000))
            pc_thinks = pc_t2 - pc_t1

            ai_thinking_times.append(pc_thinks)

            print("Board after computer's move:\n", curr_state.board)
            print(f"Computer took {pc_thinks} ms to make a move.")
            print(f"Move estimation = {new_state.estimation}")
            print(f"Number of nodes in memory: {nodes}")
            print(f"Last move changes: {curr_state.changes}\n")
            print(curr_state.player)
            print(curr_state.opponent)
            # best move is the state after the pc made its move so the players are already switched
            # we need to switch the players back in case game is over so we get the correct winner
            curr_state.change_turns()
            curr_state.game_over(t_start, ai_thinking_times, nodes_stats)
            # switch players back to normal so human can play their turn
            curr_state.change_turns()
            pygame.display.update()


def p_vs_p(board, curr_state):
    t_start = int(round(time()))
    p1_moves = p2_moves = 0
    while True:

        if curr_state.player.type == Game.PMIN:
            print("It's player's turn!\n")
            curr_state = player_turn(curr_state, board, t_start, p1_moves, p2_moves)
            print(f"Board after {curr_state.player.type}'s move:\n", curr_state.board)
            print(curr_state.player.walls, curr_state.opponent.walls)
            curr_state.game_over(t_start)
            curr_state.change_turns()
        else:
            print("It's player's turn!\n")
            curr_state = player_turn(curr_state, board, t_start, p1_moves, p2_moves)
            print(f"Board after {curr_state.player.type}'s  move:\n", curr_state.board)
            curr_state.game_over(t_start)
            print(curr_state.opponent.walls, curr_state.player.walls)
            curr_state.change_turns()


def ai_vs_ai(curr_state, algo):
    t_start = int(round(time()))
    ai1_thinking_times = ai2_thinking_times = []
    nodes_stats = []
    ai1_moves = 0
    ai2_moves = 0
    depth = curr_state.tree_depth
    while True:
        curr_state.tree_depth = depth
        if curr_state.player.type == Game.PMIN:
            curr_state = ai_turn(curr_state, depth, ai1_moves, algo, ai1_thinking_times, t_start, "1", 0)
        else:
            curr_state = ai_turn(curr_state, depth, ai2_moves, algo, ai2_thinking_times, t_start, "2", 0)
        pygame.display.update()


def player_turn(curr_state, board, t1, h_moves, ai_moves, ai_times=[], nodes_stats=[]):
    ignore_time = 0
    not_done = True
    copied = False
    paused = False
    pawn_selected = False
    undoed = False
    new_state = State.copy_state(curr_state)
    while not_done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                t2 = int(round(time()))
                print(f"Game has been running for {t2 - t1}s")
                print(f"Player made {h_moves} moves.")
                print(f"Computer made {ai_moves} moves.")
                pygame.quit()
                sys.exit()
            # #################  KEY EVENTS  #######################
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    t2 = int(round(time()))
                    print(f"Game has been running for {t2 - t1}s")
                    print(f"Player made {h_moves} moves.")
                    print(f"Computer made {ai_moves} moves.")
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_u:
                    if curr_state.prev_move.prev_move is None:
                        print("There is nothing to undo!!")
                    else:
                        undoed = True
                        undo_state = curr_state.prev_move.prev_move
                        undo_state.draw_current_state()

                if event.key == pygame.K_r:
                    start_game()
                if event.key == pygame.K_p:
                    if undoed:
                        curr_state = State.copy_state(undo_state)
                    if not paused:
                        t2 = int(round(time()))
                        paused = curr_state.board.pause(ai_times, nodes_stats, ai_moves, h_moves)
                        print(f"Current game time is: {t2 - t1} seconds")
                        print("Game is paused.Press 'p' to resume.")
                    else:
                        paused = curr_state.resume()
                        print("Game is resumed.")

            # ####################### CLICK ###########################################
            if event.type == pygame.MOUSEBUTTONDOWN and not paused:
                if undoed and not copied:
                    copied = True
                    curr_state = State.copy_state(undo_state)
                    curr_state.prev_move = curr_state.prev_move.prev_move
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
                                old_pawn = curr_state.player.position
                                new_state.move_pawn(cell)
                                new_state.draw_pawn_after_move(old_pawn)
                                pawn_selected = False
                                undoed = False
                                not_done = False

                        # WALL PLACEMENT
                        for wall_idx, wall in enumerate(cell.wall):
                            if wall and wall.collidepoint(pos) and not pawn_selected:
                                found_walls.append((line_idx, cell_idx, wall_idx))
                if len(found_walls) == 2 and curr_state.player.walls > 0:
                    if found_walls[0][1] == found_walls[1][1] and found_walls[0][1] < board.columns - 1:
                        if new_state.board.is_wall_valid(found_walls[0]):
                            new_state.board.add_horizontal_wall(found_walls[0], draw=True)
                            new_state.board.add_horizontal_wall(found_walls[1], draw=True)
                            new_state.player.walls -= 1
                            undoed = False
                            not_done = False
                        else:
                            found_walls = []
                            not_done = True
                            print("Not a valid wall position!!")
                    elif found_walls[0][0] < board.lines - 1:
                        if new_state.board.is_wall_valid(found_walls[0], "vertical"):
                            new_state.board.add_vertical_wall(found_walls[0], draw=True)
                            new_state.board.add_vertical_wall(found_walls[1], draw=True)
                            new_state.player.walls -= 1
                            undoed = False
                            not_done = False
                        else:
                            found_walls = []
                            not_done = True
                            print("Not a valid wall position!!")
                    pygame.display.update()

    return new_state


def ai_turn(curr_state, depth, ai_moves, algorithm, ai_thinking_times, t_start, est_f, nodes):
    curr_state.tree_depth = depth
    ai_moves += 1
    print(f"It's computer{est_f}'s turn!\n")
    pc_t1 = int(round(time() * 1000))
    if algorithm == "minimax":
        new_state, nodes = curr_state.mini_max(est_f)
    else:
        new_state, nodes = curr_state.alpha_beta(-500, 500, nodes, est_f)

    new_state.best_move.draw_changes()
    curr_state = new_state.best_move

    pc_t2 = int(round(time() * 1000))
    pc_thinks = pc_t2 - pc_t1

    ai_thinking_times.append(pc_thinks)

    print(f"Board after computer{est_f}'s move:\n", curr_state.board)
    print(f"Computer{est_f} took {pc_thinks} ms to make a move.")
    print(f"Move estimation = {new_state.estimation}")
    print(f"Number of nodes in memory: {nodes}")
    print(f"Last move changes: {curr_state.changes}\n")
    print(curr_state.player)
    print(curr_state.opponent)
    curr_state.change_turns()
    curr_state.game_over(t_start, ai_thinking_times, [])
    curr_state.change_turns()
    return curr_state


def start_game():
    init_board, init_state, algorithm, game_type = set_game()
    if game_type == "p-ai":
        p_vs_ai(init_board, init_state, algorithm)
    elif game_type == "p-p":
        p_vs_p(init_board, init_state)
    else:
        ai_vs_ai(init_state, algorithm)

start_game()
