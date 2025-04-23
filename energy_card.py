from card import Card

class EnergyCard(Card):
    VALID_ENERGY_TYPES = [
        "Grass",    # Healing and Poison effects
        "Fire",     # High damage, Burn effects
        "Water",    # Energy manipulation, Pokémon movement
        "Lightning", # Energy recovery, Paralysis
        "Psychic",  # Special powers, Sleep/Confusion/Poison
        "Fighting", # High risk/reward, coin flips
        "Darkness", # Discard effects, Poison
        "Metal",    # Damage resistance
        "Fairy",    # Attack reduction
        "Dragon",   # Dual-type requirements
        "Colorless" # Versatile, works with any deck
    ]

    def __init__(self, energy_type):
        super().__init__(f"{energy_type} Energy", "Energy")
        if energy_type not in self.VALID_ENERGY_TYPES:
            raise ValueError(f"Invalid energy type. Must be one of: {', '.join(self.VALID_ENERGY_TYPES)}")
        self.energy_type = energy_type
        self.special_effects = self._get_special_effects()

    def _get_special_effects(self):
        """Get the special effects associated with this energy type."""
        effects = {
            "Grass": {
                "description": "Often has healing abilities and can cause Poison",
                "common_effects": ["heal", "poison"]
            },
            "Fire": {
                "description": "High damage attacks with Burn effects, needs recovery time",
                "common_effects": ["burn", "high_damage"]
            },
            "Water": {
                "description": "Can manipulate Energy and move opposing Pokémon",
                "common_effects": ["energy_manipulation", "pokemon_movement"]
            },
            "Lightning": {
                "description": "Can recover Energy and cause Paralysis",
                "common_effects": ["energy_recovery", "paralysis"]
            },
            "Psychic": {
                "description": "Special powers causing Sleep, Confusion, or Poison",
                "common_effects": ["sleep", "confusion", "poison"]
            },
            "Fighting": {
                "description": "High risk/reward attacks with coin flip mechanics",
                "common_effects": ["coin_flip", "high_risk"]
            },
            "Darkness": {
                "description": "Sneaky attacks causing discards and Poison",
                "common_effects": ["discard", "poison"]
            },
            "Metal": {
                "description": "High damage resistance",
                "common_effects": ["damage_resistance"]
            },
            "Fairy": {
                "description": "Reduces effectiveness of opposing attacks",
                "common_effects": ["attack_reduction"]
            },
            "Dragon": {
                "description": "Strong attacks requiring multiple Energy types",
                "common_effects": ["dual_type_requirement"]
            },
            "Colorless": {
                "description": "Versatile, works with any type of deck",
                "common_effects": ["versatile"]
            }
        }
        return effects.get(self.energy_type, {})

    def __str__(self):
        return f"{self.energy_type} Energy"

    def get_description(self):
        """Get a description of this energy type's special characteristics."""
        return self.special_effects.get("description", "No special effects.")
