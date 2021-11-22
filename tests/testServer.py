import unittest
from LayoverMeeting import LayoverMeeting
from LayoverUser import LayoverUser
import json
import numpy as np
from server import app as flask_app, meeting
from server import meeting_db
from server import getUniqueRandomHash
from contextlib import contextmanager
from flask import template_rendered

# For checking context 
@contextmanager
def captured_templates(app):
    recorded = []
    def record(sender, template, context, **extra):
        recorded.append((template, context))
    template_rendered.connect(record, app)
    try:
        yield recorded
    finally:
        template_rendered.disconnect(record, app)

class BaseCase(unittest.TestCase):
	def setUp(self):
		self.client = flask_app.test_client()
		# this statement will be executed before testing
		self.simpleMeeting = LayoverMeeting(
			"4K93mf", "MyMeeting", "in_person", 15, "general_week", "", "", 8, 18)

		self.numRows = (18-8) * 4
		self.simpleUser1 = LayoverUser("John Doe", "jd@gmail.com", "4K93mf")
		self.simpleUser2 = LayoverUser(
			"Jane Street", "js@gmail.com", "4K93mf")
	def tearDown(self):
		meeting_db.clear()
		pass
		# this statement will be executed after testing

class TestServer(BaseCase):

	def testHashGenerator(self):

		# Random so execute 25 times to rule out chance of flaky tests 
		for _ in range(25):
			actual = getUniqueRandomHash()
			self.assertEqual(len(actual), 6)
			self.assertTrue(actual.isalnum())

	def testSimpleGetAbc(self):
		client = self.client
		res = client.get('/abc')
		self.assertEqual(res.status_code, 200)
		actual = json.loads(res.get_data())
		expected = {'hello': 'world'}
		self.assertEqual(actual, expected)

	def testSimpleHandleMeetingHappy(self):
		client = self.client
		res = client.post('/handle_meeting_creation', data={
			"meeting_name": "yaba",
			"meeting_type": "wok",
			"meeting_length" : 15,
			"start_time": 8,
			"end_time": 18
	 	}, content_type="application/x-www-form-urlencoded") # Mark it as a form

		# Check status code
		self.assertEqual(res.status_code, 302)
		
		# Verify server side state
		self.assertEqual(len(meeting_db), 1)

		# The only meeting key
		k = list(meeting_db)[0]
		
		# Check meetings are equivalent
		actual = meeting_db[k]
		expected = LayoverMeeting(k, "yaba", "wok", 15, "general_week", '','', 8, 18)
		self.assertEqual(actual, expected)
		
	
	def testSimpleHandleMeetingBadRequest(self):
		client = self.client
		res = client.post('/handle_meeting_creation', data={
			# "meeting_name": "yaba", <- missing field
			"meeting_type": "wok",
			"meeting_length" : 15,
			"start_time": 8,
			"end_time": 18
	 	}, content_type="application/x-www-form-urlencoded") # Mark it as a form

		# Check status code
		self.assertEqual(res.status_code, 400)
		
		# Verify server side dictionary store is empty
		self.assertEqual(len(meeting_db), 0)

	def testSimpleHandleMeetingBadEndpoint(self):
		client = self.client
		res = client.post('/handle_meeting_crea', data={
			"meeting_name": "yaba", 
			"meeting_type": "wok",
			"meeting_length" : 15,
			"start_time": 8,
			"end_time": 18
	 	}, content_type="application/x-www-form-urlencoded") # Mark it as a form

		# Check status code
		self.assertEqual(res.status_code, 404)
		
		# Verify server side dictionary store is empty
		self.assertEqual(len(meeting_db), 0)


	def testSimpleHandleUserInfo(self):
		client = self.client
		
		# Create the meeting
		meeting = self.simpleMeeting
		meeting_db[meeting.getMeetingID()] = meeting
		
		# Assume simple meeting already exists with id: 4K93mf
		res = client.post('/handle_user_info', data={
			"display_name": "John Doe", 
			"email": "jd@gmail.com",
			"meeting_id" : "4K93mf"
	 	}, content_type="application/x-www-form-urlencoded") # Mark it as a form

		# Check status code
		self.assertEqual(res.status_code, 302)
		
		actualMeeting = meeting_db[meeting.getMeetingID()]
		actualUser = actualMeeting.getUser("jd@gmail.com")

		# Check number of users
		self.assertEqual(len(actualMeeting.getUsers()), 1)

		expectedUser = self.simpleUser1
		# Verify user is correct
		self.assertEqual(actualUser, expectedUser)


	def testSimpleHandleUserInfoMultipleUser(self):
		client = self.client

		# Create the meeting
		meeting = self.simpleMeeting
		meeting_db[meeting.getMeetingID()] = meeting
		
		# Assume simple meeting already exists with id: 4K93mf
		res = client.post('/handle_user_info', data={
			"display_name": "John Doe", 
			"email": "jd@gmail.com",
			"meeting_id" : "4K93mf"
	 	}, content_type="application/x-www-form-urlencoded") # Mark it as a form

		# Check status code
		self.assertEqual(res.status_code, 302)

		res = client.post('/handle_user_info', data={
			"display_name": "Jane Street", 
			"email": "js@gmail.com",
			"meeting_id" : "4K93mf"
	 	}, content_type="application/x-www-form-urlencoded") # Mark it as a form

		# Check status code
		self.assertEqual(res.status_code, 302)
		
		actualMeeting = meeting_db[meeting.getMeetingID()]
		actualUser = actualMeeting.getUser("jd@gmail.com")

		# Check number of users
		self.assertEqual(len(actualMeeting.getUsers()), 2)

		expectedUser = self.simpleUser1
		# Verify user is correct
		self.assertEqual(actualUser, expectedUser)

		actualUser = actualMeeting.getUser("js@gmail.com")
		expectedUser = self.simpleUser2
		# Verify user is correct
		self.assertEqual(actualUser, expectedUser)


	def testSimpleHandleUserInfoDuplicateUser(self):
		client = self.client

		# Create the meeting
		meeting = self.simpleMeeting
		meeting_db[meeting.getMeetingID()] = meeting
		
		# Assume simple meeting already exists with id: 4K93mf
		res = client.post('/handle_user_info', data={
			"display_name": "John Doe", 
			"email": "jd@gmail.com",
			"meeting_id" : "4K93mf"
	 	}, content_type="application/x-www-form-urlencoded") # Mark it as a form

		# Check status code
		self.assertEqual(res.status_code, 302)

		res = client.post('/handle_user_info', data={
			"display_name": "John Doe", 
			"email": "jd@gmail.com",
			"meeting_id" : "4K93mf"
	 	}, content_type="application/x-www-form-urlencoded") # Mark it as a form

		# Check status code
		self.assertEqual(res.status_code, 302)
		
		actualMeeting = meeting_db[meeting.getMeetingID()]
		actualUser = actualMeeting.getUser("jd@gmail.com")

		# Check number of users
		self.assertEqual(len(actualMeeting.getUsers()), 1)

		expectedUser = self.simpleUser1
		# Verify user is correct
		self.assertEqual(actualUser, expectedUser)


	def testSimpleHandleUserInfoUpdateUser(self):
		client = self.client

		# Create the meeting
		meeting = self.simpleMeeting
		meeting_db[meeting.getMeetingID()] = meeting
		
		# Assume simple meeting already exists with id: 4K93mf
		res = client.post('/handle_user_info', data={
			"display_name": "John Doe", 
			"email": "jd@gmail.com",
			"meeting_id" : "4K93mf"
	 	}, content_type="application/x-www-form-urlencoded") # Mark it as a form

		# Check status code
		self.assertEqual(res.status_code, 302)

		res = client.post('/handle_user_info', data={
			"display_name": "James Don", 
			"email": "jd@gmail.com",
			"meeting_id" : "4K93mf"
	 	}, content_type="application/x-www-form-urlencoded") # Mark it as a form

		# Check status code
		self.assertEqual(res.status_code, 302)
		
		actualMeeting = meeting_db[meeting.getMeetingID()]
		actualUser = actualMeeting.getUser("jd@gmail.com")

		# Check number of users
		self.assertEqual(len(actualMeeting.getUsers()), 1)

		expectedUser = self.simpleUser1
		# Verify user is correct
		self.assertEqual(actualUser, expectedUser)


	def testSimpleSubmitAvailabilityEmpty(self):
		client = self.client

		# Create meeting. Assume handle_meeting_setup and handle_user_info 
		# functions correctly
		meeting = self.simpleMeeting
		meeting.addUser(self.simpleUser1)
		meeting_db[meeting.getMeetingID()] = meeting
		inPerson = [[0, 0, 0, 0, 0, 0, 0] for _ in range(self.numRows)]
		virtual = [[0, 0, 0, 0, 0, 0, 0] for _ in range(self.numRows)]

		res = client.post('/submitAvailability', json={
			"inPersonMeetingTable": inPerson,
			"virtualMeetingTable": virtual,
			"meeting_id" : meeting.getMeetingID() ,
			"email": "jd@gmail.com"
			}) # Mark it as a form

		# Check status code
		self.assertEqual(res.status_code, 200)
		
		actualMeeting = meeting_db[meeting.getMeetingID()]
		actualUser = actualMeeting.getUser("jd@gmail.com")
		
		# Verify availability is set
		self.assertEqual(actualUser.getInPersonAvailability(), inPerson)
		self.assertEqual(actualUser.getVirtualAvailability(), virtual)



	def testSimpleSubmitAvailabilityCompleted(self):
		client = self.client

		# Create meeting. Assume handle_meeting_setup and handle_user_info 
		# functions correctly
		meeting = self.simpleMeeting
		meeting.addUser(self.simpleUser1)
		meeting_db[meeting.getMeetingID()] = meeting
		inPerson = [[0, 0, 0, 0, 0, 0, 0] for _ in range(self.numRows)]
		virtual = [[0, 0, 0, 0, 0, 0, 0] for _ in range(self.numRows)]

		inPerson[3][4] = 1
		inPerson[1][1] = 1
		inPerson[30][6] = 0.75
		inPerson[1][2] = 0.75

		virtual[1][1] = 1
		virtual[2][2] = 1
		virtual[4][4] = 0.75
		virtual[5][1] = 0.75

		res = client.post('/submitAvailability', json={
			"inPersonMeetingTable": inPerson,
			"virtualMeetingTable": virtual,
			"meeting_id" : meeting.getMeetingID() ,
			"email": "jd@gmail.com"
			}) # Mark it as a form

		# Check status code
		self.assertEqual(res.status_code, 200)
		
		actualMeeting = meeting_db[meeting.getMeetingID()]
		actualUser = actualMeeting.getUser("jd@gmail.com")
		
		# Verify availability is set
		self.assertEqual(actualUser.getInPersonAvailability(), inPerson)
		self.assertEqual(actualUser.getVirtualAvailability(), virtual)

	def testGetRootDoc(self):
		with flask_app.test_client() as c:
			with captured_templates(flask_app) as templates:
				res = c.get('/')
				self.assertEqual(res.status_code, 200)
				template, context = templates[0]
				self.assertEqual(template.name, 'setup-landing.html')

	def testGetMeetingDetails(self):
		with flask_app.test_client() as c:
			with captured_templates(flask_app) as templates:
				meeting = self.simpleMeeting
				meeting_db[meeting.getMeetingID()] = meeting
				res = c.get('/meeting/' + meeting.getMeetingID())
				self.assertEqual(res.status_code, 200)

				template, context = templates[0]
				self.assertEqual(template.name, 'scheduling-landing.html')
				
				self.assertEqual(context['data'], meeting.toJSON())

	def testGetMeetingDetailsNonExistant(self):
		c = self.client
		meeting = self.simpleMeeting
		res = c.get('/meeting/' + meeting.getMeetingID())
		self.assertEqual(res.status_code, 500)


	def testGetAvailabilityDetails(self):
		with flask_app.test_client() as c:
			with captured_templates(flask_app) as templates:
				meeting = self.simpleMeeting
				user = self.simpleUser1
				meeting_db[meeting.getMeetingID()] = meeting
				meeting.addUser(user)
				res = c.get('/availability/' + meeting.getMeetingID() + '/' + user.getID())
				self.assertEqual(res.status_code, 200)

				template, context = templates[0]
				self.assertEqual(template.name, 'scheduling-availability.html')

				self.assertEqual(context['data'], user.toJSON())
				self.assertEqual(context['meeting'], meeting.toJSON())

	def testGetResultDetails(self):
		with flask_app.test_client() as c:
			with captured_templates(flask_app) as templates:
				meeting = self.simpleMeeting
				user = self.simpleUser1

				inPerson = [[0, 0, 0, 0, 0, 0, 0] for _ in range(self.numRows)]
				virtual = [[0, 0, 0, 0, 0, 0, 0] for _ in range(self.numRows)]

				inPerson[3][4] = 1
				inPerson[1][1] = 1
				inPerson[30][6] = 0.75
				inPerson[1][2] = 0.75

				virtual[1][1] = 1
				virtual[2][2] = 1
				virtual[4][4] = 0.75
				virtual[5][1] = 0.75

				user.setAvailability(inPerson, virtual)
				meeting_db[meeting.getMeetingID()] = meeting
				meeting.addUser(user)
				res = c.get('/results/' + meeting.getMeetingID())
				self.assertEqual(res.status_code, 200)

				template, context = templates[0]
				self.assertEqual(template.name, 'results.html')

				expectedMeetingInfo = meeting.toJSON()
				combinedResultsInPerson = meeting.compiledAvailability(True)
				expectedCompiledInPerson = json.dumps(combinedResultsInPerson.tolist())
				expectedBestInPersonTimesIdx = json.dumps(meeting.bestMeetingTimes(combinedResultsInPerson)[0])
				expectedBestInPersonTimes = json.dumps(meeting.bestMeetingTimes(combinedResultsInPerson)[1])
				combinedResultsVirtual = meeting.compiledAvailability(False)
				expectedCompiledVirtual = json.dumps(combinedResultsVirtual.tolist())
				expectedBestVirtualTimesIdx = json.dumps(meeting.bestMeetingTimes(combinedResultsVirtual)[0])
				expectedBestVirtualTimes = json.dumps(meeting.bestMeetingTimes(combinedResultsVirtual)[1])

				expectedData = '{"meeting_info":' + expectedMeetingInfo + ',"compiled_inperson":' + expectedCompiledInPerson + ',"best_times_inperson":' \
				+ expectedBestInPersonTimes + ',"best_times_idx_inperson":' + expectedBestInPersonTimesIdx + ',"compiled_virtual":' + expectedCompiledVirtual + \
				',"best_times_virtual":' + expectedBestVirtualTimes  + ',"best_times_idx_virtual":' + expectedBestVirtualTimesIdx + '}'

				self.assertEqual(context['data'], expectedData)