import pygame
from game import *


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
            print(f"Gave over! {winner}. Press 'r' to play again.")

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
