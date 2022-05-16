from time import sleep, time
from queue import Queue
from player import *

MAX_SCORE = 99
MIN_SIGN = -1
MAX_SIGN = 1


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
        self.changes = None

    def __repr__(self):
        human_text = "\nHuman is at position "
        pc_text = "\nComputer is at position "
        text1 = human_text if self.player.type == Game.PMIN else pc_text
        text2 = pc_text if self.player.type == Game.PMIN else human_text
        out = str(self.board) + text1 + str(self.player.position) + \
              text2 + str(self.opponent.position)
        return out

    @staticmethod
    def copy_state(state):
        new_player = Player.copy_player(state.player)
        new_opp = Player.copy_player(state.opponent)
        new_game = Game.copy_game(state.board)
        new_depth = deepcopy(state.tree_depth)
        new_state = State(new_game, new_player, new_opp, new_depth, state)
        new_state.changes = deepcopy(state.changes)
        if state.estimation is not None:
            new_state.estimation = deepcopy(state.estimation)
        return new_state

    def change_turns(self):
        self.player, self.opponent = self.opponent, self.player

    def is_final_state(self):
        return self.player.position[0] == self.player.scope

    def game_over(self, t_start, thinking_times=[], nodes=[]):
        t_end = int(round(time()))
        winner = "Computer has " if self.player.type == Game.PMAX else "You have "
        if self.is_final_state():
            i = self.player.position[0]
            j = self.player.position[1]
            self.board.board[i][j].draw((252, 39, 39))  # mark the winner's cell with red
            self.board.draw_pawn(self.player.pawn_img, self.board.board[i][j])
            sleep(1)
            self.board.end_of_game(thinking_times, nodes)
            pygame.display.update()
            print(f"Total time: {t_end - t_start}s")
            print(f"Game over! {winner} won. Press 'r' to play again.")

    def estimation_f1(self, sign):
        extra = 0
        # avoid placing random walls that have the same estimation with other better choices
        if len(self.changes) == 3:
            if self.player.type == Game.PMAX:
                if self.changes[0] <= self.opponent.position[0]:
                    return -sign * MAX_SCORE
            else:
                if self.changes[0] >= self.opponent.position[0]:
                    return sign * MAX_SCORE
            if self.opponent.walls < 6:
                extra = self.opponent.walls
        else:
            if self.player.type == Game.PMAX:
                if self.changes[0] < self.player.position[0]:
                    extra = 1
            else:
                if self.changes[0] > self.player.position[0]:
                    extra = 1
        # we decrease the number of lines until the player's scope * 1(MAX) or -1 (MIN)
        return -sign * (self.player.scope - self.player.position[0] - extra)

    def estimation_f2(self):
        """
        :return: the min number of steps to go until reaching the next closer line to the scope
        """
        q = Queue()
        q.put(self.player.position)
        scope = self.player.position[0] + 1 if self.player.type == Game.PMAX else self.player.position[0] - 1
        n_moves_away = 0
        visited = set()
        while not q.empty():
            cell_coord = q.get()
            if cell_coord[1] == scope:
                return n_moves_away
            n_moves_away += 1
            visited.add(cell_coord)
            moves = self.get_valid_moves(custom_pos=cell_coord)
            for move in moves:
                if move not in visited:  # not expanded yet
                    q.put(move.coord)
        return n_moves_away

    def estimate_move(self, estimation_f="1"):
        if self.is_final_state():
            best_score = self.tree_depth + MAX_SCORE
            if self.player.scope == PLAYER1_HOME:
                self.estimation = best_score
            else:
                self.estimation = -best_score
        else:
            sign = MAX_SIGN if self.player.type == Game.PMAX else MIN_SIGN
            if estimation_f == "1":
                self.estimation = self.estimation_f1(sign)
            else:
                self.estimation = -sign * (MAX_SCORE - self.estimation_f2())

    def set_possible_moves(self):
        # adding wall related moves
        player_moves = []
        if self.player.walls > 0:
            player_moves = self.wall_placements()
        # adding pawn related moves
        pawn_moves = self.get_valid_moves()
        for pawn_pos in pawn_moves:
            new_state = self.__class__.copy_state(self)
            new_state.changes = self.player.position
            new_state.player.update_pos(pawn_pos.coord)
            player_moves.append(new_state)
        opp_moves = []
        for move in player_moves:
            opp_state = self.__class__.copy_state(move)
            opp_state.tree_depth -= 1
            opp_state.change_turns()
            opp_moves.append(opp_state)
        self.possible_moves = opp_moves

    @staticmethod
    def compute_other_wall(direction, found_wall):
        i = found_wall[0]
        j = found_wall[1]
        wall = found_wall[2]
        other_idx = (wall + 2) % 4  # the opposite wall (the wall of the neighbouring cell)
        if direction == "horizontal":
            if wall == 0:
                other_wall = (i - 1, j, other_idx)
            else:
                other_wall = (i + 1, j, other_idx)
        else:
            if wall == 1:
                other_wall = (i, j + 1, other_idx)
            else:
                other_wall = (i, j - 1, other_idx)
        return other_wall

    def wall_placements(self):
        """
        :return:  the list of possible wall placements in a game state(used in BFS)
        """
        lst = []
        for i, line in enumerate(self.board.board):
            for j, cell in enumerate(line):
                for wall in range(len(cell.wall)):
                    found_wall = (i, j, wall)
                    direction = "horizontal" if wall == 0 or wall == 2 else "vertical"
                    if self.board.is_wall_valid(found_wall, direction):
                        new_state = self.__class__.copy_state(self)
                        new_state.changes = found_wall
                        other_wall = self.compute_other_wall(direction, found_wall)
                        if direction == "horizontal":
                            new_state.board.add_horizontal_wall(found_wall)
                            new_state.board.add_horizontal_wall(other_wall)
                        else:
                            new_state.board.add_vertical_wall(found_wall)
                            new_state.board.add_vertical_wall(other_wall)
                        lst.append(new_state)
        return lst

    def valid_pawn_move(self, cell) -> bool:
        """

        :param cell:  cell to move pawn on
        If cell is on the pawn's RIGHT, we have to check for a wall on the cells' LEFT
        Same for every direction
        """
        pawn = self.player.position
        opp = self.opponent.position
        if self.board.jumps_over(self.player, self.opponent, cell):
            return True
        if self.board.jumps_diagonally(self.player, self.opponent, cell):
            return True

        if cell.coord != opp:
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

    def get_valid_moves(self, custom_pos=None):
        directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        moves = []
        if custom_pos is None:
            l = self.player.position[0]
            c = self.player.position[1]
        else:
            l = custom_pos[0]
            c = custom_pos[1]

        for d in directions:
            if 0 <= l + d[0] < self.board.lines and \
                    0 <= c + d[1] < self.board.columns:
                move = self.board.board[l + d[0]][c + d[1]]
                if self.valid_pawn_move(move):
                    moves.append(move)

        if self.player.type == Game.PMAX:
            # jumping over pawn case
            if 0 <= l + 2 < self.board.lines:
                move = self.board.board[l + 2][c]
                if self.valid_pawn_move(move):
                    moves.append(move)

            if 0 <= l + 1 < self.board.lines and 0 <= c - 1 < self.board.columns:
                move = self.board.board[l + 1][c - 1]
                if self.valid_pawn_move(move):
                    moves.append(move)
            if 0 <= l + 1 < self.board.lines and 0 <= c + 1 < self.board.columns:
                move = self.board.board[l + 1][c - 1]
                if self.valid_pawn_move(move):
                    moves.append(move)
        else:
            if 0 <= l - 2 < self.board.lines:
                move = self.board.board[l - 2][c]
                if self.valid_pawn_move(move):
                    moves.append(move)
            if 0 <= l - 1 < self.board.lines and 0 <= c - 1 < self.board.columns:
                move = self.board.board[l - 1][c - 1]
                if self.valid_pawn_move(move):
                    moves.append(move)
            if 0 <= l - 1 < self.board.lines and 0 <= c + 1 < self.board.columns:
                move = self.board.board[l - 1][c - 1]
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
        self.stop_showing_valid_moves()  # deleting prev possible moves before pawn update
        self.player.update_pos(cell.coord)

    def draw_pawn_after_move(self, last_pos, h_turn=True):
        l_player = last_pos[0]
        c_player = last_pos[1]
        if h_turn:
            i = self.player.position[0]
            j = self.player.position[1]
            self.board.draw_pawn(self.player.pawn_img, self.board.board[i][j])
        else:
            i = self.opponent.position[0]
            j = self.opponent.position[1]
            self.board.draw_pawn(self.opponent.pawn_img, self.board.board[i][j])

        self.board.board[l_player][c_player].draw()

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

    def resume(self):
        # draw the board again after a pause and return False (if resumed => pause = False)
        self.draw_current_state()
        return False

    def best_move_wall_changes(self):
        # set changes to the new state (best move) after the end of the algorithm
        found_wall = self.changes
        i = found_wall[0]
        j = found_wall[1]
        wall = found_wall[2]

        direction = "horizontal" if wall == 0 or wall == 2 else "vertical"
        other_wall = self.compute_other_wall(direction, found_wall)

        self.board.board[i][j].draw_wall()
        if direction == "horizontal":
            self.board.board[other_wall[0]][other_wall[1] + 1].draw_wall()
        else:
            self.board.board[other_wall[0] + 1][other_wall[1]].draw_wall()

    def mini_max(self, estimation_f="1", nodes=0):
        if self.tree_depth == 0 or self.is_final_state():
            self.estimate_move(estimation_f)
            return self, nodes
        self.set_possible_moves()
        nodes += len(self.possible_moves)
        moves_with_estimation = [state.mini_max("1", nodes)[0] for state in self.possible_moves]
        if self.player.type == Game.PMAX:  # player is PMAX
            self.best_move = max(moves_with_estimation, key=lambda x: x.estimation)
        else:
            self.best_move = min(moves_with_estimation, key=lambda x: x.estimation)

        self.estimation = self.best_move.estimation
        self.board = Game.copy_game(self.best_move.board)
        return self, nodes

    def alpha_beta(self, alpha, beta, nodes=0, estimation_f="1"):
        # nodes = n of nodes in memory
        if self.tree_depth == 0 or self.is_final_state():
            self.estimate_move(estimation_f)
            return self, nodes

        if alpha > beta:
            return self, nodes  # este intr-un interval invalid deci nu o mai procesez

        self.set_possible_moves()
        nodes += len(self.possible_moves)
        if self.player.type == Game.PMAX:
            curr_estimation = float('-inf')  # in aceasta variabila calculam maximul

            for move in self.possible_moves:
                # calculeaza estimarea pentru starea noua, realizand subarborele
                new_state = move.alpha_beta(alpha, beta, nodes, "1")[0]  # aici construim subarborele pentru next_state

                if curr_estimation < new_state.estimation:
                    self.best_move = new_state
                    curr_estimation = new_state.estimation

                if alpha < new_state.estimation:
                    alpha = new_state.estimation
                    if alpha >= beta:  # interval invalid
                        break

        elif self.player.type == Game.PMIN:
            curr_estimation = float('inf')
            for move in self.possible_moves:
                # calculeaza estimarea
                new_state = move.alpha_beta(alpha, beta, nodes, "1")[0]  # aici construim subarborele pentru starea_noua

                if curr_estimation > new_state.estimation:
                    self.best_move = new_state
                    curr_estimation = new_state.estimation
                if beta > new_state.estimation:
                    beta = new_state.estimation
                    if alpha >= beta:
                        break
        if len(self.best_move.changes) == 3:
            self.best_move.opponent.walls -= 1

        self.estimation = self.best_move.estimation
        return self, nodes

    def draw_changes(self):
        # called only inside mini_max() or alpha_beta() after best move is chosen
        if len(self.changes) == 3:
            self.best_move_wall_changes()
        elif len(self.changes) == 2:
            self.draw_pawn_after_move(self.changes, False)
        pygame.display.update()

