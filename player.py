class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.bench = []
        self.active = None
        self.discard_pile = []
        self.deck = []
        self.prize_cards = []
        self.prizes_taken = 0
        self.opponent = None  # Will be set externally (used for KO handling)

    def setup_prizes(self):
        self.prize_cards = self.deck[:6]
        self.deck = self.deck[6:]
        print(f"{self.name} set aside 6 Prize Cards.")

    def take_prize_card(self):
        if self.prize_cards:
            card = self.prize_cards.pop(0)
            self.hand.append(card)
            self.prizes_taken += 1
            print(f"{self.name} took a Prize Card: {card}")
        else:
            print(f"{self.name} has no Prize Cards left!")

    def has_won(self):
        return self.prizes_taken >= 6

    def play_basic_pokemon(self, pokemon):
        if pokemon.stage != "Basic":
            print(f"{pokemon.name} is not a Basic Pokémon!")
            return False
        if not self.active:
            self.active = pokemon
            print(f"{self.name} played {pokemon.name} as Active Pokémon.")
        elif len(self.bench) < 5:
            self.bench.append(pokemon)
            print(f"{self.name} placed {pokemon.name} on the Bench.")
        else:
            print("Bench is full.")
            return False
        return True

    def evolve_pokemon(self, new_card):
        if new_card.stage == "Stage 1" or new_card.stage == "Stage 2":
            targets = [self.active] + self.bench
            for i, poke in enumerate(targets):
                if poke and poke.name == new_card.evolves_from:
                    new_card.energy_attached = poke.energy_attached
                    new_card.current_hp = poke.current_hp
                    if i == 0:
                        self.active = new_card
                        print(f"{poke.name} evolved into {new_card.name} (Active).")
                    else:
                        self.bench[i - 1] = new_card
                        print(f"{poke.name} evolved into {new_card.name} (Bench).")
                    return True
            print(f"Cannot evolve {new_card.name}: {new_card.evolves_from} not found.")
        else:
            print(f"{new_card.name} is not an evolution card.")
        return False

    def attach_energy(self, pokemon, energy):
        pokemon.energy_attached.append(energy.energy_type)
        print(f"Attached {energy.energy_type} Energy to {pokemon.name}.")

    def can_use_attack(self, pokemon, attack_name):
        attack = pokemon.attacks.get(attack_name)
        if not attack:
            print(f"{pokemon.name} doesn't have the attack '{attack_name}'.")
            return False

        cost = attack["cost"]
        attached = pokemon.energy_attached[:]
        for required in cost:
            if required == "Colorless":
                if attached:
                    attached.pop(0)
                else:
                    return False
            elif required in attached:
                attached.remove(required)
            else:
                return False
        return True

    def use_attack(self, pokemon, attack_name):
        if not self.can_use_attack(pokemon, attack_name):
            print(f"{pokemon.name} cannot use '{attack_name}': not enough energy.")
            return False

        attack = pokemon.attacks[attack_name]
        print(f"{pokemon.name} used {attack_name}! Deals {attack['damage']} damage.")
        if attack.get("effect"):
            print(f"Effect: {attack['effect']}")

        opponent = self.opponent
        if opponent.active:
            if self.deal_damage(opponent.active, attack['damage']):
                self.handle_knock_out(opponent)
        return True

    def deal_damage(self, pokemon, amount):
        pokemon.current_hp -= amount
        print(f"{pokemon.name} took {amount} damage! HP left: {pokemon.current_hp}")
        if pokemon.current_hp <= 0:
            print(f"{pokemon.name} has been Knocked Out!")
            return True
        return False

    def handle_knock_out(self, opponent):
        knocked_out = opponent.active
        opponent.discard_pile.append(knocked_out)
        opponent.active = None

        if opponent.bench:
            opponent.active = opponent.bench.pop(0)
            print(f"{opponent.name} promotes {opponent.active.name} to Active Spot.")
        else:
            print(f"{opponent.name} has no more Pokémon in play!")

        self.take_prize_card()
        
def retreat_active(self):
    if not self.bench:
        print("No Pokémon on the Bench to switch with.")
        return False

    print("\nBench Pokémon:")
    for i, poke in enumerate(self.bench):
        print(f"{i}: {poke.name} ({poke.current_hp}/{poke.hp})")

    choice = input("Choose a Pokémon from the Bench to switch with: ").strip()
    if choice.isdigit():
        index = int(choice)
        if 0 <= index < len(self.bench):
            self.bench.append(self.active)
            self.active = self.bench.pop(index)
            print(f"{self.name} retreated and switched in {self.active.name}.")
            return True
    print("Invalid choice.")
    return False
