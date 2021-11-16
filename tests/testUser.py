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
        self.abc = 9
        pass
        # this statement will be executed before testing
        # self.app = app.test_client()
        # self.db = db.get_db() # get db by example

    def tearDown(self):
        pass
        # this statement will be executed after testing
        # Delete Database collections after the test is complete
        # for collection in self.db.list_collection_names()
        # self.db.drop_collection(collection)


class TestUser(BaseCase):
    # class SumTest(unittest.TestCase):
    # class BaseCase(unittest.TestCase):

    # pass
    def testCheckPass(self):
        self.assertEqual(self.abc, 9)

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

    def test_list_int(self):
        data = [1, 2, 3, 4, 5]
        result = sum(data)
        self.assertEqual(result, 15)

    def test_lisf_float(self):
        data = [1.2, 2.4, 2.7, 0.5, 1.8]
        result = sum(data)
        self.assertEqual(result, 8.6)

    def test_list_with_negative_value(self):
        data = [1, 2, 3, 4, -5]
        result = sum(data)
        self.assertEqual(result, 5)

    def test_with_tupple(self):
        data = (1, 2, 3, 4, 5)
        result = sum(data)
        self.assertEqual(result, 15)

    def test_fail_with_string(self):
        data = [1, 2, '3', '4', '5']
        result = sum(data)
        self.assertEqual(result[0], "Error occured!")
        self.assertEqual(result[1], 500)

    def test_fail_with_single_value(self):
        data = 1
        result = sum(data)
        self.assertEqual(result[0], "Error occured!")
        self.assertEqual(result[1], 500)
