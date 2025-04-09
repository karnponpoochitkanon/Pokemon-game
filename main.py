import sys
import pygame.display
from setting import *
from os.path import isfile, join
from pytmx.util_pygame import load_pygame

class Main:
    def __init__(self):
        pygame.init()
        self.display = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Pokemon')

    def import_assets(self):
        self.maps = {'world': load_pygame(join('assets', 'map.tmx')),}

    @staticmethod
    def run():
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()

if __name__ == '__main__':
    game = Main()
    game.run()