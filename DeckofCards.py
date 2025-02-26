import random

SUITS = ["Hearts", "Diamonds", "Spades", "Clubs"]
NAMES = [str(x) for x in range(2, 11)] + ["Jack", "Queen", "King", "Ace"]


class Card:
	def __init__(self, index: int):
		self.index = index

	@property
	def rank(self) -> str:
		return NAMES[self.index % len(NAMES)]

	@property
	def suit(self) -> str:
		return SUITS[self.index // len(NAMES)]

	def __str__(self) -> str:
		return f"{self.rank} of {self.suit}"

def main():
	amt = "..."
	deck = [Card(x) for x in range(len(SUITS) * len(NAMES))]
	while not amt.isdigit(): amt = input("How many cards?\t")
	hand = random.sample(deck, int(amt))
	print("You drew the following cards:\n" + "\n".join(str(x) for x in hand) + f"\nThere are {len(deck) - int(amt)} cards left.")


if __name__ == '__main__':
	main()
