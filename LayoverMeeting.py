import json
import numpy as np
from datetime import time, timedelta
from datetime import datetime


class LayoverMeeting:
	def __init__(self, meeting_id: str, name: str, meeting_type: str, meeting_length: int, date_type: str, start_date: None, end_date: None):
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

		# Initializing template via hard coding
		# TODO: make compiled schedule dynamic, but not reliant on a key in case no availabilities added yet
		# user0 = self.getUser(userKeys[0])
		# user0_availability = np.array(user0.getInPersonAvailability())
		compiled_schedule = np.zeros((64, 7))

		for userKey in userKeys:
			user = self.getUser(userKey)
			user_availability = user.getInPersonAvailability()
			compiled_schedule += user_availability

		max_val = np.max(compiled_schedule)
		compiled_schedule /= max_val

		# self.combined_results = compiled_schedule
		# if want list of lists,
		# comment the following line and uncomment the rest of the code
		return compiled_schedule

		# compiled_schedule_list = list()
		# for i in range(compiled_schedule.shape[0]):
		# 	compiled_schedule_list.append(compiled_schedule[i])
		# self.schedule_results = compiled_schedule_list

	def bestMeetingTimes(self):
		compiled_list = self.compiledAvailability()

		start_ind = 0
		end_ind = start_ind + self.meeting_length

		start_time = datetime(2021, 11, 4, hour=7)  # dummy values, must change in future
		end_time = datetime(2021, 11, 4, hour=22)
		week_dict = {0: 'Sunday', 1: 'Monday', 2: 'Tuesday', 3: 'Wednesday', 4: 'Thursday', 5: 'Friday', 6: 'Saturday'}


		best_five = {} #k:v where k = sum of compiled availabilities over the potential meeting times, and v = (day index, time index) tuple
		for day_idx, day in enumerate(compiled_list.T):
			start_ind = 0
			end_ind = start_ind + self.meeting_length
			while end_ind <= len(day):
				curr_sum = sum(day[start_ind:end_ind])

				if best_five:
					#check if curr sum is greater than any of the current top 5 or list does not have 5 times yet
					for i in sorted(best_five):
						if curr_sum > i or len(best_five) < 5:
							best_five[curr_sum] = (day_idx, start_ind)

							#if length is larger than 5, pop the smallest key
							if len(best_five) > 5:
								best_five.pop(sorted(best_five)[0])
							# break out of loop so we don't pop more than one
							break

				else:  # if dict is empty add in first value
					best_five[curr_sum] = (day_idx, start_ind)

				start_ind += 1
				end_ind += 1

		best_times = []
		for i in sorted(best_five):
			datetime_tostr = start_time+timedelta(minutes=(15*best_five[i][1]))
			best_times.insert(0, (week_dict[best_five[i][0]] + ' ' + datetime_tostr.strftime("%H:%M")))
		return(best_times)
		# self.schedule_results = best_times

