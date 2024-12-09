import logging
from unittest import TestCase, main
from klfuncutil.collection import *


class MyList(list):
    def name():
        return "MyList"


class DeepCopyTest(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_append_element_number(self):
        pass


if __name__ == "__main__":
    logging.basicConfig(filename="tests.log", level=logging.DEBUG)
    main()
