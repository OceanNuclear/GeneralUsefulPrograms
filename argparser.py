import argparse
parg = argparse.ArgumentParser(description="""An example code to show how argparse works
(it violates many programming paradigm
but is done exactly right for parsing command line arguments, I guess.)""",
    usage="""A usage statement about typical cases:
python __main__.py # append any of the flag you find in help.'""",)

"""https://docs.python.org/3/library/argparse.html#the-add-argument-method
All kwargs of add_argument of are:
name or flags - Either a name or a list of option strings, e.g. foo or -f, --foo.
action  - The basic type of action to be taken when this argument is encountered at the command line.
    # allowed options are ('store_const', 'append_const', 'store_true', 'store_false', 'count', 'extend')
nargs   - The number of command-line arguments that should be consumed.
const   - A constant value required by some action and nargs selections.
default - The value produced if the argument is absent from the command line and if it is absent from the namespace object.
type    - The type to which the command-line argument should be converted.
choices - A container of the allowable values for the argument.
required- Whether or not the command-line option may be omitted (optionals only).
help    - A brief description of what the argument does.
metavar - A name for the argument in usage messages.
dest    - The name of the attribute to be added to the object returned by parse_args().
    # this is automatically inferred from the long flag (and if it's hyphenated, .replace('-','_'))

action=
default=None,
type=None,
choices=None,
help='help',
"""
# '=' are automatically intepreted as spaces.

# case 1: a boolean option with both a long form and a short form.
parg.add_argument("-p", "--print_this", help="Print this particular statement", action="store_true") 
    # can only be accessed by parg.parse_args().print_this, not parg.parse_args().p

# case 2: a boolean option with only a short form
parg.add_argument("-S", help="a boolean flag with no short form", action="store_true")
    # can be accessed by parg.parse_args().S

# case 3: a flag with only a short form, taking in a str argument.
parg.add_argument("-A", help="Enter ONE test argument.",)
    # python __main__.py -A 1 -A 2 # would give cl_arg.parse_args().A==2,
    # because the first A's value gets overwritten because extend isn't used.

# case 4: a flag with mult
parg.add_argument("-v", "--verbosity-increase", dest="verbosity", help="Increase the output verbosity", action="count", default=0)
    # python __main__.py -vv
    # python __main__.py -v -v
    # python __main__.py -v --verbosity # order doesn't matter
    # all gives cl_arg.verbosity = 2

# case 5: taking in multiple arguments into as 2D ragged array (i.e. lists of lists of variable lengths).
parg.add_argument('-j', '--jnp', action='append', nargs='*', help="Example with multiple arguments, repeatable.")
    # python __main.py__ -j a list of words -j another list
    # gives cl_arg.jnp == [['a', 'list', 'of', 'words'], ['another', 'list']]
# the alternative to '*' (requiring 0+ arguments) is '+' (requiring 1+ arguments).

# case 6: taking in multiple arguments, but each with fixed lengths and nice names, into a 2D array.
parg.add_argument('-i', '--inp', action='append', nargs=2, metavar=('url','name'), help="Example with 2 arguments.")
    # the metavar is simply used to fill out the names in the help documentation.

# case 7: Taking in multiple arguments, into a 1D array
parg.add_argument('-n', '--numbers', action='extend', nargs='+', type=int, help="A list of ints.")
    # python __main__.py -n 1 2 -n 3
        # cl_arg.numbers == [1, 2, 3]

# case 8: a variable with default True, toggled to False. TAKES NO ARGUMENT.
parg.add_argument('--default-true', action='store_const', const=False, default=True)
    # const: if flag is present, what value will it take.
    # default: if flag is absent, what value will it take.
    # python __main__.py --default-true
        # cl_arg.default_true == False
    # python __main__.py
        # cl_arg.default_true == True
    # python __main__.py --default-true anywordatall
        # Error 

# case 9: a variable with no deafult (None). toggled to True if used. TAKES NO ARGUMENT.
parg.add_argument('--default-none', action='store_const', const=True)
    # python __main__.py --default-true
        # cl_arg.default_none == False
    # python __main__.py
        # cl_arg.default_none == None
     # python __main__.py --default-none anywordatall
        # Error

# case 9: a flag with a different dest than it's long name:
parg.add_argument('-s', '--simple-name', dest="complicated_name")

if __name__=="__main__":
    cl_arg = parg.parse_args()
    from pprint import pprint
    pprint({attr: getattr(cl_arg, attr) for attr in dir(cl_arg) if not attr.startswith("_")},
        sort_dicts=False,
        width=1,)

    if cl_arg.print_this:
        print("print_this: Print this particular statement")
    if cl_arg.S:
        print("S is activated")
    if cl_arg.verbosity: # doesn't get printed of verbosity level = 0
        print(f"verbosity level = {cl_arg.verbosity}")
        if cl_arg.verbosity >1:
            print("(The attributes of cl_arg are automatically sorted alphabetically, and listed above.)")