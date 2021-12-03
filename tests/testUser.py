from layover import db
import unittest
from layover.models import User
import json

class BaseCase(unittest.TestCase):
    
    def setUp(self):

        self.simpleUser = User(userName="John Doe", userEmail="jd@gmail.com", meetingID="K92fke")
        self.userWithAvail = User(
            userName="Jane Street", userEmail="js@gmail.com", meetingID="k28F34")

    def tearDown(self):
        pass
        # this statement will be executed after every test


class TestLayoverUser(BaseCase):

    def testSimpleGetID(self):
        self.assertEqual(self.simpleUser.getID(), "jd@gmail.com")

    def testSimpleGetInPerson(self):
        self.assertEqual(self.simpleUser.getInPersonAvailability(), None)

    def testSimpleGetVirtual(self):
        self.assertEqual(self.simpleUser.getVirtualAvailability(), None)

    def testSimpleToJson(self):

        actualDict = json.loads(self.simpleUser.toJSON())
        expectedJSON = {'email': 'jd@gmail.com',
                        'inPersonAvailability': None,
                        'meeting_id': 'K92fke',
                        'name': 'John Doe',
                        'virtualAvailability': None}
        self.assertDictEqual(actualDict, expectedJSON)

    def testToJsonWithAvail(self):
        inPersonAvail = [[1, 1, 1], [0, 1, 0]]
        virtualAvail = [[0, 0, 1], [0, 1, 1]]
        self.userWithAvail.setAvailability(inPersonAvail,virtualAvail)
        actualDict = json.loads(self.userWithAvail.toJSON())
        expectedJSON = {'email': 'js@gmail.com',
                        'inPersonAvailability': [[1, 1, 1], [0, 1, 0]],
                        'meeting_id': 'k28F34',
                        'name': 'Jane Street',
                        'virtualAvailability': [[0, 0, 1], [0, 1, 1]]}
        self.assertDictEqual(actualDict, expectedJSON)


    def testSetAndGetAvail(self):
        inPersonAvail = [[1, 1, 1], [0, 1, 0]]
        virtualAvail = [[0, 0, 1], [0, 1, 1]]
        self.userWithAvail.setAvailability(inPersonAvail,virtualAvail)
        self.assertListEqual(self.userWithAvail.getInPersonAvailability(), [
                             [1, 1, 1], [0, 1, 0]])
        self.assertListEqual(self.userWithAvail.getVirtualAvailability(), [
                             [0, 0, 1], [0, 1, 1]])

    def testSimpleGetName(self):
        self.assertEqual(self.simpleUser.getName(), "John Doe")

    def testSimpleGetMeetingID(self):
        self.assertEqual(self.simpleUser.getMeetingID(), "K92fke")

    def testUserNotEqual(self):
        self.assertNotEqual(self.simpleUser, self.userWithAvail)

    def testUserEqual(self):
        otherUser = User(userName="John Doe", userEmail="jd@gmail.com", meetingID="K92fke")
        self.assertEqual(self.simpleUser, otherUser)