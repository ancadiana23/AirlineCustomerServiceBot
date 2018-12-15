import os 
import re

import speech_recognition as sr
from google.cloud import texttospeech

from booking import Booking
from passanger import Passanger
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
		#self.print_database()
		self.init_question_asnwers_map()


	def init_synthethic_dataset(self):
		self.database = {}
		Passangers  = [Passanger(name) for name in ["John Green", \
											  "Louie Anderson", \
											  "Liza Koshy"]]
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
						[(Passangers[0], flights[0], "economy"),
						 (Passangers[0], flights[1], "economy"),
						 (Passangers[1], flights[2], "business"), \
						 (Passangers[2], flights[3], "economy")]]
		bookings[0].add_ticket(tickets[0])
		bookings[0].add_ticket(tickets[1])
		bookings[1].add_ticket(tickets[2])
		bookings[2].add_ticket(tickets[3])

		self.database["Passangers"] = Passangers
		self.database["bookings"] = bookings
		self.database["flights"] = flights
		self.database["tickets"] = tickets


	def print_database(self):
		for key in self.database:
			for x in self.database[key]:
				print(x)

	def init_question_asnwers_map(self):
		self.questions_to_answers = {"hi" : ("Hello, how may I help you today?", Bot.no_action),
						"could you tell me the waiting time" : 
							("The security waiting time at the Schipol Airport is aproximately 5 minutes.", Bot.no_action),
						"goodbye": ("Goodbye, have a pleasant day.", self.stop )}

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
		"""Transcribe speech from recorded from `microphone`.

		Returns a dictionary with three keys:
		"success": a boolean indicating whether or not the API request was
				   successful
		"error":   `None` if no error occured, otherwise a string containing
				   an error message if the API could not be reached or
				   speech was unrecognizable
		"transcription": `None` if speech could not be transcribed,
				   otherwise a string containing the transcribed text
		"""

		# adjust the recognizer sensitivity to ambient noise and record audio
		# from the microphone
		with self.microphone as source:
			self.recognizer.adjust_for_ambient_noise(source)
			audio = self.recognizer.listen(source)

		# set up the response object
		response = {
			"success": True,
			"error": None,
			"transcription": None
		}

		try:
			response["transcription"] = self.recognizer.recognize_google(audio)
		except sr.RequestError:
			# API was unreachable or unresponsive
			response["success"] = False
			response["error"] = "API unavailable"
		except sr.UnknownValueError:
			# speech was unintelligible
			response["error"] = "Unable to recognize speech"

		return response


	def no_action():
		pass

	def stop(self):
		self.run = False
	
	def run(self):
		self.run = True
		while self.run:
			print("How may I help you?")
			question = self.recognize_speech_from_mic()
			if not question["success"]:
				self.speak("I didn't catch that. Could you repeat please?\n")
				continue

			# if there was an error, stop the game
			if question["error"]:
				self.speak("ERROR: {}".format(question["error"]))
				continue

			# show the user the transcription
			print("You said: {}".format(question["transcription"]))

			for re_exp in self.questions_to_answers.keys():
				if not re.match(re_exp, question["transcription"]):
					continue
				# Speak the message
				self.speak(self.questions_to_answers[re_exp][0])
				# Perform the action
				self.questions_to_answers[re_exp][1]()

if __name__ == "__main__":
	bot = Bot()
	bot.run()

   
