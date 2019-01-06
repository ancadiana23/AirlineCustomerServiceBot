class Ticket:
	id = 0
	
	def __init__(self, client, flight, booking_class):
		self.id = Ticket.id
		Ticket.id += 1
		self.client = client
		self.flight = flight
		self.seat = ""
		self.booking_class = booking_class

	def set_cabin_luggage(self, cabin_luggage):
		self.cabin_luggage = cabin_luggage

	def set_checkin_luggage(self, checkin_luggage):
		self.checkin_luggage = checkin_luggage

	def set_seat(self, seat):
		self.seat = seat

	def __str__(self):
		return "Ticket ({}, {}, {})".format(self.id, self.client.name, self.flight.id)