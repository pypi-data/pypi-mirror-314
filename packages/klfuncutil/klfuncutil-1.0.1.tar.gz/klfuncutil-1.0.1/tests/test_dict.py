import logging
from unittest import TestCase, main
from collections import OrderedDict
from klfuncutil.collection import *


class TestDict(TestCase):
    def setUp(self):
        self.input = {"a": 1, "b": 2, "c": 3}
        self.input_copy = {"a": 1, "b": 2, "c": 3}
        self.input_id = id(self.input)
        self.result = None

    def tearDown(self):
        # check that source has not changed
        self.assertEqual(self.input, self.input_copy)
        # the type the result must be list
        self.assertTrue(issubclass(type(self.result), dict))
        # make sure that input ist unchanged
        self.assertEqual(self.input_id, id(self.input))
        # make sure to result contains a different object
        self.assertNotEqual(self.input_id, id(self.result))

    def test_append_number_tuple(self):
        self.result = append_element(self.input, ("x", 9))
        self.assertEqual(self.result, {"a": 1, "b": 2, "c": 3, "x": 9})

    def test_append_number_list(self):
        self.result = append_element(self.input, ["x", 9])
        self.assertEqual(self.result, {"a": 1, "b": 2, "c": 3, "x": 9})

    def test_append_number_iter(self):
        self.result = append_element(self.input, iter(["x", 9]))
        self.assertEqual(self.result, {"a": 1, "b": 2, "c": 3, "x": 9})

    def test_ordered_dict(self):
        d1 = OrderedDict(self.input)
        self.result = append_element(d1, ["x", 9])
        self.assertEqual(type(self.result), OrderedDict)

    def test_append_dict(self):
        self.result = append_collection(self.input, {"x": 9, 1: "a"})
        self.assertEqual(self.result, {"a": 1, "b": 2, "c": 3, "x": 9, 1: "a"})

    def test_append_list(self):
        self.result = append_collection(self.input, [("x", 9), (1, "a")])
        self.assertEqual(self.result, {"a": 1, "b": 2, "c": 3, "x": 9, 1: "a"})

    def test_append_tuple(self):
        self.result = append_collection(self.input, (["x", 9], (1, "a")))

    def test_append_iter(self):
        self.result = append_collection(self.input, iter({"x": 9, 1: "a"}.items()))
        self.assertEqual(self.result, {"a": 1, "b": 2, "c": 3, "x": 9, 1: "a"})


if __name__ == "__main__":
    logging.basicConfig(filename="tests.log", level=logging.DEBUG)
    main()
