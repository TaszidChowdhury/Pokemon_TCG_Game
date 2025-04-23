import random
from game import Game
from player import Player
from energy_card import EnergyCard

# Pokémon imports from cards folder
from cards.charmander import create_charmander
from cards.charmeleon import create_charmeleon
from cards.charizard import create_charizard
from cards.squirtle import create_squirtle
from cards.wartortle import create_wartortle
from cards.blastoise import create_blastoise
from cards.bulbasaur import create_bulbasaur
from cards.ivysaur import create_ivysaur
from cards.venusaur import create_venusaur

def make_random_deck():
    deck = []
    card_counts = {}  # Track counts of each card name

    # Helper function to check if we can add a card
    def can_add_card(card):
        if card.card_type == "Energy" and card.name.endswith(" Energy"):
            return True  # Basic Energy cards have no limit
        if card.name not in card_counts:
            return True
        return card_counts[card.name] < 4

    # Helper function to add a card to deck and update counts
    def add_card(card):
        if can_add_card(card):
            deck.append(card)
            if card.name not in card_counts:
                card_counts[card.name] = 0
            card_counts[card.name] += 1
            return True
        return False

    # Pokémon
    pokemon_creators = [
        create_charmander, create_charmeleon, create_charizard,
        create_squirtle, create_wartortle, create_blastoise,
        create_bulbasaur, create_ivysaur, create_venusaur
    ]

    # First ensure we have at least one Basic Pokémon
    basic_pokemon_creators = [creator for creator in pokemon_creators if creator().stage == "Basic"]
    if not basic_pokemon_creators:
        raise ValueError("No Basic Pokémon available for deck construction!")
    
    # Add at least one Basic Pokémon
    basic_creator = random.choice(basic_pokemon_creators)
    add_card(basic_creator())

    # Add more Pokémon (respecting 4-card limit)
    while len(deck) < 20:  # Target about 20 Pokémon
        creator = random.choice(pokemon_creators)
        card = creator()
        add_card(card)

    # Energy (no limit on Basic Energy)
    energy_types = EnergyCard.VALID_ENERGY_TYPES
    # Distribute energy types based on Pokémon types in deck
    pokemon_types = [card.p_type for card in deck if hasattr(card, 'p_type')]
    type_counts = {}
    for p_type in pokemon_types:
        type_counts[p_type] = type_counts.get(p_type, 0) + 1

    # Add energy cards based on Pokémon types
    for p_type, count in type_counts.items():
        # Add more energy of types that match Pokémon
        energy_count = min(8, count * 2)  # Up to 8 energy per type
        for _ in range(energy_count):
            add_card(EnergyCard(p_type))

    # Add some Colorless energy for versatility
    while len([c for c in deck if c.card_type == "Energy"]) < 20:  # Target about 20 Energy
        # Prefer Colorless if we need more energy
        if random.random() < 0.3:  # 30% chance for Colorless
            add_card(EnergyCard("Colorless"))
        else:
            # Add other energy types that might be needed
            needed_types = [t for t in energy_types if t != "Colorless"]
            add_card(EnergyCard(random.choice(needed_types)))

    # Trainer cards
    trainers = create_trainer_cards()
    while len(deck) < 60:  # Fill remaining slots with Trainers
        trainer = random.choice(trainers)
        add_card(trainer)

    # Verify deck construction rules
    if len(deck) != 60:
        raise ValueError(f"Deck must be exactly 60 cards, but has {len(deck)} cards!")

    # Verify we have at least one Basic Pokémon
    if not any(getattr(card, 'stage', '') == "Basic" for card in deck):
        raise ValueError("Deck must contain at least one Basic Pokémon!")

    # Verify no more than 4 of any non-Basic Energy card
    for card_name, count in card_counts.items():
        if count > 4 and not card_name.endswith(" Energy"):
            raise ValueError(f"Deck contains {count} copies of {card_name}, maximum is 4!")

    random.shuffle(deck)
    return deck

def draw_two_cards(player):
    for _ in range(2):
        if player.deck:
            card = player.deck.pop(0)
            player.hand.append(card)
            print(f"{player.name} drew {card}")
        else:
            print("Deck is empty!")

def heal_active_pokemon(player):
    if player.active:
        player.active.current_hp = min(player.active.hp, player.active.current_hp + 20)
        print(f"{player.active.name} healed 20 HP!")

def draw_new_hand(player):
    player.deck.extend(player.hand)
    random.shuffle(player.deck)
    player.hand.clear()
    for _ in range(5):
        if player.deck:
            card = player.deck.pop(0)
            player.hand.append(card)
    print(f"{player.name} drew a new hand of 5 cards.")

from trainer_card import TrainerCard

def create_trainer_cards():
    return [
        TrainerCard("Potion", heal_active_pokemon, "Heals 20 damage from your Active Pokémon."),
        TrainerCard("Professor's Research", draw_new_hand, "Discard your hand and draw 5 new cards."),
        TrainerCard("Supporter", draw_two_cards, "Draw 2 cards."),
        TrainerCard("Stadium", lambda p: print("Stadium effect activated"), "Special stadium effect."),
        TrainerCard("Energy Switch", lambda p: print("Switched Energy between Pokémon"), "Move an Energy from one Pokémon to another."),
        TrainerCard("Energy Retrieval", lambda p: print("Retrieved Energy from discard"), "Get 2 basic Energy cards from your discard pile."),
        TrainerCard("Energy Search", lambda p: print("Searched for Energy"), "Search your deck for a basic Energy card.")
    ]

def main():
    try:
        # Create players
        ash = Player("Ash")
        misty = Player("Misty")

        # Assign randomized 60-card decks
        print("Building Ash's deck...")
        ash.deck = make_random_deck()
        print("Building Misty's deck...")
        misty.deck = make_random_deck()

        # Set opponents
        ash.opponent = misty
        misty.opponent = ash

        # Start game
        game = Game(ash, misty)
        game.run()
    except ValueError as e:
        print(f"Error creating decks: {e}")
        return

if __name__ == "__main__":
    main()

