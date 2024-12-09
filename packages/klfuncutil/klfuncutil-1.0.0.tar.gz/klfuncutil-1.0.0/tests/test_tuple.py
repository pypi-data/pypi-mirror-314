import logging
from unittest import TestCase, main
from collections import namedtuple
from klfuncutil.collection import *


class MyTuple(tuple):
    def name():
        return "MyTuple"


class TestTuple(TestCase):
    def setUp(self):
        self.input = (1, 2, 3)
        self.input_copy = (1, 2, 3)
        self.input_id = id(self.input)
        self.result = None

    def tearDown(self):
        # check that source has not changed
        self.assertEqual(self.input, self.input_copy)
        # the type the result must be list
        self.assertTrue(issubclass(type(self.result), tuple))
        # make sure that input ist unchanged
        self.assertEqual(self.input_id, id(self.input))
        # make sure to result contains a different object
        self.assertNotEqual(self.input_id, id(self.result))

    def test_append_number(self):
        self.result = append_element(self.input, 4)
        self.assertEqual(self.result, (1, 2, 3, 4))

    def test_append_string(self):
        self.result = append_element(self.input, "Kalle")
        self.assertEqual(self.result, (1, 2, 3, "Kalle"))

    def test_append_tuple(self):
        self.result = append_collection(self.input, (9, 8, 8))
        self.assertEqual(self.result, (1, 2, 3, 9, 8, 8))

    def test_append_list(self):
        self.result = append_collection(self.input, [9, 8, 8])
        self.assertEqual(self.result, (1, 2, 3, 9, 8, 8))

    def test_append_iter(self):
        self.result = append_collection(self.input, range(10))
        self.assertEqual(self.result, (1, 2, 3, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9))

    def test_ownclass_append_element(self):
        myobject = MyTuple((1, 2, 3, 4))
        self.result = append_element(myobject, "Kalle")
        self.assertEqual(self.result, (1, 2, 3, 4, "Kalle"))
        self.assertEqual(type(self.result), MyTuple)

    def test_ownclass_append_tuple(self):
        myobject = MyTuple((1, 2, 3, 4))
        self.result = append_collection(myobject, ("Kalle", "Pelle"))
        self.assertEqual(self.result, (1, 2, 3, 4, "Kalle", "Pelle"))
        self.assertEqual(type(self.result), MyTuple)

    def test_ownclass_append_list(self):
        myobject = MyTuple((1, 2, 3, 4))
        self.result = append_collection(myobject, ["Kalle", "Pelle"])
        self.assertEqual(self.result, (1, 2, 3, 4, "Kalle", "Pelle"))
        self.assertEqual(type(self.result), MyTuple)

    def test_ownclass_append_iter(self):
        myobject = MyTuple((1, 2, 3, 4))
        self.result = append_collection(myobject, iter(["Kalle", "Pelle"]))
        self.assertEqual(self.result, (1, 2, 3, 4, "Kalle", "Pelle"))
        self.assertEqual(type(self.result), MyTuple)

    def test_remove_element(self):
        self.result = remove_element(self.input, 2)
        self.assertEqual(self.result, (1, 3))
        self.assertEqual(type(self.result), tuple)

    def test_ownlcass_remove_element(self):
        myobject = MyTuple((1, 2, 3, 4))
        self.result = remove_element(myobject, 3)
        self.assertEqual(self.result, (1, 2, 4))
        self.assertEqual(type(self.result), MyTuple)


if __name__ == "__main__":
    logging.basicConfig(filename="tests.log", level=logging.DEBUG)
    main()
