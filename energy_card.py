from card import Card

class EnergyCard(Card):
    def __init__(self, energy_type):
        super().__init__(f"{energy_type} Energy", "Energy")
        if energy_type not in ["Fire", "Water", "Grass"]:
            raise ValueError("Invalid energy type. Must be 'Fire', 'Water', or 'Grass'.")
        self.energy_type = energy_type

    def __str__(self):
        return f"{self.energy_type} Energy"
