class Flight:
	id = 0

	def __init__(self, company, origin, destination, time, num_seats):
		self.id = Flight.id
		Flight.id += 1
		self.company = company
		self.origin = origin
		self.destination = destination
		self.time = time
		self.num_seats = num_seats

	def __str__(self):
		return "Flight ({}, {}, {}, {}, {})"\
					.format(self.id, \
							self.company, \
							self.origin, \
							self.destination,
							self.time)