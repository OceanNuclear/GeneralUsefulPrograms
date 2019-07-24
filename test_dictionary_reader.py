def find_matching_braces(list_of_lines):
    '''given a collection of text lines stored as a list, find out the indices of the lines where matching braces occurs'''
    #copying the design pattern of finding matching paranthesis.
    brace_stack = [] #stack
    d = {}
    #d stores the opening and closing braces' line numbers
    for l_num, line in enumerate(list_of_lines):
        if "{" in line: brace_stack.append(l_num)
        if "}" in line:
            try:
                d[brace_stack.pop()]=l_num
            except IndexError:
                print("More } than {")
    if len(brace_stack)!=0: print("More { than }")
    return d
def convert_str_value(string):
    if ("[" in string) and ("]" in string): #filter out the list
        splitted_list = string.strip("[]").split(",")
        #filter out the empty list case:
        if len(splitted_list)==1:
            if splitted_list[0]=="":
                #return an empty list [] instead of a [None]
                return []
        return_list = [ convert_str_value(elem.strip()) for elem in splitted_list ] #recursively call itself on the elements of the list
        return return_list
    if string.startswith('"') and string.endswith('"'): #filter out the strings
        assert string.count('"')==2, "too many quotation marks!"
        return string[1:-1]
    if string.startswith("'") and string.endswith("'"): #filter out the strings
        assert string.count("'")==2, "too many quotation marks!"
        return string[1:-1]
    if "False" in string: return False #filter out the booleans and None's
    if "True" in string: return True
    if "None" in string: return None
    if "." in string:#filter out the floats
        try:
            return float(string)
        except ValueError: #filter out the function objects
            if ("<" in string) and (">" in string) and ("object" in string):
                raise ValueError("Cannot input a method object as a string; but can try using string e.g. 'AdaGrad'")
    return int(string) #only integers should be left
def read_dict_out_of_file(filename):
    with open(filename,"r") as f:
        data = f.readlines()
    braces = find_matching_braces(data)
    try:
        first_pair = next(iter(braces.items()))
    except StopIteration:
        sys.exit("No more dictionaries in file")
    with open(filename, "w") as f:
        for line in data[first_pair[1]+1:] :
        # for line in data[:] :
            f.write(line)
    first_dict = []
    for line in data[first_pair[0]:first_pair[1]+1]:
        if ":" in line:
            line = line.strip().strip("{}").strip()
            if line[-1]==",": line = line[:-1] #remove the rightmost comma
            first_dict.append(line)
    dictionary_to_be_returned = {}
    for line in first_dict:
        #split the "sentence" down the middle at the ':'
        key, value = [ arg.strip() for arg in line.split(":") ]
        #must ensure that none of these are empty
        assert not len(key)==0, "Must have a key before the :"
        assert not len(value)==0, "Must have a value after the :"
        dictionary_to_be_returned[key] = convert_str_value(value)
    return dictionary_to_be_returned

def continuous_neural_network_runner(filename):
    dictionary_read = read_dict_out_of_file(filename)
    for k, v in dictionary_read.items():
        print(k,":",v,)
continuous_neural_network_runner("test_dict.txt")