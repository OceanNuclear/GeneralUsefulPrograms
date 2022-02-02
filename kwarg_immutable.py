import _ctypes

def di(obj_id):
    """ Inverse of id() function. """
    return _ctypes.PyObj_FromPtr(obj_id)

def mutab(arg, kw=[]):
    """The SAME list is reused .
    Even though the list stored by kw is only accessible in the function's scope,
    It is preserved forever, even when we exit the function's scope, and re-enters.
    This can be good or bad depending on whether you want a hidden variable to exist in the background."""
    kw += [arg,] # id(kw) is the SAME as before.
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