class Card:
    def __init__(self, name, card_type):
        self.name = name                # Name of the card
        self.card_type = card_type      # Type: 'Pokemon', 'Trainer', or 'Energy'

    def __str__(self):
        return f"{self.name} [{self.card_type}]"
