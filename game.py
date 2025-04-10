import random

class Game:
    def __init__(self, player1, player2):
        self.players = [player1, player2]
        self.current_turn = 0

    def setup(self):
        print("=== Game Setup ===")
        for player in self.players:
            random.shuffle(player.deck)

            # Draw a 5-card hand — if no Basic Pokémon, reshuffle (mulligan)
            while True:
                player.hand = [player.deck.pop(0) for _ in range(5)]
                if any(getattr(card, 'stage', '') == "Basic" for card in player.hand):
                    break
                print(f"{player.name} had no Basic Pokémon — performing a mulligan.")
                player.deck.extend(player.hand)
                player.hand.clear()
                random.shuffle(player.deck)

            player.setup_prizes()

            # Choose Active Pokémon
            print(f"\n{player.name}, choose your Active Pokémon:")
            basics = [card for card in player.hand if getattr(card, 'stage', '') == "Basic"]
            for i, card in enumerate(basics):
                print(f"{i}: {card.name}")
            while True:
                choice = input("Enter the number: ").strip()
                if choice.isdigit():
                    index = int(choice)
                    if 0 <= index < len(basics):
                        selected = basics[index]
                        player.play_basic_pokemon(selected)
                        player.hand.remove(selected)
                        break
                print("Invalid choice. Try again.")

            # Choose up to 3 Bench Pokémon
            print(f"\n{player.name}, choose up to 3 Basic Pokémon for your Bench:")
            basics = [card for card in player.hand if getattr(card, 'stage', '') == "Basic"]
            for i, card in enumerate(basics):
                print(f"{i}: {card.name}")
            while len(player.bench) < 3 and basics:
                choice = input("Enter number of Pokémon to add to Bench (or press Enter to skip): ").strip()
                if choice == "":
                    break
                if choice.isdigit():
                    index = int(choice)
                    if 0 <= index < len(basics):
                        selected = basics.pop(index)
                        player.play_basic_pokemon(selected)
                        player.hand.remove(selected)
                    else:
                        print("Invalid index.")
                else:
                    print("Invalid input.")
            print(f"{player.name} ready!")

    def play_turn(self, player):
        opponent = player.opponent
        print(f"\n== {player.name}'s Turn ==")

        # Show current Active Pokémon for both players
        if player.active:
            print(f"{player.name}'s Active Pokémon: {player.active.name} (HP: {player.active.current_hp}/{player.active.hp})")
        if opponent and opponent.active:
            print(f"{opponent.name}'s Active Pokémon: {opponent.active.name} (HP: {opponent.active.current_hp}/{opponent.active.hp})")

        # Draw a card
        if player.deck:
            drawn = player.deck.pop(0)
            player.hand.append(drawn)
            print(f"{player.name} drew a card: {drawn}")
        else:
            print(f"{player.name} has no cards left to draw!")


        # Show hand
        print("\nYour hand:")
        for i, card in enumerate(player.hand):
            print(f"{i}: {card}")

        # Option to retreat
        if player.bench:
            choice = input("Do you want to retreat your Active Pokémon? (y/n): ").strip().lower()
            if choice == 'y':
                self.retreat_active(player)

        # Evolve Pokémon
        choice = input("Do you want to evolve a Pokémon? (y/n): ").strip().lower()
        if choice == 'y':
            for i, card in enumerate(player.hand):
                if hasattr(card, 'stage') and card.stage in ["Stage 1", "Stage 2"]:
                    print(f"{i}: {card.name} (evolves from {card.evolves_from})")
            evolve_choice = input("Enter the number of the evolution card to play: ").strip()
            if evolve_choice.isdigit():
                index = int(evolve_choice)
                if 0 <= index < len(player.hand):
                    evolved = player.evolve_pokemon(player.hand[index])
                    if evolved:
                        player.hand.pop(index)

        # Attach Energy
        for i, card in enumerate(player.hand):
            if card.card_type == "Energy":
                print(f"{i}: {card}")
        energy_choice = input("Enter the number of an Energy card to attach (or press Enter to skip): ").strip()
        if energy_choice.isdigit():
            index = int(energy_choice)
            if 0 <= index < len(player.hand):
                player.attach_energy(player.active, player.hand[index])
                player.hand.pop(index)

        # Choose Attack
        if player.active and player.active.attacks:
            print("\nAvailable attacks:")
            for i, (name, atk) in enumerate(player.active.attacks.items()):
                print(f"{i}: {name} – {atk['damage']} dmg – Cost: {atk['cost']}")
            attack_choice = input("Choose attack number (or press Enter to skip): ").strip()
            if attack_choice.isdigit():
                index = int(attack_choice)
                attack_names = list(player.active.attacks.keys())
                if 0 <= index < len(attack_names):
                    player.use_attack(player.active, attack_names[index])
                else:
                    print("Invalid attack number.")
            else:
                print("Skipped attacking.")

    def retreat_active(self, player):
        print("\nBench Pokémon:")
        for i, poke in enumerate(player.bench):
            print(f"{i}: {poke.name} ({poke.current_hp}/{poke.hp})")

        choice = input("Choose a Pokémon from the Bench to switch with: ").strip()
        if choice.isdigit():
            index = int(choice)
            if 0 <= index < len(player.bench):
                player.bench.append(player.active)
                player.active = player.bench.pop(index)
                print(f"{player.name} retreated and switched in {player.active.name}.")
            else:
                print("Invalid index.")
        else:
            print("Retreat cancelled.")

    def check_game_over(self):
        for player in self.players:
            if player.has_won():
                print(f"\n🎉 {player.name} has taken all 6 Prize Cards and wins the game!")
                return True
            if not player.active:
                print(f"\n{player.name} has no Active Pokémon left!")
                winner = self.players[1 - self.players.index(player)]
                print(f"🎉 {winner.name} wins the game!")
                return True
        return False

    def run(self):
        self.setup()
        while True:
            self.play_turn(self.players[self.current_turn])
            if self.check_game_over():
                break
            self.current_turn = 1 - self.current_turn
