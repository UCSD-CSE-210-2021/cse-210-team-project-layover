import json
import numpy as np


class LayoverMeeting:
	def __init__(self, meeting_id: str, name: str, meeting_type: str, meeting_length: int, date_type: str, start_date, end_date):
		self.meeting_id = meeting_id
		self.name = name
		self.users = dict()
		self.meeting_type = meeting_type
		self.meeting_length = meeting_length
		self.date_type = date_type
		self.start_date = start_date
		self.end_date = end_date
		if self.date_type == "general_week":
			self.start_date = ""
			self.end_date = ""
		self.schedule_results = None

	def getMeetingID(self):
		return self.meeting_id

	def getName(self):
		return self.name

	def getUsers(self):
		return self.users.keys()

	def getUser(self, userKey):
		try:
			return self.users[userKey]
		except KeyError:
			return None

	def getLength(self):
		return self.meeting_length

	def getMeetingType(self):
		return self.meeting_type

	def getDateType(self):
		return self.date_type

	def addUser(self, newUser):
		self.users[newUser.getID()] = newUser

	def toJSON(self):
		return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

	def compiledAvailability(self):
		userKeys = list(self.getUsers())

		# initializing template via first key
		user0 = self.getUser(userKeys[0])
		user0_availabiliy = np.array(user0.getAvailability())
		compiled_schedule = np.zeros(user0_availabiliy.shape)
		
		for userKey in userKeys:
			user = self.getUser(userKey)
			user_availability = user.getAvailability()
			compiled_schedule += user_availability

		max_val = np.max(compiled_schedule)
		compiled_schedule /= max_val

		# if want list of lists,
		# comment the following line and uncomment the rest of the code
		self.schedule_results = compiled_schedule

		# compiled_schedule_list = list()
		# for i in range(compiled_schedule.shape[0]):
		# 	compiled_schedule_list.append(compiled_schedule[i])
		# self.schedule_results = compiled_schedule_list