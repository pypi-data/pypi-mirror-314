import logging
from unittest import TestCase, main
import itertools
import sys
from klfuncutil.iterator import *


class TestRepeatIter(TestCase):
    def setUp(self):
        self.name_list = ["Kalle", "Pelle", "Olle", "Nisse"]

    def tearDown(self):
        pass

    def test_iter(self):
        name_iter = iter(self.name_list)
        name_list_1 = list(name_iter)
        self.assertEqual(len(name_list_1), 4)
        name_list_2 = list(name_iter)
        self.assertEqual(len(name_list_2), 0)

    def test_iter_class(self):
        class IterClass1:
            def __init__(self, data):
                self.data = data

            def __iter__(self):
                return iter(self.data)

        # test it
        IterObj = IterClass1(self.name_list)

        name_list_1 = list(IterObj)
        name_list_2 = list(IterObj)
        self.assertEqual(len(name_list_1), 4)
        self.assertEqual(len(name_list_2), 4)

    def test_iter_fkt(self):
        # a function that returns an iterator
        def iter_fkt(data):
            return iter(data)

        # a class that takes a function as parameter
        class IterClass2:
            def __init__(self, fkt, data):
                self.fkt = fkt
                self.data = data

            def __iter__(self):
                return self.fkt(self.data)

        # test it
        IterObj = IterClass2(iter_fkt, self.name_list)
        name_list_1 = list(IterObj)
        name_list_2 = list(IterObj)
        self.assertEqual(len(name_list_1), 4)
        self.assertEqual(len(name_list_2), 4)

    def test_decorator(self):
        @restartable_t
        def iter_fkt(data):
            return iter(data)

        it = iter_fkt(data=self.name_list)

        name_list_1 = list(it)
        name_list_2 = list(it)
        self.assertEqual(len(name_list_1), 4)
        self.assertEqual(len(name_list_2), 4)

    def test_decorator_filter(self):

        @restartable_t
        def iter_fkt(data):
            """Liefert den Iterator

            Hier wird ein Iterator ausgegeben der
            aus der Collection alle Werte in "lower case"
            liefert die mit einem "k" beginnen.

            Parameter:
            data : eine Collection aus der ein Iterator erzeugt werden kall

            Return: ein Iterator ueber die Collection

            """
            it = iter(data)
            filter_iter = filter(
                lambda name: name[0] == "k", map(lambda name: name.lower(), it)
            )
            return filter_iter

        ###print(help(iter_fkt))

        it = iter_fkt(data=self.name_list)

        name_list_1 = list(it)
        name_list_2 = list(it)
        self.assertEqual(len(name_list_1), 1)
        self.assertEqual(len(name_list_2), 1)

    def test_example(self):
        def get_some_iter1():
            return iter([1, 2, 3])

        i1 = get_some_iter1()
        assert list(i1) == [1, 2, 3]
        assert list(i1) == []

        @restartable_t
        def get_some_iter2():
            return iter([1, 2, 3])

        i2 = get_some_iter2()
        assert list(i2) == [1, 2, 3]
        assert list(i2) == [1, 2, 3]

    def test_sum_list(self):
        @restartable_t
        def sum_list(number_list):
            """An iterator
            return number_list[0] -> number_list[0]+number_list[1] -> ...
            """
            lastnumber = 0
            for current_number in number_list:
                lastnumber = lastnumber + current_number
                yield lastnumber

        sum_iter = sum_list([1, 2, 3, 4])
        l1 = list(sum_iter)
        l2 = list(sum_iter)
        self.assertEqual(l1, l2)

    def test_fitler_iter(self):
        @restartable_t
        def filter_a(some_test):
            return filter(lambda some_char: some_char.upper() != "A", some_test)

        name_iter = filter_a("Kalle Anderson")
        n1 = "".join(name_iter)
        n2 = "".join(name_iter)
        self.assertEqual(n1, n2)


if __name__ == "__main__":
    logging.basicConfig(filename="tests.log", level=logging.DEBUG)
    main()
