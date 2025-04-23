from pokemon_card import PokemonCard

def create_wartortle():
    return PokemonCard(
        name="Wartortle",
        stage="Stage 1",
        evolves_from="Squirtle",
        hp=80,
        p_type="Water",
        attacks={
            "Bubble": {
                "damage": 10,
                "cost": ["Water"],
                "effect": "Flip a coin. Paralyze if heads."
            },
            "Double Spin": {
                "damage": 30,
                "cost": ["Water", "Colorless", "Colorless"],
                "effect": "Flip 2 coins. This attack does 30 damage times the number of heads."
            }
        },
        retreat_cost=2,
        weakness={"Grass": "x2"}
    )
