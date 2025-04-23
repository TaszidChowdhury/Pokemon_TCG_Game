import random
from typing import List, Optional

class Game:
    def __init__(self, player1, player2):
        self.players = [player1, player2]
        self.current_turn = 0
        self.turn_count = 0

    def display_game_state(self):
        """Display the current state of the game for both players."""
        print("\n=== Current Game State ===")
        for player in self.players:
            print(f"\n{player.name}'s Side:")
            print(f"Prize Cards: {len(player.prize_cards)} remaining")
            print(f"Cards in Deck: {len(player.deck)}")
            print(f"Cards in Hand: {len(player.hand)}")
            
            if player.active:
                print(f"\nActive Pokémon: {player.active.name}")
                print(f"HP: {player.active.current_hp}/{player.active.hp}")
                print(f"Energy Attached: {', '.join(player.active.energy_attached) if player.active.energy_attached else 'None'}")
            
            if player.bench:
                print("\nBench Pokémon:")
                for i, pokemon in enumerate(player.bench, 1):
                    print(f"{i}. {pokemon.name} (HP: {pokemon.current_hp}/{pokemon.hp})")
                    print(f"   Energy: {', '.join(pokemon.energy_attached) if pokemon.energy_attached else 'None'}")
            else:
                print("\nNo Pokémon on Bench")
            print("-" * 40)

    def get_valid_input(self, prompt: str, valid_range: Optional[List[int]] = None, allow_empty: bool = False) -> str:
        """Helper method to get valid input from the user."""
        while True:
            choice = input(prompt).strip()
            if allow_empty and not choice:
                return choice
            if choice.isdigit():
                if valid_range is None or int(choice) in valid_range:
                    return choice
            print("Invalid input. Please try again.")

    def flip_coin(self):
        """Flip a coin to determine who goes first."""
        print("\n=== Coin Flip ===")
        result = random.choice(["Heads", "Tails"])
        print(f"The coin flip result is: {result}")
        return result

    def setup(self):
        print("=== Game Setup ===")
        
        # Step 2: Coin flip to determine who goes first
        coin_result = self.flip_coin()
        first_player = self.get_valid_input(
            f"Who called {coin_result}? (1: {self.players[0].name}, 2: {self.players[1].name}): ",
            range(1, 3)
        )
        first_player_index = int(first_player) - 1
        self.current_turn = first_player_index
        print(f"\n{self.players[first_player_index].name} won the coin flip and will go first!")

        # Step 3 & 4: Shuffle and draw initial hands
        for player in self.players:
            print(f"\n{player.name}'s turn to set up:")
            random.shuffle(player.deck)
            
            # Handle mulligans
            mulligan_count = 0
            while True:
                # Draw 7 cards
                player.hand = [player.deck.pop(0) for _ in range(7)]
                print(f"{player.name} drew 7 cards.")
                
                # Check for Basic Pokémon
                basics = [card for card in player.hand if getattr(card, 'stage', '') == "Basic"]
                if basics:
                    break
                
                # No Basic Pokémon - perform mulligan
                mulligan_count += 1
                print(f"\n{player.name} has no Basic Pokémon in hand. Revealing hand:")
                for card in player.hand:
                    print(f"- {card}")
                
                # Return cards to deck and shuffle
                player.deck.extend(player.hand)
                player.hand.clear()
                random.shuffle(player.deck)
                print(f"{player.name} shuffles their hand back into their deck.")
                
                # Opponent draws an extra card for each mulligan
                opponent = self.players[1 - self.players.index(player)]
                if opponent.deck:
                    extra_card = opponent.deck.pop(0)
                    opponent.hand.append(extra_card)
                    print(f"{opponent.name} draws an extra card due to the mulligan: {extra_card}")
            
            if mulligan_count > 0:
                print(f"{player.name} performed {mulligan_count} mulligan(s).")
            
            # Step 5: Choose Active Pokémon
            print(f"\n{player.name}, choose your Active Pokémon:")
            for i, card in enumerate(basics):
                print(f"{i}: {card.name}")
            
            choice = self.get_valid_input("Enter the number: ", range(len(basics)))
            selected = basics[int(choice)]
            player.play_basic_pokemon(selected)
            player.hand.remove(selected)

            # Set up Prize Cards
            player.setup_prizes()
            print(f"{player.name} set aside 6 Prize Cards.")

            # Show remaining hand
            print(f"\n{player.name}'s remaining hand:")
            for i, card in enumerate(player.hand):
                print(f"{i}: {card}")

            # Option to place Pokémon on Bench
            basics = [card for card in player.hand if getattr(card, 'stage', '') == "Basic"]
            if basics:
                print(f"\n{player.name}, you may place Basic Pokémon on your Bench:")
                for i, card in enumerate(basics):
                    print(f"{i}: {card.name}")
                
                while len(player.bench) < 5 and basics:
                    choice = self.get_valid_input(
                        "Enter number of Pokémon to add to Bench (or press Enter to skip): ",
                        range(len(basics)),
                        allow_empty=True
                    )
                    if not choice:
                        break
                    selected = basics.pop(int(choice))
                    player.play_basic_pokemon(selected)
                    player.hand.remove(selected)
            
            print(f"{player.name} is ready!")

    def play_turn(self, player):
        """Play a turn for the given player."""
        print(f"\n=== {player.name}'s Turn ===")
        
        # Draw a card at the start of turn
        if player.deck:
            drawn_card = player.deck.pop(0)
            player.hand.append(drawn_card)
            print(f"{player.name} drew a card: {drawn_card}")
        else:
            print(f"{player.name} has no cards left to draw!")
            return False  # Game over if can't draw

        # Main turn loop - can perform actions in any order
        while True:
            print("\nAvailable Actions:")
            print("1. Put Basic Pokémon on Bench")
            print("2. Evolve Pokémon")
            print("3. Attach Energy")
            print("4. Play Trainer")
            print("5. Retreat Active Pokémon")
            print("6. Use Ability")
            print("7. Attack")
            print("8. End Turn")
            
            choice = input("Choose an action (1-8): ")
            
            if choice == "1":  # Put Basic Pokémon on Bench
                if len(player.bench) >= 5:
                    print("Bench is full!")
                    continue
                
                basic_pokemon = [card for card in player.hand if getattr(card, 'stage', '') == "Basic"]
                if not basic_pokemon:
                    print("No Basic Pokémon in hand!")
                    continue
                
                print("\nBasic Pokémon in hand:")
                for i, pokemon in enumerate(basic_pokemon, 1):
                    print(f"{i}. {pokemon.name} (HP: {pokemon.hp})")
                
                try:
                    choice = int(input("Choose a Pokémon to put on Bench (1-{}): ".format(len(basic_pokemon))))
                    if 1 <= choice <= len(basic_pokemon):
                        pokemon = basic_pokemon[choice-1]
                        player.hand.remove(pokemon)
                        player.bench.append(pokemon)
                        print(f"Put {pokemon.name} on Bench!")
                    else:
                        print("Invalid choice!")
                except ValueError:
                    print("Please enter a number!")
            
            elif choice == "2":  # Evolve Pokémon
                # Check if player has any evolution cards in hand
                evolution_cards = [card for card in player.hand if getattr(card, 'stage', '') in ["Stage 1", "Stage 2"]]
                if not evolution_cards:
                    print("No evolution cards in hand!")
                    continue

                # Show available evolution cards
                print("\nEvolution cards in hand:")
                for i, card in enumerate(evolution_cards, 1):
                    print(f"{i}. {card.name} (Stage: {card.stage})")

                try:
                    evo_choice = int(input("Choose an evolution card to play (1-{}): ".format(len(evolution_cards))))
                    if not 1 <= evo_choice <= len(evolution_cards):
                        print("Invalid choice!")
                        continue

                    evolution_card = evolution_cards[evo_choice-1]
                    
                    # Show available Pokémon to evolve
                    print("\nAvailable Pokémon to evolve:")
                    if player.active and player.active.can_evolve_into(evolution_card):
                        print(f"1. Active: {player.active.name}")
                    for i, pokemon in enumerate(player.bench, 1):
                        if pokemon.can_evolve_into(evolution_card):
                            print(f"{i+1}. Bench: {pokemon.name}")

                    try:
                        poke_choice = int(input("Choose a Pokémon to evolve (1-{}): ".format(
                            len([p for p in [player.active] + player.bench if p and p.can_evolve_into(evolution_card)])
                        )))
                        
                        # Get the target Pokémon
                        if poke_choice == 1 and player.active and player.active.can_evolve_into(evolution_card):
                            target = player.active
                        else:
                            bench_index = poke_choice - (2 if player.active and player.active.can_evolve_into(evolution_card) else 1)
                            if 0 <= bench_index < len(player.bench):
                                target = player.bench[bench_index]
                            else:
                                print("Invalid choice!")
                                continue

                        if target and target.can_evolve_into(evolution_card):
                            player.hand.remove(evolution_card)
                            if target == player.active:
                                player.active = evolution_card
                            else:
                                player.bench[player.bench.index(target)] = evolution_card
                            print(f"Evolved {target.name} into {evolution_card.name}!")
                        else:
                            print("Cannot evolve that Pokémon!")
                    except ValueError:
                        print("Please enter a number!")
                except ValueError:
                    print("Please enter a number!")
            
            elif choice == "3":  # Attach Energy
                if not player.hand:
                    print("No cards in hand!")
                    continue
                
                energy_cards = [card for card in player.hand if card.card_type == "Energy"]
                if not energy_cards:
                    print("No Energy cards in hand!")
                    continue
                
                print("\nEnergy cards in hand:")
                for i, energy in enumerate(energy_cards, 1):
                    print(f"{i}. {energy.name}")
                
                try:
                    choice = int(input("Choose an Energy card (1-{}): ".format(len(energy_cards))))
                    if 1 <= choice <= len(energy_cards):
                        energy = energy_cards[choice-1]
                        
                        print("\nChoose a Pokémon to attach Energy to:")
                        if player.active:
                            print(f"1. Active: {player.active.name}")
                        for i, pokemon in enumerate(player.bench, 1):
                            print(f"{i+1}. Bench: {pokemon.name}")
                        
                        try:
                            poke_choice = int(input("Choose a Pokémon (1-{}): ".format(len(player.bench) + 1)))
                            if poke_choice == 1 and player.active:
                                player.active.attached_energy.append(energy)
                                player.hand.remove(energy)
                                print(f"Attached {energy.name} to {player.active.name}!")
                            elif 1 < poke_choice <= len(player.bench) + 1:
                                pokemon = player.bench[poke_choice-2]
                                pokemon.attached_energy.append(energy)
                                player.hand.remove(energy)
                                print(f"Attached {energy.name} to {pokemon.name}!")
                            else:
                                print("Invalid choice!")
                        except ValueError:
                            print("Please enter a number!")
                    else:
                        print("Invalid choice!")
                except ValueError:
                    print("Please enter a number!")
            
            elif choice == "4":  # Play Trainer
                trainer_cards = [card for card in player.hand if card.card_type == "Trainer"]
                if not trainer_cards:
                    print("No Trainer cards in hand!")
                    continue
                
                print("\nTrainer cards in hand:")
                for i, trainer in enumerate(trainer_cards, 1):
                    print(f"{i}. {trainer.name} - {trainer.description}")
                
                try:
                    choice = int(input("Choose a Trainer card (1-{}): ".format(len(trainer_cards))))
                    if 1 <= choice <= len(trainer_cards):
                        trainer = trainer_cards[choice-1]
                        trainer.effect(player)
                        player.hand.remove(trainer)
                        print(f"Played {trainer.name}!")
                    else:
                        print("Invalid choice!")
                except ValueError:
                    print("Please enter a number!")
            
            elif choice == "5":  # Retreat Active Pokémon
                if not player.active:
                    print("No Active Pokémon!")
                    continue
                
                if not player.bench:
                    print("No Pokémon on Bench to retreat to!")
                    continue
                
                retreat_cost = player.active.retreat_cost
                attached_energy = [e.energy_type for e in player.active.attached_energy]
                
                # Check if retreat cost can be paid
                if len(attached_energy) < retreat_cost:
                    print(f"Not enough Energy attached! Need {retreat_cost} Energy, have {len(attached_energy)}")
                    continue
                
                print("\nChoose a Pokémon to retreat to:")
                for i, pokemon in enumerate(player.bench, 1):
                    print(f"{i}. {pokemon.name}")
                
                try:
                    choice = int(input("Choose a Pokémon (1-{}): ".format(len(player.bench))))
                    if 1 <= choice <= len(player.bench):
                        # Move Active to Bench
                        player.bench.append(player.active)
                        # Set new Active
                        player.active = player.bench.pop(choice-1)
                        # Discard Energy equal to retreat cost
                        for _ in range(retreat_cost):
                            if player.active.attached_energy:
                                player.active.attached_energy.pop(0)
                        print(f"Retreated to {player.active.name}!")
                    else:
                        print("Invalid choice!")
                except ValueError:
                    print("Please enter a number!")
            
            elif choice == "6":  # Use Ability
                if not player.active or not player.active.ability:
                    print("No Ability to use!")
                    continue
                
                print(f"\n{player.active.name}'s Ability: {player.active.ability}")
                if input("Use Ability? (y/n): ").lower() == 'y':
                    player.active.use_ability(player)
            
            elif choice == "7":  # Attack
                if not player.active:
                    print("No Active Pokémon!")
                    continue
                
                if not player.active.attacks:
                    print("No attacks available!")
                    continue
                
                print("\nAvailable attacks:")
                for i, attack in enumerate(player.active.attacks, 1):
                    print(f"{i}. {attack['name']} (Damage: {attack['damage']}, Cost: {attack['cost']})")
                
                try:
                    choice = int(input("Choose an attack (1-{}): ".format(len(player.active.attacks))))
                    if 1 <= choice <= len(player.active.attacks):
                        attack = player.active.attacks[choice-1]
                        
                        # Check if attack cost can be paid
                        attached_energy = [e.energy_type for e in player.active.attached_energy]
                        if not all(cost in attached_energy for cost in attack['cost']):
                            print("Not enough Energy to use this attack!")
                            continue
                        
                        # Apply attack
                        player.opponent.active.current_hp -= attack['damage']
                        print(f"{player.active.name} used {attack['name']} for {attack['damage']} damage!")
                        
                        # Check for knockout
                        if player.opponent.active.current_hp <= 0:
                            print(f"{player.opponent.active.name} was knocked out!")
                            player.opponent.active = None
                            if not player.opponent.bench:
                                return True  # Game over
                    else:
                        print("Invalid choice!")
                except ValueError:
                    print("Please enter a number!")
            
            elif choice == "8":  # End Turn
                break
            
            else:
                print("Invalid choice!")
        
        return False  # Game continues

    def retreat_active(self, player):
        print("\nBench Pokémon:")
        for i, poke in enumerate(player.bench):
            print(f"{i}: {poke.name} ({poke.current_hp}/{poke.hp})")

        choice = self.get_valid_input("Choose a Pokémon from the Bench to switch with: ", range(len(player.bench)))
        if choice:
            index = int(choice)
            player.bench.append(player.active)
            player.active = player.bench.pop(index)
            print(f"{player.name} retreated and switched in {player.active.name}.")

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
