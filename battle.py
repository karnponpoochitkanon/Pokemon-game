import pygame
import sys
from setting import *

class BattleScene:
    def __init__(self, screen, player_pokemon, wild_pokemon, player_team):
        self.screen = screen
        self.player_pokemon = player_pokemon
        self.wild_pokemon = wild_pokemon
        self.bg = pygame.image.load("image/fight/forest.png")
        self.player_team = player_team

        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font("Fonts/Arabica/ttf/Arabica.ttf", 28)

        self.battle_over = False

        # Positions
        scale_size = (int(WINDOW_WIDTH * 0.20), int(WINDOW_WIDTH * 0.20))
        self.player_img = pygame.transform.scale(
            pygame.image.load(f"image/pokemon/{player_pokemon.name}.png").convert_alpha(),
            scale_size
        )
        self.wild_img = pygame.transform.scale(
            pygame.image.load(f"image/pokemon/{wild_pokemon.name}.png").convert_alpha(),
            scale_size
        )

        self.player_pos = (80, 280)
        self.wild_pos = (910, 280)

    def draw_health_bar(self, x, y, hp, max_hp, name_text):
        ratio = hp / max_hp
        name_surf = self.font.render(name_text, True, (0, 0, 0))

        box_rect = pygame.Rect(x - 10, y - 10, 225, 50)
        pygame.draw.rect(self.screen, (255, 255, 255), box_rect, border_radius=12)
        pygame.draw.rect(self.screen, (0, 0, 0), box_rect, 3, border_radius=12)

        self.screen.blit(name_surf, (x, y - 8))
        pygame.draw.rect(self.screen, (0, 0, 0), (x, y + 18, 200, 14), border_radius=8)
        pygame.draw.rect(self.screen, (0, 255, 0), (x, y + 18, 200 * ratio, 14), border_radius=8)

    def draw_pokemon(self):
        self.screen.blit(self.player_img, self.player_pos)
        self.screen.blit(self.wild_img, self.wild_pos)
        self.draw_health_bar(self.player_pos[0], self.player_pos[1] - 50, self.player_pokemon.hp, self.player_pokemon.max_hp, f"YOU: {self.player_pokemon.name.upper()}")
        self.draw_health_bar(self.wild_pos[0], self.wild_pos[1] - 50, self.wild_pokemon.hp, self.wild_pokemon.max_hp, f"WILD: {self.wild_pokemon.name.upper()}")

    def get_attack_animation(self, element_type):
        path_map = {
            "Normal": "image/skill/scratch.png",
            "Fire": "image/skill/fire.png",
            "Water": "image/skill/splash.png",
            "Grass": "image/skill/green.png"
        }
        return pygame.image.load(path_map.get(element_type, "image/skill/scratch.png")).convert_alpha()

    def play_attack_animation(self, element_type, target_pos):
        sprite_sheet = self.get_attack_animation(element_type)
        frame_width, frame_height = 192, 192
        num_frames = 4

        fighting_font = pygame.font.Font("Fonts/Arabica/ttf/Arabica.ttf", 64)
        tip_font = pygame.font.Font("Fonts/Arabica/ttf/Arabica.ttf", 28)

        for i in range(num_frames):
            frame = sprite_sheet.subsurface(pygame.Rect(i * frame_width, 0, frame_width, frame_height))
            self.screen.blit(self.bg, (0, 0))
            self.draw_pokemon()

            # ✅ แสดง FIGHTING!
            title = fighting_font.render("FIGHTING!", True, (200, 0, 0))
            self.screen.blit(title, (WINDOW_WIDTH // 2 - title.get_width() // 2, 20))

            # ✅ แสดงปุ่ม "PRESS 1 TO CHANGE POKEMON" ถ้ามีมากกว่า 1 ตัว
            if len(self.player_team) > 1:
                msg = tip_font.render("PRESS 1 TO CHANGE POKEMON", True, (0, 0, 0))
                box = pygame.Surface((msg.get_width() + 40, msg.get_height() + 20))
                box.fill((255, 240, 240))
                pygame.draw.rect(box, (255, 0, 0), box.get_rect(), 3)
                box.blit(msg, (20, 10))
                self.screen.blit(box, (30, WINDOW_HEIGHT - box.get_height() - 30))

            self.screen.blit(frame, target_pos)
            pygame.display.flip()
            pygame.time.delay(100)

    def get_attack_bonus(self, attacker, defender):
        advantage = {
            "Water": "Fire",
            "Fire": "Grass",
            "Grass": "Water"
        }
        if advantage.get(attacker.element_type) == defender.element_type:
            return 20
        return 0

    def run(self):
        fighting_font = pygame.font.Font("Fonts/Arabica/ttf/Arabica.ttf", 64)
        tip_font = pygame.font.Font("Fonts/Arabica/ttf/Arabica.ttf", 28)

        def draw_ui():
            # BG + Pokemon
            self.screen.blit(self.bg, (0, 0))
            self.draw_pokemon()

            # FIGHTING!
            title = fighting_font.render("FIGHTING!", True, (200, 0, 0))
            self.screen.blit(title, (WINDOW_WIDTH // 2 - title.get_width() // 2, 20))

            # ✅ แสดงปุ่มเปลี่ยนโปเกม่อนถ้ามีมากกว่า 1 ตัว
            if len(self.player_team) > 1:
                msg = tip_font.render("PRESS 1 TO CHANGE POKEMON", True, (0, 0, 0))
                box = pygame.Surface((msg.get_width() + 40, msg.get_height() + 20))
                box.fill((255, 240, 240))
                pygame.draw.rect(box, (255, 0, 0), box.get_rect(), 3)
                box.blit(msg, (20, 10))

                # ✅ วางที่มุมล่างซ้าย
                self.screen.blit(box, (30, WINDOW_HEIGHT - box.get_height() - 30))

        while True:
            draw_ui()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN and not self.battle_over:
                    if event.key == pygame.K_SPACE:
                        bonus = self.get_attack_bonus(self.player_pokemon, self.wild_pokemon)
                        self.play_attack_animation(self.player_pokemon.element_type, self.wild_pos)
                        self.wild_pokemon.hp -= self.player_pokemon.base_attack + bonus

                        if self.wild_pokemon.hp <= 0:
                            return "win"

                        bonus = self.get_attack_bonus(self.wild_pokemon, self.player_pokemon)
                        self.play_attack_animation(self.wild_pokemon.element_type, self.player_pos)
                        self.player_pokemon.hp -= self.wild_pokemon.base_attack + bonus

                        if self.player_pokemon.hp <= 0:
                            return "lose"

                    elif event.key == pygame.K_1:
                        if len(self.player_team) > 1:
                            return "run"

            pygame.display.flip()
            self.clock.tick(60)