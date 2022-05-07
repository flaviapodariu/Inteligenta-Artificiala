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

    def move_pawn(self, cell):
        l_player = self.player.position[0]
        c_player = self.player.position[1]

        prev_moves = self.get_valid_moves()  # getting prev moves before pawn update
        for move in prev_moves:
            move.draw()

        self.player.update_pos(cell.coord)

        self.board.draw_pawn(self.player.pawn_img, cell)

        self.board.board[l_player][c_player].draw()

        pygame.display.update()

    def mini_max(self):
        pass

    def alpha_beta(self):
        pass
