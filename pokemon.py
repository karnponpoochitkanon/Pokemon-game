class Pokemon:
    def __init__(self, name, element_type="Normal"):
        self.name = name
        self.element_type = element_type

    def __repr__(self):
        return f"{self.name} ({self.element_type})"


class PlayerMonsters:
    def __init__(self):
        self.monsters = [Pokemon("pikachu", "Normal")]

    def get_available_monsters(self):
        return [
            Pokemon("hitokage", "Fire"),
            Pokemon("zenigame", "Water"),
            Pokemon("fushigidane", "Grass"),
            Pokemon("eevee", "Normal"),
            Pokemon("furin", "Normal"),
            Pokemon("gus", "Normal")
        ]