import os
os.environ['MY_ENV'] = "testSettings.py"
from flask import Flask
from layover import db
import unittest
# from unittest.case import expectedFailure
# from LayoverMeeting import LayoverMeeting
# from LayoverUser import LayoverUser
from layover.models import User, Meeting
import json
import numpy as np
from flask_sqlalchemy import SQLAlchemy
# from app.routes import sum
# import BaseCase
# from routes import sum
# from app import routes


class BaseCase(unittest.TestCase):

    # Tests don't run in sequential order. this means we have to account for tests overlapping
    # between testMeeting and testServer. Hence, we MUST drop db every single test and rebuild it

    # @classmethod
    # # Runs a single time before testing
    # def setUpClass(cls):
    #     db.create_all()
    #     BaseCase.populate_db()
    #     print("setup done")
    
    # @classmethod
    # def populate_db(self):
        
    #     self.simpleMeeting = Meeting(meetingID="4K93mf", meetingName="MyMeeting", meetingType="in_person",
    #     meetingLength=15, dateType="general_week", startDate="", endDate="", dayStartTime=5, dayEndTime=21)
    #     db.session.add(self.simpleMeeting)

    #     self.meetingWithUser = Meeting(meetingID="8Uk4mL", meetingName="Andrea's Meeting", meetingType="in_person",
    #     meetingLength=30, dateType="general_week", startDate="", endDate="", dayStartTime=5, dayEndTime=21)
    #     db.session.add(self.meetingWithUser)
        
    #     self.newUser = User(userName="John Doe", userEmail="jd@gmail.com", meetingID="8Uk4mL")
    #     self.newUser2 = User(userName="Jane Street", userEmail="js@gmail.com", meetingID="8Uk4mL")


    #     # self.meetingWithUser = LayoverMeeting(
    #     #     "", "", "", 30, "", "", "")
    #     # self.newUser = LayoverUser("John Doe", "jd@gmail.com", "K92fke")
    #     # self.newUser2 = LayoverUser("Jane Street", "js@gmail.com", "K92fke")
    #     # print(len(User.query.all()))
    #     self.meetingWithUser.addUser(self.newUser)
    #     self.meetingWithUser.addUser(self.newUser2)
    #     # print(len(User.query.all()))
    #     meetingHrLong = Meeting(meetingID="93k2lf", meetingName="Eric's Meeting", meetingType="in_person",
    #     meetingLength=60, dateType="general_week", startDate="", endDate="", dayStartTime=5, dayEndTime=21)
    #     db.session.add(meetingHrLong)
        
        
    #     db.session.commit()
    #     print(self.meetingWithUser.getUsers())
    #     print(self.meetingWithUser.getUser("jd@gmail.com"))
    #     print("COMPLETED SETUP")
    #     # pass
    
    @classmethod
    # Runs a single time before testing
    def tearDownClass(cls):
        db.drop_all()

    def setUp(self):
        db.create_all()

        self.simpleMeeting = Meeting(meetingID="4K93mf", meetingName="MyMeeting", meetingType="in_person",
        meetingLength=15, dateType="general_week", startDate="", endDate="", dayStartTime=5, dayEndTime=21)
        db.session.add(self.simpleMeeting)

        self.meetingWithUser = Meeting(meetingID="8Uk4mL", meetingName="Andrea's Meeting", meetingType="in_person",
        meetingLength=30, dateType="general_week", startDate="", endDate="", dayStartTime=5, dayEndTime=21)
        db.session.add(self.meetingWithUser)

        self.newUser = User(userName="John Doe", userEmail="jd@gmail.com", meetingID="8Uk4mL")
        self.newUser2 = User(userName="Jane Street", userEmail="js@gmail.com", meetingID="8Uk4mL")

        self.meetingWithUser.addUser(self.newUser)
        self.meetingWithUser.addUser(self.newUser2)
        meetingHrLong = Meeting(meetingID="93k2lf", meetingName="Eric's Meeting", meetingType="in_person",
        meetingLength=60, dateType="general_week", startDate="", endDate="", dayStartTime=5, dayEndTime=21)
        db.session.add(meetingHrLong)

        db.session.commit()

    def tearDown(self):
        db.drop_all()

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

    def testSimpleToJSON(self):
            meeting = self.simpleMeeting
            actualDict = json.loads(meeting.toJSON())
            expectedJSON = {
                "date_type": "general_week",
                "day_end_time": 21,
                "day_start_time": 5,
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
            expectedUser = User(userName="John Doe", userEmail="jd@gmail.com", meetingID="8Uk4mL")
            self.assertEqual(meeting.getUser("jd@gmail.com"), expectedUser)

    def testGetNonExistantUser(self):
        meeting = self.meetingWithUser
        self.assertEqual(meeting.getUser("ff@gmail.com"), None)

    def testAddMultipleUsers(self):
        
        meeting = self.meetingWithUser
        expectedUser = self.newUser
        self.assertEqual(meeting.getUser("jd@gmail.com"), expectedUser)
        expectedUser = self.newUser2
        self.assertEqual(meeting.getUser("js@gmail.com"), expectedUser)
        
    def testGetMultipleUsers(self):
        
        meeting = self.meetingWithUser
        self.assertListEqual([u.getID() for u in meeting.getUsers()], [
            "jd@gmail.com", "js@gmail.com"])

    def testCompiledAvailWithNoUsers(self):
        
        meeting = self.simpleMeeting
        self.assertTrue(np.array_equal(
            meeting.compiledAvailability(True), np.zeros((64, 7))))

    def testCompiledAvailNoUserInputAvail(self):
        meeting = self.meetingWithUser
        self.assertTrue(np.array_equal(
            meeting.compiledAvailability(True), np.zeros((64, 7))))

    def testCompiledAvailSingleUser(self):

        meeting = self.meetingWithUser
        avail = [[0, 0, 0, 0, 0, 0, 0] for i in range(64)]
        avail[0][0] = 1
        avail[1][0] = 1
        avail[2][0] = 1
        newUser = self.newUser
        newUser.setAvailability(avail, None)
        db.session.add(newUser)
        db.session.commit()

        actual = meeting.compiledAvailability(True)
        expected = np.zeros((64, 7))
        expected[0][0] = 1
        expected[1][0] = 1
        expected[2][0] = 1

        self.assertTrue(np.array_equal(actual, expected))

    def testCompiledAvailTwoUserFullOverlap(self):
        
        meeting = self.meetingWithUser
        avail = [[0, 0, 0, 0, 0, 0, 0] for i in range(64)]
        avail[0][0] = 1
        avail[1][0] = 1
        avail[2][0] = 1
        newUser = self.newUser
        newUser2 = self.newUser2
        newUser.setAvailability(avail, None)
        newUser2.setAvailability(avail, None)
        db.session.add(newUser)
        db.session.add(newUser2)
        db.session.commit()

        actual = meeting.compiledAvailability(True)
        expected = np.zeros((64, 7))
        expected[0][0] = 1
        expected[1][0] = 1
        expected[2][0] = 1

        self.assertTrue(np.array_equal(actual, expected))

    def testCompiledAvailTwoUserPartialOverlap(self):

        meeting = self.meetingWithUser
        avail1 = [[0, 0, 0, 0, 0, 0, 0] for i in range(64)]
        avail1[0][0] = 1
        avail1[1][0] = 1
        avail1[2][0] = 1

        avail2 = [[0, 0, 0, 0, 0, 0, 0] for i in range(64)]
        avail2[1][0] = 1
        avail2[2][0] = 1
        avail2[3][0] = 1
        newUser = self.newUser
        newUser2 = self.newUser2
        newUser.setAvailability(avail1, None)
        newUser2.setAvailability(avail2, None)
        db.session.add(newUser)
        db.session.add(newUser2)
        db.session.commit()

        actual = meeting.compiledAvailability(True)
        expected = np.zeros((64, 7))
        expected[0][0] = 0.5
        expected[1][0] = 1
        expected[2][0] = 1
        expected[3][0] = 0.5

        self.assertTrue(np.array_equal(actual, expected))


    def testCompiledAvailTwoUserNoOverlap(self):

        meeting = self.meetingWithUser
        avail1 = [[0, 0, 0, 0, 0, 0, 0] for i in range(64)]
        avail1[0][0] = 1
        avail1[1][0] = 1
        avail1[2][0] = 1

        avail2 = [[0, 0, 0, 0, 0, 0, 0] for i in range(64)]
        avail2[0][1] = 1
        avail2[1][1] = 1
        avail2[2][1] = 1
        newUser = self.newUser
        newUser2 = self.newUser2
        newUser.setAvailability(avail1, None)
        newUser2.setAvailability(avail2, None)
        db.session.add(newUser)
        db.session.add(newUser2)
        db.session.commit()

        actual = meeting.compiledAvailability(True)
        expected = np.zeros((64, 7))
        expected[0][0] = 1
        expected[1][0] = 1
        expected[2][0] = 1
        expected[0][1] = 1
        expected[1][1] = 1
        expected[2][1] = 1

        self.assertTrue(np.array_equal(actual, expected))


    def testCompiledAvailTwoUserPartialOverlapVirtual(self):
        meeting = self.meetingWithUser
        avail1 = [[0, 0, 0, 0, 0, 0, 0] for i in range(64)]
        avail1[0][0] = 1
        avail1[1][0] = 1
        avail1[2][0] = 1

        avail2 = [[0, 0, 0, 0, 0, 0, 0] for i in range(64)]
        avail2[1][0] = 1
        avail2[2][0] = 1
        avail2[3][0] = 1
        newUser = self.newUser
        newUser2 = self.newUser2
        newUser.setAvailability(avail1, None)
        newUser2.setAvailability(avail2, None)
        db.session.add(newUser)
        db.session.add(newUser2)
        db.session.commit()

        actual = meeting.compiledAvailability(True)
        expected = np.zeros((64, 7))
        expected[0][0] = 0.5
        expected[1][0] = 1
        expected[2][0] = 1
        expected[3][0] = 0.5

        self.assertTrue(np.array_equal(actual, expected))

    # def testBestTimesEmptyAvail(self):
    #     meeting = self.simpleMeeting
    #     actual = meeting.bestMeetingTimes(meeting.compiledAvailability(True))
    #     expected = ['Sunday 08:00', 'Sunday 07:45',
    #                 'Sunday 07:30', 'Sunday 07:15', 'Sunday 07:00']
    #     # Order is not relevant so use countEqual
    #     self.assertCountEqual(actual, expected)

    # def testBestTimesSingleUser(self):
    #     meeting = self.simpleMeeting
    #     avail = [[0, 0, 0, 0, 0, 0, 0] for i in range(64)]
    #     avail[0][0] = 1
    #     avail[1][0] = 1
    #     avail[2][0] = 1
    #     self.newUser.setAvailability(avail, None)
    #     meeting.addUser(self.newUser)
    #     print(meeting.getUsers())
    #     actual = meeting.bestMeetingTimes(meeting.compiledAvailability(True))
    #     expected = ['Sunday 08:00', 'Sunday 07:45',
    #                 'Sunday 07:30', 'Sunday 07:15', 'Sunday 07:00']
    #     # Order is not relevant so use countEqual
    #     self.assertCountEqual(actual, expected)

    # def testBestTimesTwoUserNoOverlap(self):
    #     meeting = self.simpleMeeting
    #     avail1 = [[0, 0, 0, 0, 0, 0, 0] for i in range(64)]
    #     avail1[0][0] = 1
    #     avail1[1][0] = 1
    #     avail1[2][0] = 1

    #     avail2 = [[0, 0, 0, 0, 0, 0, 0] for i in range(64)]
    #     avail2[1][1] = 1
    #     avail2[2][1] = 1
    #     avail2[3][1] = 1

    #     self.newUser.setAvailability(avail1, None)
    #     self.newUser2.setAvailability(avail2, None)

    #     meeting.addUser(self.newUser)
    #     meeting.addUser(self.newUser2)

    #     actual = meeting.bestMeetingTimes(meeting.compiledAvailability(True))
    #     expected = ['Monday 07:30', 'Monday 07:15',
    #                 'Sunday 07:30', 'Sunday 07:15', 'Sunday 07:00']
    #     # Order is not relevant so use countEqual
    #     self.assertCountEqual(actual, expected)

    # def testBestTimesTwoUserSingleOverlap(self):
    #     meeting = self.simpleMeeting
    #     avail1 = [[0, 0, 0, 0, 0, 0, 0] for i in range(64)]
    #     avail1[0][0] = 1
    #     avail1[1][0] = 1
    #     avail1[2][0] = 1
    #     avail1[5][6] = 1

    #     avail2 = [[0, 0, 0, 0, 0, 0, 0] for i in range(64)]
    #     avail2[1][1] = 1
    #     avail2[2][1] = 1
    #     avail2[3][1] = 1
    #     avail2[5][6] = 1

    #     self.newUser.setAvailability(avail1, None)
    #     self.newUser2.setAvailability(avail2, None)

    #     meeting.addUser(self.newUser)
    #     meeting.addUser(self.newUser2)

    #     actual = meeting.bestMeetingTimes(meeting.compiledAvailability(True))
    #     expected = ['Saturday 08:15', 'Monday 07:30',
    #                 'Monday 07:15', 'Sunday 07:30', 'Sunday 07:15']
    #     # Order is not relevant so use countEqual
    #     self.assertCountEqual(actual, expected)

    # def testBestTimesTwoUserMultipleOverlap(self):
    #     meeting = self.simpleMeeting
    #     avail1 = [[0, 0, 0, 0, 0, 0, 0] for i in range(64)]
    #     avail1[0][2] = 1
    #     avail1[1][2] = 1
    #     avail1[2][2] = 1
    #     avail1[3][2] = 1
    #     avail1[1][3] = 1
    #     avail1[2][3] = 1
    #     avail1[3][3] = 1
    #     avail1[4][3] = 1
    #     avail1[2][6] = 0.75
    #     avail1[3][6] = 0.75

    #     avail2 = [[0, 0, 0, 0, 0, 0, 0] for i in range(64)]
    #     avail2[2][0] = 1
    #     avail2[3][0] = 1
    #     avail2[0][2] = 1
    #     avail2[1][2] = 1
    #     avail2[3][3] = 0.75
    #     avail2[4][3] = 0.75
    #     avail2[2][6] = 1

    #     self.newUser.setAvailability(avail1, None)
    #     self.newUser2.setAvailability(avail2, None)

    #     meeting.addUser(self.newUser)
    #     meeting.addUser(self.newUser2)

    #     actual = meeting.bestMeetingTimes(meeting.compiledAvailability(True))
    #     expected = ['Tuesday 07:00', 'Tuesday 07:15',
    #                 'Wednesday 07:45', 'Wednesday 08:00', 'Saturday 07:30']
    #     # Order is not relevant so use countEqual
    #     self.assertCountEqual(actual, expected)

    # def testGoodTimesShorterThanMeetingInterval(self):
    #     # If user wants a 1hr meeting but only 15 or 30 minute slots open

    #     meeting = self.meetingHrLong
    #     avail1 = [[0, 0, 0, 0, 0, 0, 0] for i in range(64)]

    #     # Sun
    #     avail1[0][0] = 1
    #     avail1[1][0] = 0.75
    #     avail1[2][0] = 1
    #     avail1[3][0] = 0.75

    #     # Tue
    #     avail1[0][2] = 1
    #     avail1[1][2] = 1

    #     # Wed
    #     avail1[3][3] = 0.75
    #     avail1[4][3] = 0.75

    #     # Fri
    #     avail1[0][5] = 1
    #     avail1[1][5] = 1
    #     avail1[2][5] = 1
    #     avail1[3][5] = 1

    #     # Sat
    #     avail1[1][6] = 1
    #     avail1[3][6] = 0.75

    #     avail2 = [[0, 0, 0, 0, 0, 0, 0] for i in range(64)]
    #     # Sun
    #     avail2[0][0] = 1
    #     avail2[1][0] = 0.75
    #     avail2[2][0] = 1
    #     avail2[3][0] = 0.75

    #     # Tue
    #     avail2[0][2] = 1
    #     avail2[1][2] = 1

    #     # Wed
    #     avail2[3][3] = 0.75
    #     avail2[4][3] = 0.75

    #     # Fri
    #     avail2[0][5] = 1
    #     avail2[1][5] = 1
    #     avail2[2][5] = 1
    #     avail2[3][5] = 1
    #     avail2[4][5] = 0.75

    #     # Sat
    #     avail1[1][6] = 1
    #     avail1[3][6] = 1

    #     self.newUser.setAvailability(avail1, None)
    #     self.newUser2.setAvailability(avail2, None)

    #     meeting.addUser(self.newUser)
    #     meeting.addUser(self.newUser2)

    #     actual = meeting.bestMeetingTimes(meeting.compiledAvailability(True))
    #     expected = ['Friday 07:00', 'Sunday 07:00',
    #                 'Friday 07:15', 'Sunday 07:15', 'Friday 07:30']  # <- these are slightly suspect. 
    #                                                                  # for example friday 8am 1 user can't 
    #                                                                  # make it and the other is maybe
    #                                                                  # yet we recommend 7:15-8:15
    #     # Order is not relevant so use countEqual
    #     self.assertCountEqual(actual, expected)
