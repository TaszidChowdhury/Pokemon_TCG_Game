from pokemon_card import PokemonCard

def create_bulbasaur():
    return PokemonCard(
        name="Bulbasaur",
        stage="Basic",
        evolves_from=None,
        hp=70,
        p_type="Grass",
        attacks={
            "Vine Whip": {
                "damage": 10,
                "cost": ["Grass"],
                "effect": None
            },
            "Razor Leaf": {
                "damage": 20,
                "cost": ["Grass", "Colorless"],
                "effect": None
            }
        },
        retreat_cost=1,
        weakness={"Fire": "x2"}
    )
