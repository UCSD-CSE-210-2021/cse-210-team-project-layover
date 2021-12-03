import os
os.environ['MY_ENV'] = "testSettings.py"
import unittest
import json
from layover import app as flask_app
from layover.routes import getUniqueRandomHash
from contextlib import contextmanager
from flask import template_rendered
from layover import db
from layover.models import User, Meeting
import json

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

    # @classmethod
    # # Runs a single time before testing
    # def setUpClass(cls):
    #     db.create_all()
    
    @classmethod
    # Runs a single time before testing
    def tearDownClass(cls):
        db.drop_all()

    def setUp(self):
        self.client = flask_app.test_client()
        
        # Recreate a clean DB every test
        db.create_all()

        self.simpleMeeting = Meeting(meetingID="4K93mf", meetingName="MyMeeting", meetingType="in_person",
        meetingLength=15, dateType="general_week", startDate="", endDate="", dayStartTime=5, dayEndTime=21)
        db.session.add(self.simpleMeeting)

        self.meetingWithUser = Meeting(meetingID="8Uk4mL", meetingName="Andrea's Meeting", meetingType="in_person",
        meetingLength=30, dateType="general_week", startDate="", endDate="", dayStartTime=5, dayEndTime=21)
        
        self.numRows = (18-8) * 4

        self.simpleUser1 = User(userName="John Doe", userEmail="jd@gmail.com", meetingID="4K93mf")
        self.simpleUser2 = User(userName="Jane Street", userEmail="js@gmail.com", meetingID="4K93mf")

        self.meetingWithUser.addUser(self.simpleUser1)
        self.meetingWithUser.addUser(self.simpleUser2)

        db.session.add(self.meetingWithUser)

        self.meetingWithUserAndAvail = Meeting(meetingID="Olpw0e", meetingName="Andrea's Meeting", meetingType="in_person",
        meetingLength=30, dateType="general_week", startDate="", endDate="", dayStartTime=5, dayEndTime=21)

        self.simpleUser3 = User(userName="John Doe", userEmail="jd@gmail.com", meetingID="Olpw0e")

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

        self.simpleUser3.setAvailability(inPerson, virtual)
        self.meetingWithUserAndAvail.addUser(self.simpleUser3)
        db.session.add(self.meetingWithUserAndAvail)
        db.session.commit()

    def tearDown(self):
        # Reset DB after every test
        db.drop_all()
        # this statement will be executed after testing

