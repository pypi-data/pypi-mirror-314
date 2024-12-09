from functools import reduce
from itertools import chain
import pickle


def _append_element_to_list(c_list, element):
    """Append a element to list

    if "element" is a list, concat the two list
    if "element" is an iterator, we append all elements from the iterator.
    any other elements we append to a copy of the list
    """
    result = type(c_list)(c_list)
    result.append(element)
    return result


def _append_collection_to_list(c_list, collection):
    """Append a collection to list"""
    if issubclass(type(collection), list):
        return type(c_list)(c_list + collection)
    return type(c_list)(c_list + list(collection))


def _append_element_to_dict(c_dict, element):
    """Create a new dict and append an element to it

    We assume, that the "element" can be accessed
    via iterator.
    """
    result_dict = type(c_dict)(c_dict)
    element_iter = iter(element)
    key = next(element_iter)
    value = next(element_iter)
    result_dict[key] = value
    return result_dict


def _append_collection_to_dict(c_dict, collection):
    """Create a new dict and add all elements from the "collection" """

    def add_item(dest_dict, element):
        element_iter = iter(element)
        key = next(element_iter)
        value = next(element_iter)
        dest_dict[key] = value
        return dest_dict

    # make a shallow copy
    result_dict = type(c_dict)(c_dict)

    # check type of "collection". If this is a "dict"
    # we loop all its items into the "result_dict"
    if issubclass(type(collection), dict):
        return _append_collection_to_dict(c_dict, collection.items())
    else:
        # we assume that the "collection" contains
        # tuples or lists
        return reduce(add_item, iter(collection), result_dict)


def _append_element_to_iter(source_iter, element):
    """Append one element to the source iterator
    and return a new iterator
    """
    return chain(source_iter, iter([element]))


def _append_collection_to_iter(source_iter, collection):
    """Append one element to the source iterator
    and return a new iterator
    """
    return chain(source_iter, iter(collection))


def _remove_element_from_list(source_list, element):
    # make copy of list
    result = type(source_list)(source_list)
    # remove element
    result.remove(element)
    # return the copy
    return result


def _remove_element_from_tuple(source_tuple, element):
    # create list from the tuple
    elements = list(source_tuple)
    # remove the element from the list
    elements.remove(element)
    # create the result from the list
    result = type(source_tuple)(elements)
    # return the copy
    return result


def _remove_element_from_dict(source_dict, element):
    result = type(source_dict)(source_dict)
    result.pop(element)
    return result


def _remove_element_from_iter(source_iter, element):
    """
    We can not remove an element from the iterator,
    but we can 'filter' it from the result
    """
    return filter(lambda x: x != element, source_iter)


# =========================================================================


def append_element(c, element):
    """General function to append a new element to a collection

    c - any collection
    element - new element

    If "c" is list, we return a new list object
    If "c" is a tuple, we return a new tuble
    If "c" is an iterator, we return a new iterator
    """
    if issubclass(type(c), list):
        return _append_element_to_list(c, element)
    if issubclass(type(c), tuple):
        return type(c)(c + (element,))
    if issubclass(type(c), dict):
        return _append_element_to_dict(c, element)
    if callable(getattr(c, "__next__")):
        return _append_element_to_iter(c, element)


def append_collection(c, collection):
    """General function to append a new element to a collection

    c - any collection
    collection - a collection with new elements that want to append

    If "c" is list, we return a new list object
    If "c" is a tuple, we return a new tuble
    If "c" is a dict, we return a new dict
    If "c" is an iterator, we return a new iterator
    """

    if issubclass(type(c), list):
        return _append_collection_to_list(c, collection)
    if issubclass(type(c), tuple):
        return type(c)(c + tuple(collection))
    if issubclass(type(c), dict):
        return _append_collection_to_dict(c, collection)
    if callable(getattr(c, "__next__")):
        return _append_collection_to_iter(c, collection)


def remove_element(c, element):
    """General function to remove a element from the collection

    c - any collection
    element - element to be removed

    If "c" is list, we return a new list object
    If "c" is a tuple, we return a new tuble
    If "c" is a dict, we return a new dict
    If "c" is an iterator, we return a new iterator
    """
    if issubclass(type(c), list):
        return _remove_element_from_list(c, element)
    if issubclass(type(c), tuple):
        return _remove_element_from_tuple(c, element)
    if issubclass(type(c), dict):
        return _remove_element_from_dict(c, element)
    if callable(getattr(c, "__next__")):
        return _remove_element_from_iter(c, element)


def deep_copy(c):
    """Create a deep-copy of the collection

    c - any collection

    """
    pickled_obj = pickle.dumps(c)
    return pickle.loads(pickled_obj)
