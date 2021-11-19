import unittest
from unittest.case import expectedFailure
from LayoverMeeting import LayoverMeeting
from LayoverUser import LayoverUser
import json
import numpy as np
# from app.routes import sum
# import BaseCase
# from routes import sum
# from app import routes


class BaseCase(unittest.TestCase):
	def setUp(self):
		self.simpleMeeting = LayoverMeeting(
			"4K93mf", "MyMeeting", "in_person", 15, "general_week", "", "", 8, 18)

		self.meetingWithUser = LayoverMeeting(
			"8Uk4mL", "Andrea's Meeting", "in_person", 30, "general_week", "", "", 8, 18)
		self.newUser = LayoverUser("John Doe", "jd@gmail.com", "K92fke")
		self.newUser2 = LayoverUser("Jane Street", "js@gmail.com", "K92fke")
		self.meetingWithUser.addUser(self.newUser)
		self.meetingWithUser.addUser(self.newUser2)

		self.meetingHrLong = LayoverMeeting(
			"93k2lf", "Eric's Meeting", "in_person", 60, "general_week", "", "", 8, 18)

		self.numRows = (18-8) * 4

		# this statement will be executed before testing

	def tearDown(self):
		pass
		# this statement will be executed after testing


class TestLayoverMeeting(BaseCase):

	def testSimpleGetMeetingId(self):
		meeting = self.simpleMeeting
		self.assertEqual(meeting.getMeetingID(), "4K93mf")

	def testSimpleGetName(self):
		meeting = self.simpleMeeting
		self.assertEqual(meeting.getName(), "MyMeeting")

	def testSimpleGetLength(self):
		meeting = self.simpleMeeting
		self.assertEqual(meeting.getLength(), 15)

	def testSimpleGetMeetingType(self):
		meeting = self.simpleMeeting
		self.assertEqual(meeting.getMeetingType(), "in_person")

	def testSimpleGetDateType(self):
		meeting = self.simpleMeeting
		self.assertEqual(meeting.getDateType(), "general_week")

	def testSimpleGetStartTime(self):
		meeting = self.simpleMeeting
		self.assertEqual(meeting.getStartTime(), 8)

	def testSimpleGetEndTime(self):
		meeting = self.simpleMeeting
		self.assertEqual(meeting.getEndTime(), 18)

	def testSimpleToJSON(self):
		meeting = self.simpleMeeting
		actualDict = json.loads(meeting.toJSON())
		expectedJSON = {
			"date_type": "general_week",
			"day_end_time": 18,
			"day_start_time": 8,
			"end_date": "",
			"meeting_id": "4K93mf",
			"meeting_length": 15,
			"meeting_type": "in_person",
			"name": "MyMeeting",
			"start_date": "",
			"users": {}
		}
		self.assertDictEqual(actualDict, expectedJSON)

	def testAddAndGetUser(self):
		meeting = self.meetingWithUser
		self.assertEqual(meeting.getUser("jd@gmail.com"), self.newUser)

	def testGetNonExistantUser(self):
		meeting = self.meetingWithUser
		self.assertEqual(meeting.getUser("ff@gmail.com"), None)

	def testAddMultipleUsers(self):
		meeting = self.meetingWithUser
		self.assertEqual(meeting.getUser("jd@gmail.com"), self.newUser)
		self.assertEqual(meeting.getUser("js@gmail.com"), self.newUser2)

	def testGetMultipleUsers(self):
		meeting = self.meetingWithUser
		self.assertListEqual(list(meeting.getUsers()), [
			"jd@gmail.com", "js@gmail.com"])

	def testCompiledAvailWithNoUsers(self):
		meeting = self.simpleMeeting
		self.assertTrue(np.array_equal(
			meeting.compiledAvailability(True), np.zeros((self.numRows, 7))))

	def testCompiledAvailNoUserInputAvail(self):
		meeting = self.simpleMeeting
		meeting.addUser(self.newUser)
		self.assertTrue(np.array_equal(
			meeting.compiledAvailability(True), np.zeros((self.numRows, 7))))

	def testCompiledAvailSingleUser(self):
		meeting = self.simpleMeeting
		avail = [[0, 0, 0, 0, 0, 0, 0] for i in range(self.numRows)]
		avail[0][0] = 1
		avail[1][0] = 1
		avail[2][0] = 1
		self.newUser.setAvailability(avail, None)
		meeting.addUser(self.newUser)

		actual = meeting.compiledAvailability(True)
		expected = np.zeros((self.numRows, 7))
		expected[0][0] = 1
		expected[1][0] = 1
		expected[2][0] = 1

		self.assertTrue(np.array_equal(actual, expected))

	def testCompiledAvailTwoUserFullOverlap(self):
		meeting = self.simpleMeeting
		avail = [[0, 0, 0, 0, 0, 0, 0] for i in range(self.numRows)]
		avail[0][0] = 1
		avail[1][0] = 1
		avail[2][0] = 1
		self.newUser.setAvailability(avail, None)
		self.newUser2.setAvailability(avail, None)
		meeting.addUser(self.newUser)
		meeting.addUser(self.newUser2)

		actual = meeting.compiledAvailability(True)
		expected = np.zeros((self.numRows, 7))
		expected[0][0] = 1
		expected[1][0] = 1
		expected[2][0] = 1

		self.assertTrue(np.array_equal(actual, expected))

	def testCompiledAvailTwoUserPartialOverlap(self):
		meeting = self.simpleMeeting
		avail1 = [[0, 0, 0, 0, 0, 0, 0] for i in range(self.numRows)]
		avail1[0][0] = 1
		avail1[1][0] = 1
		avail1[2][0] = 1

		avail2 = [[0, 0, 0, 0, 0, 0, 0] for i in range(self.numRows)]
		avail2[1][0] = 1
		avail2[2][0] = 1
		avail2[3][0] = 1

		self.newUser.setAvailability(avail1, None)
		self.newUser2.setAvailability(avail2, None)

		meeting.addUser(self.newUser)
		meeting.addUser(self.newUser2)

		actual = meeting.compiledAvailability(True)
		expected = np.zeros((self.numRows, 7))

		expected[0][0] = 0.5
		expected[1][0] = 1
		expected[2][0] = 1
		expected[3][0] = 0.5

		self.assertTrue(np.array_equal(actual, expected))

	def testCompiledAvailTwoUserNoOverlap(self):
		meeting = self.simpleMeeting
		avail1 = [[0, 0, 0, 0, 0, 0, 0] for i in range(self.numRows)]
		avail1[0][0] = 1
		avail1[1][0] = 1
		avail1[2][0] = 1

		avail2 = [[0, 0, 0, 0, 0, 0, 0] for i in range(self.numRows)]
		avail2[0][1] = 1
		avail2[1][1] = 1
		avail2[2][1] = 1

		self.newUser.setAvailability(avail1, None)
		self.newUser2.setAvailability(avail2, None)

		meeting.addUser(self.newUser)
		meeting.addUser(self.newUser2)

		actual = meeting.compiledAvailability(True)
		expected = np.zeros((self.numRows, 7))

		expected[0][0] = 1
		expected[1][0] = 1
		expected[2][0] = 1
		expected[0][1] = 1
		expected[1][1] = 1
		expected[2][1] = 1
		self.assertTrue(np.array_equal(actual, expected))

	def testCompiledAvailTwoUserPartialOverlapVirtual(self):
		meeting = self.simpleMeeting
		avail1 = [[0, 0, 0, 0, 0, 0, 0] for i in range(self.numRows)]
		avail1[0][0] = 1
		avail1[1][0] = 1
		avail1[2][0] = 1

		avail2 = [[0, 0, 0, 0, 0, 0, 0] for i in range(self.numRows)]
		avail2[1][0] = 1
		avail2[2][0] = 1
		avail2[3][0] = 1

		self.newUser.setAvailability(None, avail1)
		self.newUser2.setAvailability(None, avail2)

		meeting.addUser(self.newUser)
		meeting.addUser(self.newUser2)

		actual = meeting.compiledAvailability(False)
		expected = np.zeros((self.numRows, 7))

		expected[0][0] = 0.5
		expected[1][0] = 1
		expected[2][0] = 1
		expected[3][0] = 0.5

		self.assertTrue(np.array_equal(actual, expected))

	def testBestTimesEmptyAvail(self):
		meeting = self.simpleMeeting
		actual = meeting.bestMeetingTimes(meeting.compiledAvailability(True))[1]
		expected = []
		# Order is not relevant so use countEqual
		self.assertCountEqual(actual, expected)

	def testBestTimesSingleUser(self):
		meeting = self.simpleMeeting
		avail = [[0, 0, 0, 0, 0, 0, 0] for i in range(self.numRows)]
		avail[0][0] = 1
		avail[1][0] = 1
		avail[2][0] = 1
		self.newUser.setAvailability(avail, None)
		meeting.addUser(self.newUser)

		actual = meeting.bestMeetingTimes(meeting.compiledAvailability(True))[1]
		expected = ['Sunday 08:00', 'Sunday 08:15', 
					'Sunday 08:30']
		# Order is not relevant so use countEqual
		self.assertCountEqual(actual, expected)

	def testBestTimesTwoUserNoOverlap(self):
		meeting = self.simpleMeeting
		avail1 = [[0, 0, 0, 0, 0, 0, 0] for i in range(self.numRows)]
		avail1[0][0] = 1
		avail1[1][0] = 1
		avail1[2][0] = 1

		avail2 = [[0, 0, 0, 0, 0, 0, 0] for i in range(self.numRows)]
		avail2[1][1] = 1
		avail2[2][1] = 1
		avail2[3][1] = 1

		self.newUser.setAvailability(avail1, None)
		self.newUser2.setAvailability(avail2, None)

		meeting.addUser(self.newUser)
		meeting.addUser(self.newUser2)

		actual = meeting.bestMeetingTimes(meeting.compiledAvailability(True))[1]
		expected = ['Sunday 08:00', 'Sunday 08:15', 
					'Sunday 08:30', 'Monday 08:15', 'Monday 08:30']
		# Order is not relevant so use countEqual
		self.assertCountEqual(actual, expected)

	def testBestTimesTwoUserSingleOverlap(self):
		meeting = self.simpleMeeting
		avail1 = [[0, 0, 0, 0, 0, 0, 0] for i in range(self.numRows)]
		avail1[0][0] = 1
		avail1[1][0] = 1
		avail1[2][0] = 1
		avail1[5][6] = 1

		avail2 = [[0, 0, 0, 0, 0, 0, 0] for i in range(self.numRows)]
		avail2[1][1] = 1
		avail2[2][1] = 1
		avail2[3][1] = 1
		avail2[5][6] = 1

		self.newUser.setAvailability(avail1, None)
		self.newUser2.setAvailability(avail2, None)

		meeting.addUser(self.newUser)
		meeting.addUser(self.newUser2)

		actual = meeting.bestMeetingTimes(meeting.compiledAvailability(True))[1]
		expected = ['Saturday 09:15', 'Sunday 08:00', 
					'Sunday 08:15', 'Sunday 08:30', 'Monday 08:15']
		# Order is not relevant so use countEqual
		self.assertCountEqual(actual, expected)

	def testBestTimesTwoUserMultipleOverlap(self):
		meeting = self.simpleMeeting
		avail1 = [[0, 0, 0, 0, 0, 0, 0] for i in range(self.numRows)]
		avail1[0][2] = 1
		avail1[1][2] = 1
		avail1[2][2] = 1
		avail1[3][2] = 1
		avail1[1][3] = 1
		avail1[2][3] = 1
		avail1[3][3] = 1
		avail1[4][3] = 1
		avail1[2][6] = 0.75
		avail1[3][6] = 0.75

		avail2 = [[0, 0, 0, 0, 0, 0, 0] for i in range(self.numRows)]
		avail2[2][0] = 1
		avail2[3][0] = 1
		avail2[0][2] = 1
		avail2[1][2] = 1
		avail2[3][3] = 0.75
		avail2[4][3] = 0.75
		avail2[2][6] = 1

		self.newUser.setAvailability(avail1, None)
		self.newUser2.setAvailability(avail2, None)

		meeting.addUser(self.newUser)
		meeting.addUser(self.newUser2)

		actual = meeting.bestMeetingTimes(meeting.compiledAvailability(True))[1]
		expected = ['Tuesday 08:00', 'Tuesday 08:15', 
					'Wednesday 08:45', 'Wednesday 09:00', 'Saturday 08:30']
		# Order is not relevant so use countEqual
		self.assertCountEqual(actual, expected)

	def testGoodTimesShorterThanMeetingInterval(self):
		# If user wants a 1hr meeting but only 15 or 30 minute slots open

		meeting = self.meetingHrLong
		avail1 = [[0, 0, 0, 0, 0, 0, 0] for i in range(self.numRows)]

		# Sun
		avail1[0][0] = 1
		avail1[1][0] = 0.75
		avail1[2][0] = 1
		avail1[3][0] = 0.75

		# Tue
		avail1[0][2] = 1
		avail1[1][2] = 1

		# Wed
		avail1[3][3] = 0.75
		avail1[4][3] = 0.75

		# Fri
		avail1[0][5] = 1
		avail1[1][5] = 1
		avail1[2][5] = 1
		avail1[3][5] = 1

		# Sat
		avail1[1][6] = 1
		avail1[3][6] = 0.75

		avail2 = [[0, 0, 0, 0, 0, 0, 0] for i in range(self.numRows)]
		# Sun
		avail2[0][0] = 1
		avail2[1][0] = 0.75
		avail2[2][0] = 1
		avail2[3][0] = 0.75

		# Tue
		avail2[0][2] = 1
		avail2[1][2] = 1

		# Wed
		avail2[3][3] = 0.75
		avail2[4][3] = 0.75

		# Fri
		avail2[0][5] = 1
		avail2[1][5] = 1
		avail2[2][5] = 1
		avail2[3][5] = 1
		avail2[4][5] = 0.75

		# Sat
		avail1[1][6] = 1
		avail1[3][6] = 1

		self.newUser.setAvailability(avail1, None)
		self.newUser2.setAvailability(avail2, None)

		meeting.addUser(self.newUser)
		meeting.addUser(self.newUser2)

		actual = meeting.bestMeetingTimes(meeting.compiledAvailability(True))[1]
		expected = ['Friday 08:00', 'Sunday 08:00', 
					'Friday 08:15', 'Sunday 08:15', 'Friday 08:30']  # <- these are slightly suspect. 
																	 # for example friday 8am 1 user can't 
																	 # make it and the other is maybe
																	 # yet we recommend 7:15-8:15
		# Order is not relevant so use countEqual
		self.assertCountEqual(actual, expected)
