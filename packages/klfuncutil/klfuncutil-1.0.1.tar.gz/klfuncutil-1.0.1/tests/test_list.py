import logging
from unittest import TestCase, main
import sys

print(sys.path)
from klfuncutil.collection import *


class MyList(list):
    def name():
        return "MyList"


class ListTest(TestCase):
    def setUp(self):
        self.input = [1, 2, 3]
        self.input_copy = [1, 2, 3]
        self.input_id = id(self.input)
        self.result = None

    def tearDown(self):
        # check that source has not changed
        self.assertEqual(self.input, self.input_copy)
        # the type the result must be list
        self.assertTrue(issubclass(type(self.result), list))
        # make sure that input ist unchanged
        self.assertEqual(self.input_id, id(self.input))
        # make sure to result contains a different object
        self.assertNotEqual(self.input_id, id(self.result))

    def test_append_element_number(self):
        self.result = append_element(self.input, 4)
        self.assertEqual(self.result, [1, 2, 3, 4])

    def test_append_element_string(self):
        self.result = append_element(self.input, "Kalle")
        self.assertEqual(self.result, [1, 2, 3, "Kalle"])

    def test_append_element_tuple(self):
        self.result = append_element(self.input, (9, 8, 8))
        self.assertEqual(self.result, [1, 2, 3, (9, 8, 8)])

    def test_append_element_list(self):
        self.result = append_element(self.input, [9, 8, 8])
        self.assertEqual(self.result, [1, 2, 3, [9, 8, 8]])

    def test_append_collection_list(self):
        self.result = append_collection(self.input, [9, 8, 8])
        self.assertEqual(self.result, [1, 2, 3, 9, 8, 8])

    def test_append_collection_tuple(self):
        self.result = append_collection(self.input, (9, 8, 8))
        self.assertEqual(self.result, [1, 2, 3, 9, 8, 8])

    def test_append_collection_iter(self):
        i = filter(lambda x: x > 3, range(10))
        self.result = append_collection(self.input, i)
        self.assertEqual(self.result, [1, 2, 3, 4, 5, 6, 7, 8, 9])

    def test_own_list_class_element(self):
        mylist = MyList([1, 2, 3])
        self.result = append_element(mylist, "a")
        self.assertEqual(self.result, [1, 2, 3, "a"])
        self.assertTrue(type(self.result) == MyList)

    def test_own_list_class_list(self):
        mylist = MyList([1, 2, 3])
        self.result = append_collection(mylist, ["a", "b", "c"])
        self.assertEqual(self.result, [1, 2, 3, "a", "b", "c"])
        self.assertTrue(type(self.result) == MyList)

    def test_own_list_class_tuple(self):
        mylist = MyList([1, 2, 3])
        self.result = append_collection(mylist, ("a", "b", "c"))
        self.assertEqual(self.result, [1, 2, 3, "a", "b", "c"])
        self.assertTrue(type(self.result) == MyList)

    def test_own_list_class_iter(self):
        mylist = MyList([1, 2, 3])
        self.result = append_collection(mylist, iter(("a", "b", "c")))
        self.assertEqual(self.result, [1, 2, 3, "a", "b", "c"])
        self.assertTrue(type(self.result) == MyList)

    def test_remove_element(self):
        self.result = remove_element(self.input, 2)
        self.assertEqual(self.result, [1, 3])

    def test_remove_string_element(self):
        l = ["Kalle", "Pelle", "Olle"]
        self.result = remove_element(l, "Pelle")
        self.assertEqual(self.result, ["Kalle", "Olle"])

    def test_own_list_class_remove(self):
        mylist = MyList([1, 2, 3])
        self.result = remove_element(mylist, 2)
        self.assertEqual(self.result, [1, 3])
        self.assertTrue(type(self.result) == MyList)


if __name__ == "__main__":
    logging.basicConfig(filename="tests.log", level=logging.DEBUG)
    main()
