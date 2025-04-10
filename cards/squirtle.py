from pokemon_card import PokemonCard

def create_squirtle():
    return PokemonCard(
        name="Squirtle",
        stage="Basic",
        evolves_from=None,
        hp=60,
        p_type="Water",
        attacks={
            "Bubble": {
                "damage": 10,
                "cost": ["Water"],
                "effect": "Flip a coin. If heads, your opponent’s Active Pokémon is now Paralyzed."
            }
        },
        retreat_cost=1,
        weakness={"Grass": "x2"}
    )
