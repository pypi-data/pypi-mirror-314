import logging
from unittest import TestCase, main
import itertools
from klfuncutil.collection import *
from klfuncutil.iterator import *
import csv


class TestIter(TestCase):
    def setUp(self):
        self.input, self.input_copy = itertools.tee(iter((1, 2, 3)), 2)
        self.result = None
        self.append_element = None
        self.append_collection = None
        self.input_id = id(self.input)

    def tearDown(self):
        if self.result == None:
            return
        # make sure the the input-iter contains the same elements as the result
        for x in self.input_copy:
            y = next(self.result)
            self.assertEqual(x, y)

        if self.append_element is not None:
            # make sure that the appended element is last in the iterator
            z = next(self.result)
            self.assertTrue(z == self.append_element)

        if self.append_collection is not None:
            for x in self.append_collection:
                y = next(self.result)
                self.assertEqual(x, y)

        # make sure that input ist unchanged
        self.assertEqual(self.input_id, id(self.input))
        # make sure to result contains a different object
        self.assertNotEqual(self.input_id, id(self.result))

    def test_append_number(self):
        self.result = append_element(self.input, 4)
        self.append_element = 4

    def test_append_string(self):
        self.result = append_element(self.input, "Kalle")
        self.append_element = "Kalle"

    def test_append_num_list(self):
        self.result = append_collection(self.input, [100, 200, 300])
        self.append_collection = [100, 200, 300]

    def test_append_str_list(self):
        self.result = append_collection(self.input, "Kalle")
        self.append_collection = ["K", "a", "l", "l", "e"]

    def test_append_num_iter(self):
        self.result = append_collection(
            self.input, filter(lambda x: x != 400, [100, 200, 300, 400])
        )
        self.append_collection = [100, 200, 300]

    def test_remove_element(self):
        self.result = append_element(self.input, 4)
        self.append_element = 4
        i1 = iter([1, 2, 3])
        i2 = remove_element(i1, 2)
        l2 = list(i2)
        self.assertEqual(l2, [1, 3])

    def test_iter_next_none_restartable(self):
        def get_iter(r):
            for x in r:
                yield x

        i0 = get_iter(
            [
                1,
                2,
            ]
        )
        next(i0)
        next(i0)
        try:
            next(i0)
            self.assertTrue(False)
        except StopIteration as ex:
            pass

        try:
            d = next(i0)
            self.assertTrue(False)
        except StopIteration as ex:
            pass

    def test_iter_next_restartable(self):
        @restartable_t
        def get_iter(r):
            for x in r:
                yield x

        i0 = get_iter(
            [
                1,
                2,
            ]
        )
        next(i0)
        next(i0)
        try:
            next(i0)
            self.assertTrue(False)
        except StopIteration as ex:
            pass

        try:
            d = next(i0)
            self.assertEqual(d, 1)
        except StopIteration as ex:
            self.assertTrue(False)

    def test_csv_iter(self):

        @restartable_t
        def get_reader(csv_file):
            csv_file.seek(0)
            reader = csv.reader(csv_file, delimiter=";")
            return reader

        with open("./tests/test_iter.csv", newline="") as csv_file:
            reader = get_reader(csv_file)
            l1 = list(reader)
            l2 = list(reader)
        self.assertEqual(len(l1), 5)
        self.assertEqual(len(l2), 5)

    def test_filter(self):
        @restartable_t
        def get_reader(csv_file):
            csv_file.seek(0)
            reader = csv.reader(csv_file, delimiter=";")
            return reader

        @restartable_t
        def filter_firstname(string_in_firstname, csv_iter):
            return filter(lambda line: line[1].find(string_in_firstname) >= 0, csv_iter)

        with open("./tests/test_iter.csv", newline="") as csv_file:
            reader = get_reader(csv_file)
            filter_by_l_iter = filter_firstname("l", reader)
            l1 = list(filter_by_l_iter)
            self.assertEqual(len(l1), 3)

            # the iterator "filter_iter" has been used by the list()
            # function, but we can re-start it...
            filter_by_K_and_l = filter_firstname("K", filter_by_l_iter)
            l2 = list(filter_by_K_and_l)
            self.assertEqual(len(l2), 1)

    def test_repeatable_m(self):

        @restartable_m
        def get_list_iter():
            print("iter created")
            for x in range(0, 10):
                yield x

        i1 = get_list_iter()
        for x in i1:
            print(x)
        for x in i1:
            print(x)

        pass


if __name__ == "__main__":
    logging.basicConfig(filename="tests.log", level=logging.DEBUG)
    main()
