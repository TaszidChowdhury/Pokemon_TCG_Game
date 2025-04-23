from card import Card

class TrainerCard(Card):
    def __init__(self, name, effect_function, description=""):
        super().__init__(name, "Trainer")
        self.effect_function = effect_function  # function that executes the trainer's effect
        self.description = description

    def use(self, player):
        print(f"{player.name} played Trainer: {self.name}")
        print(f"Effect: {self.description}")
        self.effect_function(player)
