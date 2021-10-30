import json


class LayoverMeeting:
	def __init__(self, name, meeting_type, date_type, start_date, end_date):
		self.name = name
		self.users = dict()
		self.meeting_type = meeting_type
		self.date_type = date_type
		self.start_date = start_date
		self.end_date = end_date

	def getName(self):
		return self.name

	def getUsers(self):
		return self.users.keys()

	def getMeetingType(self):
		return self.meeting_type

	def getDateType(self):
		return self.date_type

	def toJSON(self):
		return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
