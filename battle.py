import pygame
import sys
from setting import *
import os
from pokemon import *
import pygame
import sys
from pokemon import Pokemon
from setting import WINDOW_WIDTH, WINDOW_HEIGHT

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

        scale_size = (int(WINDOW_WIDTH * 0.20), int(WINDOW_WIDTH * 0.20))
        self.player_img = pygame.transform.scale(
            pygame.image.load(f"image/pokemon/{player_pokemon.name}.png").convert_alpha(),
            scale_size
        )

        boss_path = f"image/boss_yim/{wild_pokemon.name}.png"
        normal_path = f"image/pokemon/{wild_pokemon.name}.png"
        if os.path.exists(boss_path):
            sprite = pygame.image.load(boss_path).convert_alpha()
        else:
            sprite = pygame.image.load(normal_path).convert_alpha()

        self.wild_img = pygame.transform.scale(sprite, scale_size)

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
        path = path_map.get(element_type, "image/skill/scratch.png")
        return pygame.image.load(path).convert_alpha()

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
            title = fighting_font.render("FIGHTING!", True, (200, 0, 0))
            self.screen.blit(title, (WINDOW_WIDTH // 2 - title.get_width() // 2, 20))

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
            self.screen.blit(self.bg, (0, 0))
            self.draw_pokemon()
            title = fighting_font.render("FIGHTING!", True, (200, 0, 0))
            self.screen.blit(title, (WINDOW_WIDTH // 2 - title.get_width() // 2, 20))

            if len(self.player_team) > 1:
                msg = tip_font.render("PRESS 1 TO CHANGE POKEMON", True, (0, 0, 0))
                box = pygame.Surface((msg.get_width() + 40, msg.get_height() + 20))
                box.fill((255, 240, 240))
                pygame.draw.rect(box, (255, 0, 0), box.get_rect(), 3)
                box.blit(msg, (20, 10))
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

class TripleBattleScene:
    def __init__(self, screen, player_team, enemy_team):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font("Fonts/Arabica/ttf/Arabica.ttf", 24)

        self.bg = pygame.image.load("image/fight/sand.png").convert()

        self.player_team = player_team
        self.enemy_team = enemy_team

        self.sprite_size = (96, 96)
        self.padding_x = 100
        self.y_positions = [100, 250, 400]

        self.player_positions = [(self.padding_x, y) for y in self.y_positions]
        self.enemy_positions = [(WINDOW_WIDTH - self.padding_x - self.sprite_size[0], y) for y in self.y_positions]

        self.player_sprites = [
            pygame.transform.scale(pygame.image.load(f"image/pokemon/{mon.name}.png"), self.sprite_size)
            for mon in self.player_team
        ]
        self.enemy_sprites = [
            pygame.transform.scale(pygame.image.load(f"image/boss_yim/{mon.name}.png"), self.sprite_size)
            for mon in self.enemy_team
        ]

        self.state = "player_phase"
        self.current_player_index = 0
        self.current_target_index = 0
        self.delay_timer = 0
        self.delay_interval = 800

    def draw_health_bar(self, x, y, mon):
        ratio = mon.hp / mon.max_hp
        pygame.draw.rect(self.screen, (255, 255, 255), (x, y, 110, 16))
        pygame.draw.rect(self.screen, (0, 0, 0), (x, y, 110, 16), 2)
        pygame.draw.rect(self.screen, (0, 255, 0), (x + 2, y + 2, max(0, 106 * ratio), 12))
        name = self.font.render(mon.name.upper(), True, (0, 0, 0))
        self.screen.blit(name, (x, y - 22))

    def play_attack_animation(self, attacker, target_pos):
        type_map = {"Normal": "scratch", "Fire": "fire", "Water": "splash", "Grass": "green"}
        sprite = pygame.image.load(f"image/skill/{type_map.get(attacker.element_type, 'scratch')}.png").convert_alpha()
        for i in range(4):
            frame = sprite.subsurface((i * 192, 0, 192, 192))
            self.draw_scene()
            self.screen.blit(frame, target_pos)
            pygame.display.flip()
            pygame.time.delay(100)

    def attack(self, attacker, defender):
        if attacker.hp <= 0 or defender.hp <= 0:
            return
        bonus = 20 if (attacker.element_type, defender.element_type) in [("Water", "Fire"), ("Fire", "Grass"), ("Grass", "Water")] else 0
        defender.hp = max(0, defender.hp - (attacker.base_attack + bonus))

    def draw_scene(self):
        self.screen.blit(self.bg, (0, 0))

        # 🔺 แสดงคำว่า BATTLE ด้านบน
        title_font = pygame.font.Font("Fonts/Arabica/ttf/Arabica.ttf", 60)
        battle_title = title_font.render("BATTLE", True, (200, 0, 0))
        self.screen.blit(battle_title, (WINDOW_WIDTH // 2 - battle_title.get_width() // 2, 20))

        # 🔺 วาดทีมผู้เล่น
        for i, mon in enumerate(self.player_team):
            self.screen.blit(self.player_sprites[i], self.player_positions[i])
            self.draw_health_bar(self.player_positions[i][0], self.player_positions[i][1] - 30, mon)

        # 🔺 วาดทีมบอส YIM
        for i, mon in enumerate(self.enemy_team):
            self.screen.blit(self.enemy_sprites[i], self.enemy_positions[i])
            self.draw_health_bar(self.enemy_positions[i][0], self.enemy_positions[i][1] - 30, mon)

        # 🔺 UI ข้างล่างแบบใช้ฟอนต์ที่รองรับ Unicode ลูกศร
        ui_font = pygame.font.SysFont(None, 26)
        # แทน ← / → ด้วยข้อความแทน
        tip = ui_font.render("LEFT / RIGHT : TARGET   |   ENTER : ATTACK", True, (0, 0, 0))
        self.screen.blit(tip, (WINDOW_WIDTH // 2 - tip.get_width() // 2, WINDOW_HEIGHT - 40))

        # 🔺 กรอบแดงรอบศัตรูที่ถูกเลือก
        if self.state == "player_phase":
            targetable = [e for e in self.enemy_team if e.hp > 0]
            if targetable:
                selected = targetable[self.current_target_index % len(targetable)]
                index = self.enemy_team.index(selected)
                x, y = self.enemy_positions[index]
                pygame.draw.rect(self.screen, (255, 0, 0),
                                 (x - 4, y - 4, self.sprite_size[0] + 8, self.sprite_size[1] + 8), 3)

    def show_result(self, text):
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        font = pygame.font.Font("Fonts/Arabica/ttf/Arabica.ttf", 80)
        label = font.render(text, True, (255, 255, 255))
        rect = label.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        self.screen.blit(label, rect)
        pygame.display.flip()
        pygame.time.delay(2000)

    def run(self):
        while True:
            self.draw_scene()
            pygame.display.update()

            if all(p.hp <= 0 for p in self.player_team):
                self.show_result("LOSER")
                return "lose"
            if all(e.hp <= 0 for e in self.enemy_team):
                self.show_result("WINNER")
                return "win"

            now = pygame.time.get_ticks()

            if self.state == "player_phase":
                attacker = self.player_team[self.current_player_index]
                if attacker.hp <= 0:
                    self.current_player_index += 1
                    if self.current_player_index >= len(self.player_team):
                        self.state = "enemy_phase"
                    continue

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.KEYDOWN:
                        targetable = [e for e in self.enemy_team if e.hp > 0]
                        if not targetable:
                            continue
                        if event.key == pygame.K_LEFT:
                            self.current_target_index = (self.current_target_index - 1) % len(targetable)
                        elif event.key == pygame.K_RIGHT:
                            self.current_target_index = (self.current_target_index + 1) % len(targetable)
                        elif event.key == pygame.K_RETURN:
                            target = targetable[self.current_target_index % len(targetable)]
                            self.play_attack_animation(attacker, self.enemy_positions[self.enemy_team.index(target)])
                            self.attack(attacker, target)
                            self.current_player_index += 1
                            if self.current_player_index >= len(self.player_team):
                                self.state = "enemy_phase"

            elif self.state == "enemy_phase" and now - self.delay_timer > self.delay_interval:
                for i in range(len(self.enemy_team)):
                    attacker = self.enemy_team[i]
                    if attacker.hp <= 0:
                        continue
                    if i >= len(self.player_team):
                        break
                    defender = self.player_team[i]
                    if defender.hp <= 0:
                        continue
                    self.play_attack_animation(attacker, self.player_positions[i])
                    self.attack(attacker, defender)
                    self.draw_scene()
                    pygame.display.update()
                    pygame.time.delay(500)

                self.state = "player_phase"
                self.current_player_index = 0
                self.delay_timer = now

            self.clock.tick(60)
