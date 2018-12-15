class Passanger:
	id = 0

	def __init__(self, name):
		self.id = Passanger.id
		Passanger.id += 1
		self.name = name
		self.loyalty_card = None

	def add_loyalty_card(loyalty_card):
		self.loyalty_card = loyalty_card

	def __str__(self):
		return "Passanger ({}, {}, {})".format(self.id, self.name, self.loyalty_card)