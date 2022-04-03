import _ctypes

def di(obj_id):
    """ Inverse of id() function. """
    return _ctypes.PyObj_FromPtr(obj_id)

def mutab(arg, kw=[]):
    """The SAME list is reused .
    Even though the list stored by kw is only accessible in the function's scope,
    It is preserved forever, even when we exit the function's scope, and re-enters.
    This can be good or bad depending on whether you want a hidden variable to exist in the background.
    The reason why kw is persistent is because it's never garbage-collected:
        the number of reference to it (from the __main__ scope) is at least 1 at all times,
        since this [] is stored in mutab.__defaults__ as the first default argument.
        If we append to it that very [] is appended and grows to a bigger list.
    """
    print(id(kw))
    kw += [arg,] # id(kw) is the SAME as before.
    print(id(kw))
    # Probably BAD! recursive call of kw will make the arg grow longer.
    return kw

def immut(arg, kw=(1,)):
    """An immutable tuple is used, so even if you try to change it nothing happens."""
    # On the each function call we try to get the same old id(kw).
    # You can show this by printing the id
    print(id(kw)) # it will be the same every time.
    kw += (arg,) # id(kw) isn't the same anymore.
    # `The original kw has been de-referenced.` # <- Need to confirm this!
    return kw
# TODO/Question: in C the pointer points to the start of an array. Is it the same in python?

# AnsweredQuestion: At the bit level, how does the format of a pointer differ from the format of an int?
# Answer: No.
#   And If there's a segfault, then this is because the OS itself kept track and knew that you're now trying to access memory out of bounds.

# print(id('15'))
# print(id('15'))
# print('15' is '15')
"""OH!
ipython does the funny thing of dereferencing all char arrays (i.e. strings longer than 1 character) between successive calls to the 
"""
def append_item_no_mut(a_list, item):
    print(id(a_list))
    a_list = a_list + [item]
    print(id(a_list))
    # This only creates a NEW a_list inside the function's scope. This new id is hidden from the outside.
    return a_list

"""LOOK here:
https://docs.python.org/3/reference/datamodel.html?highlight=iadd#object.__eq__
By default object implements __eq__() by using is
So a plain object assigned to a (a = Dummy(), b = a) has it's equality to another object implemented using is.
"""
"""
https://stackoverflow.com/questions/9766387/different-behaviour-for-list-iadd-and-list-add
+= is different from x = x + []
"""
# __qualname__ can also be called from inside a class, without it having to be bound to any methods
class Dummy():
    print(__qualname__)
    def newfunc(self):
        print(self.__name__)
d = Dummy()
d.newfunc()