# battle.py
import pygame

class BattleScene:
    def __init__(self, screen, player_pokemon, wild_pokemon):
        self.screen = screen
        self.player_pokemon = player_pokemon
        self.wild_pokemon = wild_pokemon
        self.bg = pygame.image.load("image/fight/forest.png")

    def run(self):
        # ง่ายๆก่อน: แค่แสดงโปเกม่อน 2 ตัวและชนะอัตโนมัติ
        running = True
        clock = pygame.time.Clock()
        while running:
            self.screen.blit(self.bg, (0, 0))

            font = pygame.font.Font(None, 50)
            text1 = font.render(f"You: {self.player_pokemon.name}", True, (0, 0, 0))
            text2 = font.render(f"Enemy: {self.wild_pokemon.name}", True, (0, 0, 0))
            self.screen.blit(text1, (100, 200))
            self.screen.blit(text2, (100, 300))

            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                    running = False
            clock.tick(60)