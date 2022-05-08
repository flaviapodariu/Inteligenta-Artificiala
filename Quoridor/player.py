import pygame
from game import *


class Player:

    def __init__(self, pos, player_type, scope, img_path, walls=10):
        self.position = pos
        self.type = player_type
        self.scope = scope
        pawn_img = pygame.image.load(img_path)

        self.pawn_img = pygame.transform.scale(
            pawn_img, (Game.pawn_size, Game.pawn_size))

        self.walls = walls

    def update_pos(self, pos):
        self.position = pos


