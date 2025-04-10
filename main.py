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

    # Pokémon
    pokemon_creators = [
        create_charmander, create_charmeleon, create_charizard,
        create_squirtle, create_wartortle, create_blastoise,
        create_bulbasaur, create_ivysaur, create_venusaur
    ]
    for creator in pokemon_creators:
        deck.extend([creator() for _ in range(3)])

    # Energy
    for _ in range(10):
        deck.append(EnergyCard("Fire"))
        deck.append(EnergyCard("Water"))
        deck.append(EnergyCard("Grass"))

    # Trainer cards
    trainers = create_trainer_cards()
    for _ in range(3):
        deck.append(random.choice(trainers))

    # Pad to 60
    while len(deck) < 60:
        deck.append(random.choice(trainers + [creator() for creator in pokemon_creators]))

    random.shuffle(deck)
    return deck

    # Total: 27 Pokémon + 30 Energy = 57 cards
    # Add 3 random Pokémon to make 60
    extra_pokemon = random.choices(pokemon_creators, k=3)
    deck.extend([creator() for creator in extra_pokemon])

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
        TrainerCard("Supporter", draw_two_cards, "Draw 2 cards.")
    ]


def main():
    # Create players
    ash = Player("Ash")
    misty = Player("Misty")

    # Assign randomized 60-card decks
    ash.deck = make_random_deck()
    misty.deck = make_random_deck()

    # Set opponents
    ash.opponent = misty
    misty.opponent = ash

    # Start game
    game = Game(ash, misty)
    game.run()

if __name__ == "__main__":
    main()

