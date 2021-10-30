import json


class LayoverMeeting:
	def __init__(self, name, init_user_email, init_user_name, meeting_type):
		self.name = name
		self.users = {init_user_email: init_user_name}
		self.meeting_type = meeting_type

	def getName(self):
		return self.name

	def getUsers(self):
		return self.users.keys()

	def getMeetingType(self):
		return self.meeting_type

	def toJSON(self):
		return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
