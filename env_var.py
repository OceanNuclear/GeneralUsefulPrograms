import os
from pprint import pprint
if __name__=="__main__":
	# print(os.environ['TESTVAR'])
	all_defined_vars = list(os.environ.keys())
	pprint(all_defined_vars)