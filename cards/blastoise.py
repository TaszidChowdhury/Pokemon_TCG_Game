from pokemon_card import PokemonCard

def create_blastoise():
    return PokemonCard(
        name="Blastoise",
        stage="Stage 2",
        evolves_from="Wartortle",
        hp=160,
        p_type="Water",
        attacks={
            "Hydro Tackle": {
                "damage": 150,
                "cost": ["Water", "Water", "Water"],
                "effect": "This Pokémon does 30 damage to itself."
            }
        },
        retreat_cost=3,
        weakness={"Grass": "x2"},
        ability="Powerful Squall"
    )
