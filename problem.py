class Problem:
	id = 0

	def __init__(self, content):
		self.id = Problem.id
		Problem.id += 1
		self.content = content
		self.type = ""
		self.information = {}

	def set_content(self, content):
		self.content = content

	def __str__(self):
		return "Problem ({}, {})".format(self.id, self.content)