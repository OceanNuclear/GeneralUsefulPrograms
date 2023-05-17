#!/home/ocean/anaconda3/bin/python3
from numpy import cos, arccos, sin, arctan, tan, pi, sqrt; from numpy import array as ary; import numpy as np; tau = 2*pi
from matplotlib import pyplot as plt

def wrapper(a1):
    def dummyfunc(x):
        return a1*x
    return dummyfunc
#Is equivalent to:
def wrapper(a1):
    return lambda x: x*a1

def wrapper(a1,a2,*args): #Collect all extra arguments, packaged into a tuple.
    #Because python assume that when the user calls wrapper, they parse in several elements via unpacking,
    #So they must've unpacked a list.
    #Python recontructs args by packing them back into a tuple.
    print(args) #gets a the original (args,), nested inside a tuple.
    def true_func(*args):
        #define a function using the local variable that 
        return a1*args[0]
    print('decorator has been applied on', true_func)
    return true_func #return an OBJECT (like a pointer, but existing globally) with the a1 and a2 values already properly initialized and stored inside the function.


def decorator(func_you_want_decorated):
    #1. Can initialize variable outside to be used inside:
    var_out="This variable is initialized outside"
    def func_after_decoration(arg_you_wouldve_parsed_to_func):
        print(var_out)
        
        #1. can operate on the argument to be parsed:
        new_arg_to_parse_to_func = arg_you_wouldve_parsed_to_func+1
        
        #2. can perform operation on func itself before actually calling the argument
        OBJECT = func_you_want_decorated
        print('INSIDE: decorator has been applied onto', OBJECT.__name__)
        
        #3. Can operate on the output
        output_from_orig_func = func_you_want_decorated(new_arg_to_parse_to_func) #Need to actually execute the method
        #But you cannot touch what's actually INSIDE the method
        new_output = output_from_orig_func+","
        
        #func_after_decoration's return will replace the func_you_want_decorated's return
        return new_output+" and some text added at the new 'return' line"

    print('OUTSIDE: after decorator has been applied onto', func_after_decoration.__name__)
    
    #usually we make it return the new func_after_decoration function object
    return func_after_decoration
########################
#    The following     #
########################
def func_aliased_away(args):
    print(args)
    return str(args)+"original text"
var_out="This variable is initialized outside"
def wrapped_func(args):
    print(var_out)
    new_args = args +1
    
    print('INSIDE: decorator has (not) been applied onto', wrapped_func.__name__)

    output_from_orig_func = func_aliased_away(new_args)
    new_output = output_from_orig_func+","
    
    return new_output+" and some text added at the new 'return' line "
print('OUTSIDE: before decorator has been applied onto', func_aliased_away.__name__)
########################
# can be simplified as #
########################
#
@decorator
def wrapped_func(args):
    print(args)
    return str(args)+"original text"
#
# So using the @ unary operator,
# we begin the scope of the 'decorator' function as if we've called it with 
# wrapped_func = decorator(wrapped_func)