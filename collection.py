import os
import csv
from datetime import datetime

def save_game_data_to_csv(self):
    file_empty = not os.path.exists("game_stats.csv") or os.stat("game_stats.csv").st_size == 0

    with open("game_stats.csv", mode="a", newline="") as file:
        writer = csv.writer(file)

        if file_empty:
            writer.writerow([
                "Player", "Time(s)", "YIM Battles", "Distance",
                "Total Pokemon", "Heal Tree Uses", "Character"
            ])

        elapsed = datetime.now() - self.start_time

        writer.writerow([
            self.player_name,
            int(elapsed.total_seconds()),
            self.yim_battle_count,
            self.total_distance_walked,
            len(self.player_monsters),
            self.heal_count,
            self.character_name
        ])