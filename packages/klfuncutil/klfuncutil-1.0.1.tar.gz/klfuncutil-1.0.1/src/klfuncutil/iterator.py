"""Iterator utilities
This is the help for ...
"""

from functools import wraps
from itertools import tee


def restartable_t(iter_returing_function):
    """Annoation to create re-startable iterators

    The annotation wraps a funktion that returns
    an iterator.
    The new function will return an object
    instead of an iterator. The object implemnts
    the "iterator" interfact in such a way the
    iterator can be execute multible times.

    This decorator is an alternative to using
    itertools.tee(). It consumes less memory,
    but we need to re-load the data each time the
    iterator is re-started - so it "lives" on
    runtime.

    Example:

    def get_some_iter1():
        return iter([1, 2, 3])

    i1 = get_some_iter1()
    assert list(i1) == [1, 2, 3]
    assert list(i1) == []

    @klfuncutil.iterator.restartable_t
    def get_some_iter2():
        return iter([4, 5, 6])

    i2 = get_some_iter2()
    assert list(i2) == [4, 5, 6]
    assert list(i2) == [4, 5, 6]

    Parameters:
    iter_returing_function : a function that returns an iterator

    Return:
    A new function that returns the iterator wrapped into a object
    """

    @wraps(iter_returing_function)
    def _wrapper(*args, **kwargs):
        """The function to wrapp the iterator generator

        Parameter:
        *args: positional arguments for the iter_returing_function()
        **kwargs: keyword argument for the iter_returing_function()
        return: an object of the (internal) class _Iter_Wrapper
        """

        class _Iter_Wrapper:
            def __init__(self, iter_fkt):
                self.iter_fkt = iter_fkt
                self.nxt_iter = None

            def __iter__(self):
                return self.iter_fkt(*args, **kwargs)

            def __next__(self):
                if self.nxt_iter == None:
                    self.nxt_iter = self.__iter__()
                try:
                    result = next(self.nxt_iter)
                    return result
                except StopIteration as ex:
                    self.nxt_iter = None
                    raise

        # the function will return an instance of our
        # internal class instead of the iterator that
        # the wrapped function would produce
        # If the client now uses the returned object in
        # a loop, the __iter__() function of the class
        # is called an returns the iterator.
        iter_obj = _Iter_Wrapper(iter_returing_function)
        return iter_obj

    # return the function that has been wrapped
    return _wrapper


def restartable_m(iter_returing_function):
    """Annoation to create re-startable iterators

    The annotation wraps a funktion that returns
    an iterator.
    The new function will return an object
    instead of an iterator. The object implemnts
    the "iterator" interface in such a way the
    iterator can be execute multible times.

    The decorator is using itertools.tee() - so
    it "lives" on memory consumtion.

    Example:

    def get_some_iter1():
        return iter([1, 2, 3])

    i1 = get_some_iter1()
    assert list(i1) == [1, 2, 3]
    assert list(i1) == []

    @klfuncutil.iterator.restartable_m
    def get_some_iter2():
        return iter([4, 5, 6])

    i2 = get_some_iter2()
    assert list(i2) == [4, 5, 6]
    assert list(i2) == [4, 5, 6]

    Parameters:
    iter_returing_function : a function that returns an iterator

    Return:
    A new function that returns the iterator wrapped into a object
    """

    @wraps(iter_returing_function)
    def _wrapper(*args, **kwargs):
        """The function to wrapp the iterator generator

        Parameter:
        *args: positional arguments for the iter_returing_function()
        **kwargs: keyword argument for the iter_returing_function()
        return: an object of the (internal) class _Iter_Wrapper
        """

        class _Iter_Wrapper:
            def __init__(self, iter_fkt):
                self.iter_fkt = iter_fkt
                self.source_iter = None

            def __iter__(self):
                """Requrst a new iterator."""
                if self.source_iter == None:
                    self.source_iter = self.iter_fkt(*args, **kwargs)
                # we duplicate the iterator an keep one copy
                self.source_iter, ret_val = tee(self.source_iter)
                return ret_val

        # the function will return an instance of our
        # internal class instead of the iterator that
        # the wrapped function would produce
        # If the client now uses the returned object in
        # a loop, the __iter__() function of the class
        # is called an returns the iterator.
        iter_obj = _Iter_Wrapper(iter_returing_function)
        return iter_obj

    # return the function that has been wrapped
    return _wrapper
