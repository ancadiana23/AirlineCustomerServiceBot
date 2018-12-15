class Ticket:
	id = 0
	
	def __init__(self, client, flight, booking_class):
		self.id = Ticket.id
		Ticket.id += 1
		self.client = client
		self.flight = flight
		self.seat = ""
		self.booking_class = booking_class

	def __str__(self):
		return "Ticket ({}, {}, {})".format(self.id, self.client.name, self.flight.id)