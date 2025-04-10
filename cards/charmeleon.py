from pokemon_card import PokemonCard

def create_charmeleon():
    return PokemonCard(
        name="Charmeleon",
        stage="Stage 1",
        evolves_from="Charmander",
        hp=80,
        p_type="Fire",
        attacks={
            "Slash": {
                "damage": 50,
                "cost": ["Colorless", "Colorless", "Colorless"],
                "effect": None
            },
            "Flamethrower": {
                "damage": 90,
                "cost": ["Fire", "Fire", "Colorless", "Colorless"],
                "effect": "Discard a Fire Energy attached to this Pokémon."
            }
        },
        retreat_cost=1,
        weakness={"Water": "x2"}
    )
