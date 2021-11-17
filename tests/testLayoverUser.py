import unittest
from server import sum
from LayoverUser import LayoverUser
import json
# from app.routes import sum
# import BaseCase
# from routes import sum
# from app import routes


class BaseCase(unittest.TestCase):
    def setUp(self):
        self.simpleUser = LayoverUser("John Doe", "jd@gmail.com", "K92fke")
        self.userWithAvail = LayoverUser(
            "Jane Street", "js@gmail.com", "k28F34")
        # this statement will be executed before testing

    def tearDown(self):
        pass
        # this statement will be executed after testing


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

    def testSetAndGetInPerson(self):
        self.userWithAvail.setAvailability(
            [[1, 1, 1], [0, 1, 0]], [[0, 0, 1], [0, 1, 1]])

        self.assertListEqual(self.userWithAvail.getInPersonAvailability(), [
                             [1, 1, 1], [0, 1, 0]])
        self.assertListEqual(self.userWithAvail.getVirtualAvailability(), [
                             [0, 0, 1], [0, 1, 1]])

    def testSimpleGetName(self):
        self.assertEqual(self.simpleUser.getName(), "John Doe")

    def testSimpleGetMeetingID(self):
        self.assertEqual(self.simpleUser.getMeetingID(), "K92fke")
