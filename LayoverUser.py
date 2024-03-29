import json


class LayoverUser:

	def __init__(self, name: str, email: str, meeting_id: str):
		self.name = name
		self.email = email
		self.meeting_id = meeting_id
		self.inPersonAvailability = None
		self.virtualAvailability = None

	def setAvailability(self, inPersonAvailability: list, virtualAvailability: list):
		self.inPersonAvailability = inPersonAvailability
		self.virtualAvailability = virtualAvailability

	def getName(self):
		return self.name

	def getMeetingID(self):
		return self.meeting_id

	def getID(self):
		return self.email

	def getInPersonAvailability(self):
		return self.inPersonAvailability

	def getVirtualAvailability(self):
		return self.virtualAvailability

	def toJSON(self):
		return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

	def __eq__(self, other):

		if isinstance(other, LayoverUser) and other.toJSON() == self.toJSON():
			return True

		return False
