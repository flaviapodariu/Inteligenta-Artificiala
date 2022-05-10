import pygame
from queue import Queue
from game import *
from copy import deepcopy
MAX_SCORE = 99

class State:

    def __init__(self, board, player, opp, tree_depth, prev_move=None, estimation=None):
        self.board = board
        self.player = player
        self.opponent = opp
        self.tree_depth = tree_depth
        self.prev_move = prev_move
        self.estimation = estimation
        self.possible_moves = []
        self.best_move = None

    def is_final_state(self):
        return self.player.position[0] == self.player.scope

    def game_over(self):
        winner = "Computer has " if self.player.type == "PMAX" else "You have "
        print(self.is_final_state())
        if self.is_final_state():
            print(f"Gave over! {winner} won. Press 'r' to play again.")

    def BFS(self):
        q = Queue()
        q.put(self)
        n_moves_away = 0
        while not q.empty():
            curr_state = q.get()
            if curr_state.is_final_state():
                return n_moves_away
            n_moves_away += 1
            curr_state.set_possible_moves()
            for move in curr_state.possible_moves:
                if move.possible_moves is []:  # not expanded yet
                    q.put(move)


    @classmethod
    def advantage(cls, what_player):
        return 0

    def estimate_move(self):
        if self.is_final_state():
            best_score = self.tree_depth + MAX_SCORE
            if self.player.scope == PLAYER1_HOME:
                self.estimation = best_score
            else:
                self.estimation = -best_score
        else:
            self.estimation = self.advantage(self.player) - self.advantage(self.opponent)

    def set_possible_moves(self):
        # adding wall related moves
        self.wall_placements()
        # adding pawn related moves
        pawn_moves = self.get_valid_moves()
        for pawn_pos in pawn_moves:
            new_state = deepcopy(self)
            new_state.move_pawn(pawn_pos)
            new_state.player, new_state.opponent = new_state.opponent, new_state.player
            new_state.tree_depth = self.tree_depth - 1
            new_state.prev_move = self
            self.possible_moves.append(new_state)

    def wall_placements(self):
        """
        :return: nothing (construct the list of possible wall placements in a game state(used in BFS))
        """
        for i, line in enumerate(self.board.board):
            for j, cell in enumerate(line):
                for wall in range(cell.wall):
                    found_wall = (i, j, wall)
                    direction = "horizontal" if wall == 0 or wall == 3 else "vertical"
                    if self.board.is_wall_valid(found_wall, direction):
                        new_board = deepcopy(self.board)
                        if direction == "horizontal":
                            new_board.board.draw_horizontal_wall(found_wall)
                        else:
                            new_board.board.draw_vertical_wall(found_wall)
                        new_state = State(new_board, self.opponent, self.player, self.tree_depth-1, self)
                        self.possible_moves.append(new_state)

    def valid_pawn_move(self, cell) -> bool:
        """

        :param cell:  cell to move pawn on
        If cell is on the pawn's RIGHT, we have to check for a wall on the cells' LEFT
        Same for every direction
        """
        pawn = self.player.position
        if cell.coord[0] == pawn[0] - 1 and cell.coord[1] == pawn[1]:
            # cell is up
            if not cell.has_wall_down():
                return True
        if cell.coord[0] == pawn[0] + 1 and cell.coord[1] == pawn[1]:
            # cell is down
            if not cell.has_wall_up():
                return True
        if cell.coord[0] == pawn[0] and cell.coord[1] == pawn[1] - 1:
            # cell is on left
            if not cell.has_wall_right():
                return True
        if cell.coord[0] == pawn[0] and cell.coord[1] == pawn[1] + 1:
            # cell is on right
            if not cell.has_wall_left():
                return True

        return False

    def get_valid_moves(self):
        directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        moves = []
        l = self.player.position[0]
        c = self.player.position[1]
        for d in directions:
            if 0 <= l + d[0] < self.board.lines and \
                    0 <= c + d[1] < self.board.columns:
                move = self.board.board[l + d[0]][c + d[1]]
                if self.valid_pawn_move(move):
                    moves.append(move)
        return moves

    def show_valid_moves(self):
        moves = self.get_valid_moves()
        for move in moves:
            move.draw(color=(144, 235, 222))
        pygame.display.update()

    def stop_showing_valid_moves(self):
        prev_moves = self.get_valid_moves()
        for move in prev_moves:
            move.draw()
        pygame.display.update()

    def move_pawn(self, cell):
        l_player = self.player.position[0]
        c_player = self.player.position[1]
        self.stop_showing_valid_moves()  # deleting prev moves before pawn update
        self.player.update_pos(cell.coord)

        self.board.draw_pawn(self.player.pawn_img, cell)

        self.board.board[l_player][c_player].draw()

        pygame.display.update()

    def draw_current_state(self):
        self.board.screen.fill(self.board.__class__.screen_color)
        for line in self.board.board:
            for cell in line:
                cell.draw()
        pl1_i, pl1_j = self.player.position
        pl2_i, pl2_j = self.opponent.position
        self.board.draw_pawn(self.player.pawn_img, self.board.board[pl1_i][pl1_j])
        self.board.draw_pawn(self.opponent.pawn_img, self.board.board[pl2_i][pl2_j])
        pygame.display.update()

    def pause(self):
        self.board.screen.blit(self.board.pause_backgr, (0, 0))
        pygame.display.update()
        return True

    def resume(self):
        self.draw_current_state()
        return False

    def mini_max(self):
        pass

    def alpha_beta(self):
        pass
