from pokemon_card import PokemonCard

def create_ivysaur():
    return PokemonCard(
        name="Ivysaur",
        stage="Stage 1",
        evolves_from="Bulbasaur",
        hp=80,
        p_type="Grass",
        attacks={
            "Leech Seed": {
                "damage": 20,
                "cost": ["Grass", "Colorless"],
                "effect": "Remove 1 damage counter from Ivysaur."
            },
            "Razor Leaf": {
                "damage": 60,
                "cost": ["Grass", "Grass", "Colorless"],
                "effect": None
            }
        },
        retreat_cost=2,
        weakness={"Fire": "+20"}
    )
