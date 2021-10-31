import json


class LayoverMeeting:
	def __init__(self, meeting_id, name, meeting_type, date_type, start_date, end_date):
		self.meeting_id = meeting_id
		self.name = name
		self.users = dict()
		self.meeting_type = meeting_type
		self.date_type = date_type
		self.start_date = start_date
		self.end_date = end_date
		if self.date_type == "general_week":
			self.start_date = ""
			self.end_date = ""

	def getMeetingID(self):
		return self.meeting_id

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
