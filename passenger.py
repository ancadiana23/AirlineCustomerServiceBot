class Passenger:
	id = 0

	def __init__(self, name):
		self.id = Passenger.id
		Passenger.id += 1
		self.name = name
		self.loyalty_card = None


	def set_birthdate(self, birthdate):
		self.birthdate = birthdate


	def add_loyalty_card(self,loyalty_card):
		self.loyalty_card = loyalty_card


	def __str__(self):
		return "Passenger ({}, {}, {})".format(self.id, self.name, self.loyalty_card)