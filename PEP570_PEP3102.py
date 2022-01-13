def name(p1, p2=None, /, p_or_kw=None, *, kw):
    print(p1)
    print(p2)
    print(p_or_kw)
    print(kw)
    return
if __name__=='__main__':
    name(1, kw='stuff')
    name(1, p2='p2') # fails

# at definition time, / forbids any arguments in front to be used as KW argument,                                         
# at definition time, * forbids any arguments after it to be used as positional argument.                                 
# and at calling time, the user is only allowed to switch over from positional to KW once, 
# it means they must place this switch-over point carefully / <= switch-over-point <= *.
