class BookingStatus:
	def __init__(self, luggage_allowance):
		self.luggage_allowance = luggage_allowance

	def set_minors(self):
		self.minors = True

	def set_paid(self):
		self.paid = True

	def set_flown(self):
		self.flown = True

	def change_luggage_allowance(self, luggage_allowance):
		self.luggage_allowance = luggage_allowance