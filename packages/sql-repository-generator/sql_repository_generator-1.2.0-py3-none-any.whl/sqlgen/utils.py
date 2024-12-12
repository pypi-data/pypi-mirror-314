from typing import Callable, Iterable, Sequence, assert_never


def take[T](__function: Callable[[T], bool], __iterable: Iterable[T]) -> T:
    """
    take the object matching __function from __iterable
    :param __function: the function to use when searching the object. it should return true
        if the object passed as arguments is the one searched for
    :param __iterable: the iterable to search into
    :raise KeyError: either no object were found or too many
    :return: the found object
    """
    if results := list(filter(__function, __iterable)):
        if len(results) > 1:
            raise KeyError(f"multiple {results=} for {__function=}, {__iterable=}")
        return results[0]
    raise KeyError(f"No match for {__function=} in {__iterable=}")


def index[T](__function: Callable[[T], bool], __sequence: Sequence[T]) -> int:
    """
    Custom index function that takes a filtering function and a sequence
    the Sequence must stay the same after multiple iteration or an exception will be raised
    This function replace [].index() for SQLAlchemy table that implement custom equality behaviour
    [x].index(val) use x == val. but SQLAlchmey will try to generate a DDL stuff we don't want that,
    we want to compare identity instead. hence the for loop with the "is" in the place of an "==" as we are comparing
    the same object

    :param __function: a function to find the object to get the index
    :param __sequence: the sequence to search the item into
    :return: the index of the object in the sequence
    """
    index_val = take(__function, __sequence)
    for i, item in enumerate(__sequence):
        if item is index_val:
            return i
    assert_never((__function, __sequence, index_val))
