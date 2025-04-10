from pokemon_card import PokemonCard

def create_charizard():
    return PokemonCard(
        name="Charizard",
        stage="Stage 2",
        evolves_from="Charmeleon",
        hp=150,
        p_type="Fire",
        attacks={
            "Continuous Blaze Ball": {
                "damage": 30,
                "cost": ["Fire", "Fire", "Colorless"],
                "effect": "Discard all Fire Energy. This attack does 50 more damage for each card discarded."
            }
        },
        retreat_cost=3,
        weakness={"Water": "x2"},
        ability="Roaring Resolve"
    )
