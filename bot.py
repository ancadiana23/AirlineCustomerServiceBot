import os 
import re

import speech_recognition as sr
from google.cloud import texttospeech

from booking import Booking
from passenger import Passenger
from flight import Flight
from problem import Problem
from ticket import Ticket

class Bot:

	def __init__(self):
		# create recognizer and mic instances
		self.recognizer = sr.Recognizer()
		self.microphone = sr.Microphone()
		self.tts_client = texttospeech.TextToSpeechClient()

		# check that recognizer and microphone arguments are appropriate type
		if not isinstance(self.recognizer, sr.Recognizer):
			raise TypeError("`recognizer` must be `Recognizer` instance")

		if not isinstance(self.microphone, sr.Microphone):
			raise TypeError("`microphone` must be `Microphone` instance")

		self.init_synthethic_dataset()
		self.print_database()
		self.init_question_asnwers_map()
		self.init_airport_to_city_map()


	def init_synthethic_dataset(self):
		self.database = {}
		passengers  = [Passenger(name) for name in ["john green", \
											  "louie anderson", \
											  "liza koshy"]]
		bookings = [Booking(*booking) for booking in 
						[("AMS", "ZRH", "10-Dec-2018"), \
		 				 ("LHR", "AMS", "01-Jan-2019"), \
		 				 ("BER", "ARN", "02-Mar-2019")]]
		flights = [Flight(*flight) for flight in \
						[("KLM", "AMS", "BSL", "10-Dec-2018", 200), \
						 ("SWISS", "BSL", "ZRH", "10-Dec-2018", 100), \
						 ("KLM", "LHR", "AMS", "01-Jan-2019", 300), \
						 ("Eurowings", "BER", "ARN", "02-Mar-2019", 300)]]
		tickets = [Ticket(*ticket) for ticket in \
						[(passengers[0], flights[0], "economy"),
						 (passengers[0], flights[1], "economy"),
						 (passengers[1], flights[2], "business"), \
						 (passengers[2], flights[3], "economy")]]
		bookings[0].add_ticket(tickets[0])
		bookings[0].add_ticket(tickets[1])
		bookings[1].add_ticket(tickets[2])
		bookings[2].add_ticket(tickets[3])

		self.database["passengers"] = passengers
		self.database["bookings"] = bookings
		self.database["flights"] = flights
		self.database["tickets"] = tickets
		self.database["name_to_tickets"] = {passenger.name: [] for passenger in passengers}
		for ticket in tickets:
			self.database["name_to_tickets"][ticket.client.name] += [ticket]


	def print_database(self):
		for key in self.database:
			for x in self.database[key]:
				print(x)
		print(self.database["name_to_tickets"])


	def init_question_asnwers_map(self):
		self.questions_to_answers = { \
			".*security waiting time .* Heathrow Airport.*" : 
				("The security waiting time at the Heathrow Airport is \
					aproximately 10 minutes.", Bot.no_action, "information"),
			".*know the time .* flight.*":
				("", self.flight_information, "information"),
			"goodbye": ("Goodbye, have a pleasant day.", self.stop, "information"),
			".*book .* flight.*": 
				("Let me connect you to our customer service department.", self.stop, "booking"),
			".*cancel .* flight.*": 
				("", self.cancel_flight, "booking")}

	def init_airport_to_city_map(self):
		self.airport_to_city = {
			"AMS": "Amsterdam",
			"ARN": "Stockholm",
			"BER": "Berlin",
			"BSL": "Basel",
			"LHR": "Heathrow",
			"ZRH": "Zurich"
		}


	def speak(self, text):
		# Set the text input to be synthesized
		synthesis_input = texttospeech.types.SynthesisInput(text=text)

		# Build the voice request, select the language code ("en-US") and the ssml
		# voice gender ("neutral")
		voice = texttospeech.types.VoiceSelectionParams(
			language_code='en-US',
			ssml_gender=texttospeech.enums.SsmlVoiceGender.NEUTRAL)

		# Select the type of audio file you want returned
		audio_config = texttospeech.types.AudioConfig(
			audio_encoding=texttospeech.enums.AudioEncoding.MP3)

		# Perform the text-to-speech request on the text input with the selected
		# voice parameters and audio file type
		response = self.tts_client.synthesize_speech(synthesis_input, voice, audio_config)

		# The response's audio_content is binary.
		with open('output.mp3', 'wb') as out:
			# Write the response to the output file.
			out.write(response.audio_content)
			print('Audio content written to file "output.mp3"')
			os.system('mpg321 output.mp3')


	def recognize_speech_from_mic(self):
		"""Transcribe speech from recorded from `microphone`."""

		# adjust the recognizer sensitivity to ambient noise and record audio
		# from the microphone
		with self.microphone as source:
			self.recognizer.adjust_for_ambient_noise(source)
			audio = self.recognizer.listen(source)

		response = ""
		try:
			response = self.recognizer.recognize_google(audio)
			# show the user the transcription
			print("You said: {}".format(response))

		except sr.RequestError:
			# API was unreachable or unresponsive
			self.speak("I didn't catch that. Could you repeat please?\n")

		except sr.UnknownValueError:
			# speech was unintelligible
			self.speak("I didn't catch that. Could you repeat please?\n")
			#self.speak("ERROR, Unable to recognize speech")

		return response


	def no_action():
		pass


	def stop(self):
		self.run = False


	def get_client_name(self):
		name = ""
		if "name" in self.problem.information:
			return True
		else:
			self.speak("Could you tell me your name please.")
			name = self.recognize_speech_from_mic().lower()
		
		if name not in self.database["name_to_tickets"]:
			self.speak("Could not find the name " + name + "in our database.")
			return False

		self.problem.information["name"] = name
		return True


	def flight_information(self):
		got_client_name = self.get_client_name()
		if not got_client_name:
			return

		tickets = self.database["name_to_tickets"]\
							   [self.problem.information["name"]]
		if not tickets:
			self.speak("You have no flights coming up.")
			return
		self.speak("You have a flight coming up on " + \
				   tickets[0].flight.time)


	def cancel_flight(self):
		got_client_name = self.get_client_name()
		if not got_client_name:
			return

		tickets = self.database["name_to_tickets"]\
							   [self.problem.information["name"]]
		if not tickets:
			self.speak("You have no flights coming up.")
			return

		self.speak("You have a flight coming up on " + 
				   tickets[0].flight.time+ \
				   ". Is this the one you want to cancel?")
		answer = self.recognize_speech_from_mic()
		if answer == "yes":
			self.speak("Are you sure you want to cancel your flight to " + 
				self.airport_to_city[tickets[0].flight.destination] + " on " +
				tickets[0].flight.time + "?")
		else:
			return
		answer = self.recognize_speech_from_mic()
		if answer == "yes":
			self.database["name_to_tickets"][self.problem.information["name"]].remove(tickets[0])
			#self.database["tickets"].remove(tickets[0])
			self.speak("Done")
	

	"""
	Using the recognized problem, it will classify it.
	Return a classified problem.
	"""
	def classify(self):
		information_re = ".*(?:know|time|goodbye).*"
		booking_re = ".*(?:book|cancel).*"
		if re.match(information_re, self.problem.content):
			self.problem.type = "information"
		elif re.match(booking_re, self.problem.content):
			self.problem.type = "booking"
		else:
			self.problem.type = "other"

	"""
	Receive a classified abstracted problem and decide weather it can solve it or not.
	For doing so it uses a series of rules that the airline API would provide.
	Return a solution to the problem. if positive with information about the solution.
	"""
	def assess(self):
		for re_exp in self.questions_to_answers.keys():
			if not re.match(re_exp, self.problem.content):
				continue

			# Speak the message
			self.speak(self.questions_to_answers[re_exp][0])
			# Perform the action
			self.questions_to_answers[re_exp][1]()
			self.done = True

			if self.run:
				self.speak("Can I help you with anything else?")
			return True
		return False

	
	def run(self):
		self.run = True
		self.done = False
		self.problem = Problem("")

		self.speak("Hello, how may I help you today?")

		while self.run:
			print("How may I help you?")
			question = self.recognize_speech_from_mic()
			
			# If we asked "Can I help you with anything else?" and the
			# answer is "no" then exit.
			if self.done and re.match(".*no.*", question):
				self.speak("Goodbye, have a pleasant day.")
				break
			else:
				self.done = False

			self.problem.content = question
			self.classify()
			success = self.assess()
				
			if not success:
				self.speak("I'm sorry, I don't know how to help with that.")

if __name__ == "__main__":
	bot = Bot()
	bot.run()

   
