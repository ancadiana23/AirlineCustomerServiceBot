class Flight:
	id = 0

	def __init__(self, company, origin, destination, time, max_passangers):
		self.id = Flight.id
		Flight.id += 1
		self.company = company
		self.origin = origin
		self.destination = destination
		self.time = time
		self.max_passangers = max_passangers


	def __str__(self):
		return "Flight ({}, {}, {}, {}, {})"\
					.format(self.id, \
							self.company, \
							self.origin, \
							self.destination,
							self.time)