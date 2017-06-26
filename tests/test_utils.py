import unittest

from apiaiassistant import utils


class TextToIntTestCase(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(utils.text_to_int("twenty-one"), 21)
        self.assertEqual(utils.text_to_int("14"), 14)
        self.assertEqual(utils.text_to_int("twenty-first"), 21)
        self.assertEqual(utils.text_to_int("forty two"), 42)
        self.assertEqual(utils.text_to_int("forty-two"), 42)
        self.assertEqual(utils.text_to_int("fifty five"), 55)
        self.assertEqual(utils.text_to_int("fifty fifth"), 55)
        self.assertEqual(utils.text_to_int("55th"), 55)
        self.assertEqual(utils.text_to_int("1.5"), 1.5)
        self.assertEqual(utils.text_to_int("one"), 1)
        self.assertEqual(utils.text_to_int("1"), 1)
        self.assertEqual(utils.text_to_int("1st"), 1)
        self.assertEqual(utils.text_to_int("2nd"), 2)
        self.assertEqual(utils.text_to_int("second"), 2)
        self.assertEqual(utils.text_to_int("first"), 1)
        self.assertEqual(utils.text_to_int("fifth"), 5)
        self.assertEqual(utils.text_to_int("twenty"), 20)


class ReadableListTestCase(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(
            utils.readable_list([1]), "1")
        self.assertEqual(
            utils.readable_list([1, 2]), "1 and 2")
        self.assertEqual(
            utils.readable_list([1, 2, 3]), "1, 2, and 3")
        self.assertEqual(
            utils.readable_list([1, 2, 3, 4]), "1, 2, 3, and 4")


if __name__ == '__main__':
    unittest.main()
