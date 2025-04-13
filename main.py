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
                        print(f"Starting game for: {self.player_name}")
                        return self.player_name
                elif event.type == pygame.KEYDOWN and self.active:
                    if event.key == pygame.K_RETURN:
                        print(f"Starting game for: {self.player_name}")
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

        # ลบ pikachu ออกเพื่อเอาไว้สุ่มมอนอื่น
        all_monsters = [m for m in self.pokemon_data.monsters if m.name != "pikachu"]

        print("✅ มอนทั้งหมดที่เอาไปสุ่ม (ไม่รวม pikachu):", all_monsters)

        random.shuffle(all_monsters)
        self.available_wild_monsters = all_monsters[:6]

        # ดึงแค่หญ้า 6 จุดแรก
        grass_areas = self.map.grass_rects[:6]

        print("✅ ตำแหน่งหญ้า:", grass_areas)
        print("✅ มอนที่สุ่มจะวางในหญ้า:", self.available_wild_monsters)

        # map หญ้ากับมอนเข้า dict
        self.grass_monster_lookup = {}
        for rect, monster in zip(grass_areas, self.available_wild_monsters):
            rect_key = (rect.x, rect.y, rect.width, rect.height)  # ✅ tuple
            self.grass_monster_lookup[rect_key] = monster

        print("🧪 ตำแหน่งหญ้าที่มีมอน:", self.grass_monster_lookup)

    def start_battle(self, wild_monster):
        battle = BattleScene(self.screen, self.player_monsters[0], wild_monster)
        result = battle.run()
        if result == "win":
            self.player_monsters.append(wild_monster)

    def run(self):
        running = True
        while running:
            self.screen.fill((0, 0, 0))
            keys = pygame.key.get_pressed()
            self.player.update(keys)
            self.map.draw(self.screen)
            self.player.draw(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            for rect_data, monster in list(self.grass_monster_lookup.items()):
                rect = pygame.Rect(rect_data)  # แปลง tuple กลับเป็น Rect
                if rect.collidepoint(self.player.pos):
                    self.start_battle(monster)
                    del self.grass_monster_lookup[rect_data]
                    break

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