import pygame
from game import *
from copy import deepcopy


class Player:

    def __init__(self, pos, player_type, scope, img_path, walls=10):
        self.position = pos
        self.type = player_type
        self.scope = scope
        self.path = img_path  # just for copying
        self.img = pygame.image.load(img_path)

        self.pawn_img = pygame.transform.scale(
            self.img, (Game.pawn_size, Game.pawn_size))

        self.walls = walls

    def __repr__(self):
        out = self.type + " is at position (" + str(self.position[0]) + ", " + str(self.position[1]) + ") and has " + \
              str(self.walls) + " walls left"
        return out

    def update_pos(self, pos):
        self.position = pos

    @staticmethod
    def copy_player(player):
        new_player = Player(player.position, player.type, player.scope, player.path, player.walls)
        new_player.position = deepcopy(player.position)
        new_player.walls = deepcopy(player.walls)
        return new_player
