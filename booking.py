class Booking:
	id = 0
	
	def __init__(self, origin, destination, time):
		self.id = Booking.id
		Booking.id += 1
		self.luggage = ""
		self.origin = origin
		self.destination = destination
		self.time = time
		self.tickets = []

	def add_ticket(self, ticket):
		self.tickets += [ticket]

	def __str__(self):
		tickets_description = "Tickets: " + ", ".join([str(ticket.id) for ticket in self.tickets])
		return "Booking ({}, {}, {}, {}, {})".\
						format(self.id, \
							   self.origin, \
							   self.destination, \
							   self.time, \
							   tickets_description)