class TestServer(BaseCase):

    def testHashGenerator(self):
        # Random so execute 25 times to rule out chance of flaky tests 
        for _ in range(25):
            actual = getUniqueRandomHash()
            self.assertEqual(len(actual), 6)
            self.assertTrue(actual.isalnum())

    def testSimpleHandleMeetingHappy(self):
        client = self.client
        res = client.post('/handle_meeting_creation', data={
            "meeting_name": "yaba",
            "meeting_type": "in_person",
            "meeting_length" : 15,
            "start_time": 8,
            "end_time": 18
         }, content_type="application/x-www-form-urlencoded") # Mark it as a form

        # Check status code
        self.assertEqual(res.status_code, 302)
        
        allMeetings = Meeting.query.all()

        # Verify server side state
        self.assertEqual(len(allMeetings), 4)

        # meeting = None
        for aMeeting in allMeetings:
            if aMeeting.getName() == "yaba":
                meeting = aMeeting
        
        expected = Meeting(meetingID=meeting.getMeetingID(), meetingName="yaba", meetingType="in_person",
            meetingLength=15, dateType="general_week", startDate="", endDate="", dayStartTime=8, dayEndTime=18)
        self.assertEqual(meeting, expected)


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
        self.assertEqual(len(Meeting.query.all()), 3)

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
        self.assertEqual(len(Meeting.query.all()), 3)


    def testSimpleHandleUserInfo(self):
        client = self.client
        
        # Assume simple meeting already exists with id: 4K93mf
        res = client.post('/handle_user_info', data={
            "display_name": "John Doe", 
            "email": "jd@gmail.com",
            "meeting_id" : "4K93mf"
         }, content_type="application/x-www-form-urlencoded") # Mark it as a form

        # Check status code
        self.assertEqual(res.status_code, 302)
        
        # Query db
        actualMeeting = Meeting.query.filter_by(meetingID="4K93mf").first()
        actualUser = actualMeeting.getUser("jd@gmail.com")

        # Check number of users
        self.assertEqual(len(actualMeeting.getUsers()), 1)

        expectedUser = User(userName="John Doe", userEmail="jd@gmail.com", meetingID="4K93mf")

        # Verify user is correct
        self.assertEqual(actualUser, expectedUser)


    def testSimpleHandleUserInfoMultipleUser(self):
        client = self.client

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
        
        # Query db
        actualMeeting = Meeting.query.filter_by(meetingID="4K93mf").first()
        actualUser = actualMeeting.getUser("jd@gmail.com")

        # Check number of users
        self.assertEqual(len(actualMeeting.getUsers()), 2)

        expectedUser = User(userName="John Doe", userEmail="jd@gmail.com", meetingID="4K93mf")
        # Verify user is correct
        self.assertEqual(actualUser, expectedUser)

        actualUser = actualMeeting.getUser("js@gmail.com")
        expectedUser = User(userName="Jane Street", userEmail="js@gmail.com", meetingID="4K93mf")
        # Verify user is correct
        self.assertEqual(actualUser, expectedUser)


    def testSimpleHandleUserInfoDuplicateUser(self):
        client = self.client

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
        
        # Query db
        actualMeeting = Meeting.query.filter_by(meetingID="4K93mf").first()
        actualUser = actualMeeting.getUser("jd@gmail.com")

        # Check number of users
        self.assertEqual(len(actualMeeting.getUsers()), 1)

        expectedUser = User(userName="John Doe", userEmail="jd@gmail.com", meetingID="4K93mf")
        # Verify user is correct
        self.assertEqual(actualUser, expectedUser)


    def testSimpleHandleUserInfoUpdateUser(self):
        client = self.client

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
        
        # Query db
        actualMeeting = Meeting.query.filter_by(meetingID="4K93mf").first()
        actualUser = actualMeeting.getUser("jd@gmail.com")

        # Check number of users
        self.assertEqual(len(actualMeeting.getUsers()), 1)

        expectedUser = User(userName="John Doe", userEmail="jd@gmail.com", meetingID="4K93mf")
        # Verify user is correct
        self.assertEqual(actualUser, expectedUser)


    def testSimpleSubmitAvailabilityEmpty(self):
        client = self.client

        inPerson = [[0, 0, 0, 0, 0, 0, 0] for _ in range(self.numRows)]
        virtual = [[0, 0, 0, 0, 0, 0, 0] for _ in range(self.numRows)]

        res = client.post('/submitAvailability', json={
            "inPersonMeetingTable": inPerson,
            "virtualMeetingTable": virtual,
            "meeting_id" : "8Uk4mL" ,
            "email": "jd@gmail.com"
            }) 
        
        # Check status code
        self.assertEqual(res.status_code, 200)
        
        # Query db
        actualMeeting = Meeting.query.filter_by(meetingID="8Uk4mL").first()
        actualUser = actualMeeting.getUser("jd@gmail.com")
        
        # Verify availability is set
        self.assertEqual(actualUser.getInPersonAvailability(), inPerson)
        self.assertEqual(actualUser.getVirtualAvailability(), virtual)


    def testSimpleSubmitAvailabilityCompleted(self):
        client = self.client

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
            "meeting_id" : "8Uk4mL" ,
            "email": "jd@gmail.com"
            }) 

        # Check status code
        self.assertEqual(res.status_code, 200)
        
        # Query db
        actualMeeting = Meeting.query.filter_by(meetingID="8Uk4mL").first()
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
                res = c.get('/meeting/' + '4K93mf')
                self.assertEqual(res.status_code, 200)

                template, context = templates[0]
                self.assertEqual(template.name, 'scheduling-landing.html')
                
                expectedMeeting = Meeting(meetingID="4K93mf", meetingName="MyMeeting", meetingType="in_person",
                meetingLength=15, dateType="general_week", startDate="", endDate="", dayStartTime=5, dayEndTime=21)

                self.assertEqual(context['data'], expectedMeeting.toJSON())


    def testGetMeetingDetailsNonExistant(self):
        c = self.client
        res = c.get('/meeting/' + "5K1093")
        self.assertEqual(res.status_code, 500)


    def testGetAvailabilityDetails(self):
        with flask_app.test_client() as c:
            with captured_templates(flask_app) as templates:

                res = c.get('/availability/' + 'Olpw0e' + '/' + 'jd@gmail.com')
                self.assertEqual(res.status_code, 200)

                template, context = templates[0]
                self.assertEqual(template.name, 'scheduling-availability.html')

                expectedUser = User(userName="John Doe", userEmail="jd@gmail.com", meetingID="Olpw0e")

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

                expectedUser.setAvailability(inPerson, virtual)
                self.assertEqual(context['data'], expectedUser.toJSON())

    # def testGetResultDetails(self):
    # 	with flask_app.test_client() as c:
    # 		with captured_templates(flask_app) as templates:
    # 			meeting = self.simpleMeeting
    # 			user = self.simpleUser1

    # 			inPerson = [[0, 0, 0, 0, 0, 0, 0] for _ in range(self.numRows)]
    # 			virtual = [[0, 0, 0, 0, 0, 0, 0] for _ in range(self.numRows)]

    # 			inPerson[3][4] = 1
    # 			inPerson[1][1] = 1
    # 			inPerson[30][6] = 0.75
    # 			inPerson[1][2] = 0.75

    # 			virtual[1][1] = 1
    # 			virtual[2][2] = 1
    # 			virtual[4][4] = 0.75
    # 			virtual[5][1] = 0.75

    # 			user.setAvailability(inPerson, virtual)
    # 			meeting_db[meeting.getMeetingID()] = meeting
    # 			meeting.addUser(user)
    # 			res = c.get('/results/' + meeting.getMeetingID())
    # 			self.assertEqual(res.status_code, 200)

    # 			template, context = templates[0]
    # 			self.assertEqual(template.name, 'results.html')

    # 			expectedMeetingInfo = meeting.toJSON()
    # 			combinedResultsInPerson = meeting.compiledAvailability(True)
    # 			expectedCompiledInPerson = json.dumps(combinedResultsInPerson.tolist())
    # 			expectedBestInPersonTimes = json.dumps(meeting.bestMeetingTimes(combinedResultsInPerson))
    # 			combinedResultsVirtual = meeting.compiledAvailability(False)
    # 			expectedCompiledVirtual = json.dumps(combinedResultsVirtual.tolist())
    # 			expectedBestVirtualTimes = json.dumps(meeting.bestMeetingTimes(combinedResultsVirtual))

    # 			expectedData = '{"meeting_info":' + expectedMeetingInfo + ',"compiled_inperson":' + expectedCompiledInPerson + ',"best_times_inperson":' \
    # 			+ expectedBestInPersonTimes + ',"compiled_virtual":' + expectedCompiledVirtual + \
    # 			',"best_times_virtual":' + expectedBestVirtualTimes + '}'

    # 			self.assertEqual(context['data'], expectedData)