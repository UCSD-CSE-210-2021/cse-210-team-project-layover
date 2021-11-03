class LayoverUser:
	def __init__(self, name, email, meeting_id):
		self.name = name
		self.email = email
		self.meeting_id = meeting_id
		self.availability = []

<<<<<<< HEAD
	def getName(self):
		return self.name
=======
	def setAvailability(self, availability_schedule):
		self.availability = availability_schedule
>>>>>>> origin/alexyen

	def getID(self):
		return self.email

	def getAvailability(self):
<<<<<<< HEAD
		return self.availability
=======
		return self.availability
>>>>>>> origin/alexyen
