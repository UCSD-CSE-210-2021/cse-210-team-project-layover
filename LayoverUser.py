class LayoverUser:
	def __init__(self, name, email, meeting_id):
		self.name = name
		self.email = email
		self.meeting_id = meeting_id
		self.availability = []

	def getName(self):
		return self.name

	def getID(self):
		return self.email

	def getAvailability(self):
		return self.availability
