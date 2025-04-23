from card import Card

class PokemonCard(Card):
    def __init__(
        self,
        name,
        stage,
        evolves_from,
        hp,
        p_type,
        attacks,
        retreat_cost,
        weakness=None,
        resistance=None,
        ability=None
    ):
        super().__init__(name, "Pokemon")
        self.stage = stage                  # 'Basic', 'Stage 1', or 'Stage 2'
        self.evolves_from = evolves_from    # Name of Pokémon it evolves from (if any)
        self.hp = hp                        # Hit points
        self.current_hp = hp               # Tracks current health for damage
        self.p_type = p_type                # 'Fire', 'Water', 'Grass', etc.
        self.attacks = attacks              # Dictionary of attacks
        self.retreat_cost = retreat_cost    # Number of energy needed to retreat
        self.weakness = weakness or {}      # e.g. {'Water': 'x2'}
        self.resistance = resistance or {}  # e.g. {'Electric': '-20'}
        self.ability = ability              # Optional ability name or description
        self.energy_attached = []           # List of energy types attached

    def __str__(self):
        return f"{self.name} ({self.stage}) - {self.hp} HP"
