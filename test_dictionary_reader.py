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
        return_list = [ convert_str_value(elem) for elem in string.replace("[","").replace("]","").split(",") ] #recursively call itself on the elements of the list
        if len(return_list)==0: return [] #return a instead of a [None] in case of an empty string
        return return_list
    if "'" in string or '"' in string: #filter out the strings
        return string.replace("'","").replace('"','').replace(" ","")
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
def read_and_pop_dict_out_of_file(filename):
    with open(filename,"r") as f:
        data = f.readlines()
    braces = find_matching_braces(data)
    try:
        first_pair = next(iter(braces.items()))
    except StopIteration:
        sys.exit("No more dictionaries in file")
    with open(filename, "w") as f:
        # for line in data[first_pair[1]+1:] :
        for line in data[:] :
            f.write(line)
    first_dict = data[first_pair[0]:first_pair[1]+1]
    first_dict = [ line.replace("{","").replace("}","").replace(",\n","") for line in first_dict]
    first_dict = [ line for line in first_dict if ":" in line ] #ignore all lines that doesn't contain information
    dictionary_to_be_returned = {}
    for line in first_dict:
        key, value = line.split(":")
        value = convert_str_value(value)
        #must ensure that all parts are not space
        assert key
        key = key.replace(" ","") #purge all spaces from the key
        dictionary_to_be_returned[key] = value
    return dictionary_to_be_returned

def continuous_neural_network_runner(filename):
    dictionary_read = read_and_pop_dict_out_of_file(filename)
    NN = NeuralNetwork()
    for k, v in dictionary_read.items():
        print(k,":",v)