import json


class LayoverUser:
	def __init__(self, name: str, email: str, meeting_id: str):
		self.name = name
		self.email = email
		self.meeting_id = meeting_id
		self.availability = []

	def setAvailability(self, availability_schedule: list):
		self.availability = availability_schedule

	def getID(self):
		return self.email

	def getAvailability(self):
		return self.availability

	def toJSON(self):
		return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
