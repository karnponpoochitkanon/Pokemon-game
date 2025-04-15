import pygame
import sys
import random
from setting import *
from map import *
from Player import *
from pokemon import *
from battle import BattleScene

class StartMenu:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.input_font = pygame.font.Font("Fonts/Arabica/ttf/Arabica.ttf", 34)
        self.font = pygame.font.Font("Fonts/Arabica/ttf/Arabica.ttf", 36)
        self.title_font = pygame.font.Font("Fonts/Arabica/ttf/Arabica.ttf", 100)
        self.map = Map("map/map.tmx")
        self.background = pygame.image.load("image/Wallpaper.jpg")
        self.background = pygame.transform.scale(self.background, (WINDOW_WIDTH, WINDOW_HEIGHT))

        self.input_box = pygame.Rect(0, 0, 380, 50)
        self.input_box.center = (WINDOW_WIDTH // 2, 520)
        self.color_inactive = pygame.Color('lightskyblue3')
        self.color_active = pygame.Color('dodgerblue2')
        self.color = self.color_inactive
        self.active = False
        self.player_name = ""
        self.button_rect = pygame.Rect(540, 580, 200, 50)
        self.button_color = pygame.Color((244, 143, 177))

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        main_title_surface = self.title_font.render("POKEMON GAME", True, (220, 20, 60))
        box_width = main_title_surface.get_width() + 60
        box_height = main_title_surface.get_height() + 30
        title_bg = pygame.Surface((box_width, box_height), pygame.SRCALPHA)
        pygame.draw.rect(title_bg, (255, 255, 255, 180), title_bg.get_rect(), border_radius=20)
        bg_rect = title_bg.get_rect(center=(WINDOW_WIDTH // 2, 300))
        self.screen.blit(title_bg, bg_rect)
        main_title_rect = main_title_surface.get_rect(center=(WINDOW_WIDTH // 2, 300))
        self.screen.blit(main_title_surface, main_title_rect)

        title_rect = pygame.Rect(0, 0, 300, 50)
        title_rect.midbottom = (self.input_box.centerx, self.input_box.top - 10)
        pygame.draw.rect(self.screen, (178, 223, 219), title_rect, border_radius=12)
        title_surface = self.font.render("ENTER YOUR NAME", True, (33, 33, 33))
        text_rect = title_surface.get_rect(center=title_rect.center)
        self.screen.blit(title_surface, text_rect)

        pygame.draw.rect(self.screen, (255, 255, 255), self.input_box)
        pygame.draw.rect(self.screen, self.color, self.input_box, 2)
        txt_surface = self.input_font.render(self.player_name, True, (0, 0, 0))
        self.input_box.w = max(380, txt_surface.get_width() + 20)
        text_rect = txt_surface.get_rect(center=self.input_box.center)
        self.screen.blit(txt_surface, text_rect)

        self.button_rect.centerx = self.input_box.centerx
        self.button_rect.y = self.input_box.y + 80
        pygame.draw.rect(self.screen, self.button_color, self.button_rect, border_radius=12)
        start_text = self.input_font.render("Start Game", True, (255, 255, 255))
        self.screen.blit(
            start_text,
            (self.button_rect.centerx - start_text.get_width() // 2,
             self.button_rect.centery - start_text.get_height() // 2)
        )

    def run(self):
        while True:
            self.draw()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.input_box.collidepoint(event.pos):
                        self.active = True
                        self.color = self.color_active
                    else:
                        self.active = False
                        self.color = self.color_inactive
                    if self.button_rect.collidepoint(event.pos) and self.player_name.strip():
                        return self.player_name
                elif event.type == pygame.KEYDOWN and self.active:
                    if event.key == pygame.K_RETURN:
                        return self.player_name
                    elif event.key == pygame.K_BACKSPACE:
                        self.player_name = self.player_name[:-1]
                    else:
                        if len(self.player_name) < 10 and event.unicode.isalpha() and event.unicode.isascii():
                            self.player_name += event.unicode
            pygame.display.flip()
            self.clock.tick(30)


class MainGame:
    def __init__(self, screen, player_name, player):
        self.screen = screen
        self.player_name = player_name
        self.player = player
        self.clock = pygame.time.Clock()
        self.map = Map("map/map.tmx")
        self.pokemon_data = PlayerMonsters()
        self.player_monsters = [Pokemon("pikachu", "Normal")]
        self.debug_show_grass = False
        self.show_heal_popup = False
        self.heal_popup_timer = 0

        all_monsters = [m for m in self.pokemon_data.monsters if m.name != "pikachu"]
        random.shuffle(all_monsters)
        grass_areas = self.map.grass_rects[:10]
        self.available_wild_monsters = all_monsters[:10]

        self.grass_monster_lookup = {}
        for rect, monster in zip(grass_areas, self.available_wild_monsters):
            rect_key = (rect.x, rect.y, rect.width, rect.height)
            self.grass_monster_lookup[rect_key] = monster

    def start_battle(self, wild_monster):
        if len(self.player_monsters) > 1:
            popup = PokemonSelectionPopup(self.screen, self.player_monsters)
            chosen = popup.run()
            self.player_monsters.insert(0, self.player_monsters.pop(self.player_monsters.index(chosen)))

        battle = BattleScene(self.screen, self.player_monsters[0], wild_monster, self.player_monsters)
        result = battle.run()

        if result == "win":
            wild_monster.hp = wild_monster.max_hp
            self.player_monsters.append(wild_monster)

            # ลบจาก grass_lookup
            for rect_data, mon in list(self.grass_monster_lookup.items()):
                if mon == wild_monster:
                    del self.grass_monster_lookup[rect_data]
                    break

            # ✅ แสดง popup หลังจากกลับมาหน้า map
            self.map.draw(self.screen)
            self.player.draw(self.screen)
            pygame.display.flip()
            pygame.time.delay(300)  # นิดหน่อยให้หน้าจอรีเฟรชก่อน
            popup = CatchPopup(self.screen, wild_monster.name)
            popup.show()

        elif result == "lose":
            pass  # ไม่ลบมอนถ้าแพ้

    def draw_heal_popup(self):
        font = pygame.font.Font("Fonts/Arabica/ttf/Arabica.ttf", 36)
        message_text = "All Pokemon have been healed!"
        message = font.render(message_text, True, (0, 60, 0))  # Green text

        padding_x, padding_y = 40, 30
        bg_width = message.get_width() + padding_x
        bg_height = message.get_height() + padding_y
        bg = pygame.Surface((bg_width, bg_height))

        bg.fill((204, 255, 204))  # Light green background
        pygame.draw.rect(bg, (0, 100, 0), bg.get_rect(), 4)  # Dark green border

        bg_rect = bg.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        self.screen.blit(bg, bg_rect)
        self.screen.blit(message, message.get_rect(center=bg_rect.center))

    def run(self):
        running = True
        while running:
            self.screen.fill((0, 0, 0))
            keys = pygame.key.get_pressed()
            block_rects = self.map.get_blocking_rects()
            self.player.update(keys, block_rects)
            self.map.draw(self.screen)

            # ✅ ใส่ตรงนี้เลย
            font = pygame.font.Font("Fonts/Arabica/ttf/Arabica.ttf", 24)
            # ✅ ค้นหา healtree object ที่อยู่สูงที่สุด (y น้อยสุด)
            healtree_objects = [obj for obj in self.map.tmx_data.objects if obj.name == "healtree"]
            if healtree_objects:
                topmost_tree = min(healtree_objects, key=lambda o: o.y)
                heal_rect = pygame.Rect(topmost_tree.x, topmost_tree.y, topmost_tree.width, topmost_tree.height)

                font = pygame.font.Font("Fonts/Arabica/ttf/Arabica.ttf", 24)
                label = font.render("HEAL TREE", True, (0, 100, 0))  # เขียวเข้ม
                label_shadow = font.render("HEAL TREE", True, (255, 255, 255))  # เงา

                label_pos = (heal_rect.centerx - label.get_width() // 2, heal_rect.top - 12)
                self.screen.blit(label_shadow, (label_pos[0] + 2, label_pos[1] + 2))  # เงา
                self.screen.blit(label, label_pos)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        self.debug_show_grass = not self.debug_show_grass
                    elif event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                        popup = PokemonTeamPopup(self.screen, self.player_monsters)
                        popup.run()

            if self.debug_show_grass:
                font = pygame.font.Font(None, 40)
                for rect_data in self.grass_monster_lookup:
                    x, y, w, h = rect_data
                    center = (x + w // 2, y + h // 2)
                    shadow = font.render("?", True, (0, 0, 0))
                    text = font.render("?", True, (255, 50, 50))
                    self.screen.blit(shadow, shadow.get_rect(center=(center[0] + 2, center[1] + 2)))
                    self.screen.blit(text, text.get_rect(center=center))

            self.player.draw(self.screen)

            for rect_data, monster in list(self.grass_monster_lookup.items()):
                rect = pygame.Rect(rect_data)
                if rect.colliderect(self.player.rect):
                    self.start_battle(monster)
                    break

            heal_triggered = False
            for obj in self.map.tmx_data.objects:
                if obj.name == "healtree":
                    heal_rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
                    if heal_rect.colliderect(self.player.rect):
                        heal_triggered = True
                        break

            if heal_triggered:
                for p in self.player_monsters:
                    p.hp = p.max_hp
                self.show_heal_popup = True
                self.heal_popup_timer = pygame.time.get_ticks()

            if self.show_heal_popup and pygame.time.get_ticks() - self.heal_popup_timer < 1500:
                self.draw_heal_popup()
            else:
                self.show_heal_popup = False

            pygame.display.flip()
            self.clock.tick(60)


def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Pokemon Game")

    start_menu = StartMenu(screen)
    player_name = start_menu.run()

    character_menu = CharacterSelectMenu(screen, player_name)
    player_image_path = character_menu.run()

    player = Player(player_image_path)
    game = MainGame(screen, player_name, player)
    game.run()


if __name__ == "__main__":
    main()