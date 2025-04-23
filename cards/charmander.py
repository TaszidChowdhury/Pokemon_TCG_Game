from pokemon_card import PokemonCard

def create_charmander():
    return PokemonCard(
        name="Charmander",
        stage="Basic",
        evolves_from=None,
        hp=60,
        p_type="Fire",
        attacks={
            "Ember": {
                "damage": 30,
                "cost": ["Fire"],
                "effect": "Discard a Fire Energy from this Pokémon."
            }
        },
        retreat_cost=1,
        weakness={"Water": "+20"}
    )
