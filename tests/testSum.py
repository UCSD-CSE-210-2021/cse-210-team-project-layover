import unittest
from server import sum

# from app.routes import sum
# import BaseCase
# from routes import sum
# from app import routes


class BaseCase(unittest.TestCase):
    def setUp(self):
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


class TestSum(BaseCase):
    # class SumTest(unittest.TestCase):
    # class BaseCase(unittest.TestCase):

    # pass

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
