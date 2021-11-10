import json
import numpy as np
from itertools import groupby
from datetime import time, timedelta
from datetime import datetime


class LayoverMeeting:
	def __init__(self, meeting_id: str, name: str, meeting_type: str, meeting_length: int, date_type: str, start_date: None, end_date: None):
		# meeting ID (randomized characters)
		self.meeting_id = meeting_id

		# meeting name
		self.name = name

		# intitialize dictionary of users
		self.users = dict()

		# in-person or remote
		self.meeting_type = meeting_type

		# this variable refers to the time interval (e.g. 15 minutes)
		self.meeting_length = meeting_length

		self.date_type = date_type
		self.start_date = start_date
		self.end_date = end_date
		if self.date_type == "general_week":
			self.start_date = ""
			self.end_date = ""
		
		# hard coding these values initially; start and end times for the day
		self.day_start_time = 7
		self.day_end_time = 23

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

	def compiledAvailability(self, inPerson: bool):
		userKeys = list(self.getUsers())

		# Initializing template via hard coding
		# TODO: make compiled schedule dynamic, but not reliant on a key in case no availabilities added yet

		# Alex: why would you call this function though if there are no user availabilities to compile...?

		# user0 = self.getUser(userKeys[0])
		# user0_availability = np.array(user0.getInPersonAvailability())
		num_blocks_in_day = int((self.day_end_time - self.day_start_time) * (60 / self.meeting_length))

		# WARNING: FOLLOWING VALUE IS HARD CODED
		num_days = 7
		compiled_schedule = np.zeros((num_blocks_in_day, num_days))

		for userKey in userKeys:
			user = self.getUser(userKey)
			user_availability = np.array(user.getInPersonAvailability())

			# If virtual availability is desired, use the getVirtualAvailability item
			if not inPerson:
				user_availability = np.array(user.getVirtualAvailability())

			if user_availability is None:
				continue
			compiled_schedule += user_availability

		if len(userKeys) > 0:
			max_val = np.max(compiled_schedule)
			if max_val > 0:
				compiled_schedule /= max_val

		# self.combined_results = compiled_schedule
		# if want list of lists,
		# comment the following line and uncomment the rest of the code
		return compiled_schedule

		# compiled_schedule_list = list()
		# for i in range(compiled_schedule.shape[0]):
		# 	compiled_schedule_list.append(compiled_schedule[i])
		# self.schedule_results = compiled_schedule_list

	def bestMeetingTimes(self, compiled_list):
		# compiled_list = self.compiledAvailability()
		# print(compiled_list)

		start_ind = 0
		end_ind = start_ind + self.meeting_length

		start_time = datetime(2021, 11, 4, hour=7)  # dummy values, must change in future
		end_time = datetime(2021, 11, 4, hour=22)
		week_dict = {0: 'Sunday', 1: 'Monday', 2: 'Tuesday', 3: 'Wednesday', 4: 'Thursday', 5: 'Friday', 6: 'Saturday'}

		# key = sum of compiled availabilities over the potential meeting times, and val = (day index, time index) tuple
		best_five = {}
		for day_idx, day in enumerate(compiled_list.T):
			start_ind = 0
			end_ind = start_ind + int((self.meeting_length/15))
			while end_ind <= len(day):
				curr_sum = sum(day[start_ind:end_ind])

				if best_five:
					# check if curr sum is greater than any of the current top 5
					for i in sorted(best_five):
						if curr_sum > i or len(best_five) < 5:
							while curr_sum in best_five:
								curr_sum += 0.0001
							best_five[curr_sum] = (day_idx, start_ind)

							# if length is larger than 5, pop the smallest key
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
		return best_times

	def bestMeetingTimesV2(self, compiled_schedule):
		# print(compiled_schedule)

		start_time = self.day_start_time
		end_time = self.day_end_time
		num_blocks_in_hour = 60 / self.meeting_length #60 is hard coded b/c 60min in hour
		week_dict = {0: 'Sunday', 1: 'Monday', 2: 'Tuesday', 3: 'Wednesday', 4: 'Thursday', 5: 'Friday', 6: 'Saturday'}
		transposed_schedule = compiled_schedule.T # now each index is ordered by day; shape should be (7,64)
		assert (end_time - start_time)*num_blocks_in_hour == transposed_schedule.shape[1]
		indices = np.arange(0, transposed_schedule.shape[1], 1)

		scores_list = list()
		corresponding_string_list = list()
		for i in range(transposed_schedule.shape[0]):
			zipped_value_index = list(zip(indices, transposed_schedule[i]))
			# https://stackoverflow.com/questions/38277182/splitting-numpy-array-based-on-value
			nonzero_ranges_zipped = [list(g) for k, g in groupby(zipped_value_index, lambda x: x[1] != 0) if k]
			for zipped_range in nonzero_ranges_zipped:
				index_range, value_range = np.array(list(zip(*zipped_range)))

				# calculating score for range and time range String
				# dividing sum by length of value range because want score to be dependant on values and not length of time
				# TODO: issue with best time within a large range of values; discuss with team (calculating this score metric is a bit more complicated than Alex thought)
				score = np.sum(value_range) / len(value_range)

				#############################################################################################################
				# I think there's definitely a better way to do this... this is really disgusting
				#############################################################################################################

				# calculate the hour and minute time of the index only
				start_index = index_range[0]
				start_hour = int(start_index / num_blocks_in_hour) + start_time # int() automatically floors value
				start_minute = int((start_index % num_blocks_in_hour) * self.meeting_length)
				if start_minute == 0:
					string_start_minute = '00' # lol stupid bug...
				else:
					string_start_minute = str(start_minute)
				start_string = str(start_hour) + ':' + string_start_minute				

				# there will always be a start minute, so checking is index_range only has one value
				# NEED TO ADD {self.meeting_length} TO END MINUTE BECAUSE END TIME MUST INCLUDE LAST BLOCK OF TIME
				if len(index_range) == 1:
					end_minute = start_minute + self.meeting_length
					end_hour = start_hour
					if end_minute == 60: # need to carry over time
						end_minute = 0
						end_hour += 1

					if end_minute == 0:
						string_end_minute = '00'
					else:
						string_end_minute = str(end_minute)

					end_string = str(end_hour) + ':' + string_end_minute
					string_range = f'\"{start_string} - {end_string}\"'
					# print(f'The range of time is {string_range}')
				else:
					end_index = int(index_range[len(index_range)-1])
					end_hour = int(end_index / num_blocks_in_hour) + start_time # int() automatically floors value
					end_minute = int((end_index % num_blocks_in_hour) * self.meeting_length) + self.meeting_length

					# repeating code... gross
					if end_minute == 60: # need to carry over time
						end_minute = 0
						end_hour += 1

					if end_minute == 0:
						string_end_minute = '00'
					else:
						string_end_minute = str(end_minute)

					# calculating end_string and displaying the range of time
					end_string = str(end_hour) + ':' + string_end_minute
					string_range = f'\"{start_string} - {end_string}\"'
					# print(f'The range of time is {string_range}')

				scores_list.append(score)
				corresponding_string_list.append(string_range)

		meeting_times = list(zip(scores_list, corresponding_string_list))
		sorted_meeting_times = sorted(meeting_times, key = lambda x: x[0], reverse=True)
		best_time_list, corresponding_time_list = list(zip(*sorted_meeting_times))

		# temporary code just to show that we can output best meeting times
		n = 5
		print(f"Top {n} meeting times:")
		for i in range(n):
			print(f'{corresponding_string_list[i]} (Score: {best_time_list[i]})')


				
