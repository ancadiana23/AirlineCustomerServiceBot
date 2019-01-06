from booking_status import BookingStatus

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
		self.booking_status = BookingStatus

	def add_ticket(self, ticket):
		self.tickets += [ticket]

	def set_payment_method(self, payment_method):
		self.payment_method = payment_method

	def set_price(self, price):
		self.price = price

	def set_currency(self, currency):
		self.currency = currency

	def set_point_of_sale(self, point_of_sale):
		self.point_of_sale = point_of_sale

	def set_marketing_carrier(self, marketing_carrier):
		self.marketing_carrier = marketing_carrier

	def __str__(self):
		tickets_description = "Tickets: " + ", ".join([str(ticket.id) for ticket in self.tickets])
		return "Booking ({}, {}, {}, {}, {})".\
						format(self.id, \
							   self.origin, \
							   self.destination, \
							   self.time, \
							   tickets_description)