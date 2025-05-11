import pygame
import sys
import os

class YimFinalBattle:
    def __init__(self, screen, player_team, draw_background_fn=None):
        self.screen = screen
        self.player_team = player_team
        self.draw_background_fn = draw_background_fn
        self.selected = []
        self.font = pygame.font.Font("Fonts/Arabica/ttf/Arabica.ttf", 26)

        self.card_width = 180
        self.card_height = 230
        self.sprite_scale = 80
        self.padding = 20
        self.cursor_index = 0

        self.modal_width = 3 * (self.card_width + self.padding) + self.padding
        self.modal_height = self.card_height + 120
        self.modal_rect = pygame.Rect(
            (screen.get_width() - self.modal_width) // 2,
            (screen.get_height() - self.modal_height) // 2,
            self.modal_width,
            self.modal_height
        )

    def draw(self):
        pygame.draw.rect(self.screen, (255, 255, 255), self.modal_rect, border_radius=12)
        title = self.font.render("CHOOSE UP TO 3 POKEMON TO FIGHT!", True, (0, 0, 0))
        self.screen.blit(title, (self.modal_rect.centerx - title.get_width() // 2, self.modal_rect.y + 20))

        start_x = self.modal_rect.x + self.padding
        y = self.modal_rect.y + 60

        for i, mon in enumerate(self.player_team):
            x = start_x + i * (self.card_width + self.padding)
            card_rect = pygame.Rect(x, y, self.card_width, self.card_height)

            if mon in self.selected:
                bg_color = (220, 255, 220)
                border_color = (0, 200, 0)
            elif i == self.cursor_index:
                bg_color = (255, 255, 255)
                border_color = (0, 0, 255)
            else:
                bg_color = (255, 255, 255)
                border_color = (0, 0, 0)

            pygame.draw.rect(self.screen, bg_color, card_rect, border_radius=8)
            pygame.draw.rect(self.screen, border_color, card_rect, 3, border_radius=8)

            boss_path = f"image/boss_yim/{mon.name}.png"
            normal_path = f"image/pokemon/{mon.name}.png"
            if os.path.exists(boss_path):
                sprite = pygame.image.load(boss_path).convert_alpha()
            else:
                sprite = pygame.image.load(normal_path).convert_alpha()

            sprite = pygame.transform.scale(sprite, (self.sprite_scale, self.sprite_scale))
            self.screen.blit(sprite, (x + (self.card_width - self.sprite_scale) // 2, y + 10))

            name_surf = self.font.render(mon.name.upper(), True, (0, 0, 0))
            self.screen.blit(name_surf, (x + (self.card_width - name_surf.get_width()) // 2, y + 100))

            hp_text = self.font.render(f"{mon.hp}/{mon.max_hp} HP", True, (0, 0, 0))
            self.screen.blit(hp_text, (x + (self.card_width - hp_text.get_width()) // 2, y + 135))

        if self.selected:
            ok_msg = self.font.render("Press O to start battle", True, (0, 100, 0))
            self.screen.blit(ok_msg, (self.modal_rect.centerx - ok_msg.get_width() // 2, self.modal_rect.bottom - 40))

    def run(self):
        running = True
        while running:
            if self.draw_background_fn:
                self.draw_background_fn(self.screen)
            else:
                self.screen.fill((0, 0, 0))

            self.draw()
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.cursor_index = (self.cursor_index - 1) % len(self.player_team)
                    elif event.key == pygame.K_RIGHT:
                        self.cursor_index = (self.cursor_index + 1) % len(self.player_team)
                    elif event.key == pygame.K_SPACE:
                        mon = self.player_team[self.cursor_index]
                        if mon in self.selected:
                            self.selected.remove(mon)
                        elif len(self.selected) < 3:
                            self.selected.append(mon)
                    elif event.key == pygame.K_o and self.selected:
                        return self.selected

    def create_boss_team(self):
        from pokemon import Pokemon
        return [
            Pokemon("piplup", "Water"),
            Pokemon("tanana", "Grass"),
            Pokemon("tong", "Fire")
        ]

class FinalBossSelectionPopup:
    def __init__(self, screen, pokemon_list, font_path="Fonts/Arabica/ttf/Arabica.ttf", draw_background_fn=None):
        self.screen = screen
        self.pokemon_list = pokemon_list
        self.font = pygame.font.Font(font_path, 28)
        self.draw_background_fn = draw_background_fn
        self.clock = pygame.time.Clock()

        self.card_width = 160
        self.card_height = 220
        self.padding = 20
        self.sprite_scale = 100
        self.cards_per_page = 3
        self.page = 0
        self.selected_indices = []
        self.cursor_index = 0
        self.warning_timer = 0

        self.modal_width = self.cards_per_page * (self.card_width + self.padding) + self.padding
        self.modal_height = self.card_height + 160
        self.modal_rect = pygame.Rect(
            (screen.get_width() - self.modal_width) // 2,
            (screen.get_height() - self.modal_height) // 2,
            self.modal_width,
            self.modal_height
        )

    def draw(self):
        pygame.draw.rect(self.screen, (255, 255, 255), self.modal_rect, border_radius=16)
        title = self.font.render("CHOOSE 3 POKEMON TO FIGHT BOSS", True, (0, 0, 0))
        self.screen.blit(title, (self.modal_rect.centerx - title.get_width() // 2, self.modal_rect.y + 20))

        start_index = self.page * self.cards_per_page
        end_index = min(start_index + self.cards_per_page, len(self.pokemon_list))
        visible_pokemon = self.pokemon_list[start_index:end_index]

        start_x = self.modal_rect.x + self.padding
        y = self.modal_rect.y + 60

        for i, pokemon in enumerate(visible_pokemon):
            index = start_index + i
            x = start_x + i * (self.card_width + self.padding)
            card_rect = pygame.Rect(x, y, self.card_width, self.card_height)

            is_selected = index in self.selected_indices
            is_cursor = index == self.cursor_index
            is_fainted = pokemon.hp <= 0

            # สีพื้นหลังและกรอบ
            bg_color = (220, 255, 220) if is_selected else (255, 230, 230) if is_fainted else (255, 255, 255)
            if is_fainted and is_cursor:
                border_color = (255, 0, 0)
            elif is_selected:
                border_color = (0, 200, 0)
            elif is_cursor:
                border_color = (255, 204, 0)
            else:
                border_color = (0, 0, 0)

            pygame.draw.rect(self.screen, bg_color, card_rect, border_radius=12)
            pygame.draw.rect(self.screen, border_color, card_rect, 3, border_radius=12)

            # 🖼 Sprite
            sprite = pygame.image.load(f"image/pokemon/{pokemon.name}.png").convert_alpha()
            sprite = pygame.transform.scale(sprite, (self.sprite_scale, self.sprite_scale))
            self.screen.blit(sprite, (x + (self.card_width - self.sprite_scale) // 2, y + 10))

            name_surf = self.font.render(pokemon.name.upper(), True, (0, 0, 0))
            self.screen.blit(name_surf, (x + (self.card_width - name_surf.get_width()) // 2, y + 120))

            # 🔋 HP Bar
            hp_ratio = pokemon.hp / pokemon.max_hp
            hp_bar_x = x + 10
            hp_bar_y = y + 150
            hp_bar_width = self.card_width - 20
            pygame.draw.rect(self.screen, (0, 0, 0), (hp_bar_x, hp_bar_y, hp_bar_width, 10))
            pygame.draw.rect(self.screen, (0, 255, 0), (hp_bar_x, hp_bar_y, hp_bar_width * hp_ratio, 10))

            hp_text = self.font.render(f"{pokemon.hp}/{pokemon.max_hp} HP", True, (0, 0, 0))
            self.screen.blit(hp_text, (x + (self.card_width - hp_text.get_width()) // 2, hp_bar_y + 12))

        # 📦 ข้อความด้านล่าง
        info = self.font.render(f"Selected: {len(self.selected_indices)} / 3", True, (0, 0, 0))
        self.screen.blit(info, (self.modal_rect.centerx - info.get_width() // 2, self.modal_rect.bottom - 75))

        if len(self.selected_indices) > 0:
            ok_msg = self.font.render("Press ENTER to Start", True, (0, 100, 0))
            self.screen.blit(ok_msg, (self.modal_rect.centerx - ok_msg.get_width() // 2, self.modal_rect.bottom - 50))

        cancel_msg = self.font.render("Press 1 to Cancel and Return", True, (150, 0, 0))
        self.screen.blit(cancel_msg,
                         (self.modal_rect.centerx - cancel_msg.get_width() // 2, self.modal_rect.bottom - 25))

        # ข้อความเตือนถ้าเลือดหมด
        if self.warning_timer and pygame.time.get_ticks() - self.warning_timer < 1500:
            warn = self.font.render("THIS POKEMON HAS NO HP!", True, (255, 0, 0))
            self.screen.blit(warn, warn.get_rect(center=(self.modal_rect.centerx, self.modal_rect.y - 20)))

    def run(self):
        warning_time = 0
        warning_active = False

        big_font = pygame.font.Font("Fonts/Arabica/ttf/Arabica.ttf", 26)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.cursor_index = max(0, self.cursor_index - 1)
                        self.page = self.cursor_index // self.cards_per_page
                    elif event.key == pygame.K_RIGHT:
                        self.cursor_index = min(len(self.pokemon_list) - 1, self.cursor_index + 1)
                        self.page = self.cursor_index // self.cards_per_page
                    elif event.key == pygame.K_SPACE:
                        selected_pokemon = self.pokemon_list[self.cursor_index]
                        if selected_pokemon.hp <= 0:
                            warning_active = True
                            warning_time = pygame.time.get_ticks()
                        elif self.cursor_index in self.selected_indices:
                            self.selected_indices.remove(self.cursor_index)
                        elif len(self.selected_indices) < 3:
                            self.selected_indices.append(self.cursor_index)
                    elif event.key == pygame.K_RETURN and len(self.selected_indices) > 0:
                        return [self.pokemon_list[i] for i in self.selected_indices]
                    elif event.key == pygame.K_1:
                        return None

            # วาดพื้นหลัง
            if self.draw_background_fn:
                self.draw_background_fn(self.screen)
            else:
                self.screen.fill((0, 0, 0))

            self.draw()

            # แสดงกล่องข้อความหากเลือดหมด
            if warning_active and pygame.time.get_ticks() - warning_time < 2500:
                text = big_font.render("THIS POKEMON HAS NO HP!", True, (200, 0, 0))

                box_width = text.get_width() + 40
                box_height = text.get_height() + 20
                box_x = self.modal_rect.centerx - box_width // 2
                box_y = self.modal_rect.bottom + 20

                warning_rect = pygame.Rect(box_x, box_y, box_width, box_height)

                pygame.draw.rect(self.screen, (255, 220, 220), warning_rect, border_radius=8)
                pygame.draw.rect(self.screen, (200, 0, 0), warning_rect, 3, border_radius=8)
                self.screen.blit(text, text.get_rect(center=warning_rect.center))

            else:
                warning_active = False

            pygame.display.update()
            self.clock.tick(60)