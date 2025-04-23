from pokemon_card import PokemonCard

def create_venusaur():
    return PokemonCard(
        name="Venusaur",
        stage="Stage 2",
        evolves_from="Ivysaur",
        hp=160,
        p_type="Grass",
        attacks={
            "Solar Beam": {
                "damage": 90,
                "cost": ["Grass", "Grass", "Grass"],
                "effect": None
            }
        },
        retreat_cost=4,
        weakness={"Fire": "x2"},
        ability="Jungle Totem"
    )
