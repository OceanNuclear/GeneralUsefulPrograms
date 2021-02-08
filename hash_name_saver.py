import contextlib
import datetime, os, json
JSON_FILENAME = "index.json"
# import fcntl

class HashSaver(contextlib.ContextDecorator):
    def __init__(self, trim_length=10):
        self.time = datetime.datetime.now()
        self.hash_name = hex(hash(self.time)).lstrip("-").lstrip("0x").zfill(16)[:trim_length]
        
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is None:
            return True
        else:
            return False

def _strip_once(string, lstrip_char, rstrip_char):
    if string.startswith(lstrip_char):
        string = string[len(lstrip_char):]
    if string.endswith(rstrip_char):
        string = string[:-len(rstrip_char)]
    return string

def _append_dict_into_json_dict(_dict, path, encoder=json.JSONEncoder):
    """
    open a json that's just a big dictionary, and append in a smaller dictionary.
    # shall acquire file lock first to avoid two parallel python processes writing to file at the same time.
    # I'll implement this feature later as this may take a bit of time.
    """
    with open(path, 'ab+') as f:
        f.seek(0,2)                             # Go to the end of file.
        f.seek(-1,2)                            # Remove the last }
        f.truncate()                            # to open the dictionary.
        f.write(encoder.item_separator.encode())# Add a separator.
        dumps_text = _strip_once(json.dumps(_dict, cls=encoder), "{", "}")
        # Strip the inserted dictionary bare, to expose the first level key+ value pair (of which there should only be one).
        f.write(dumps_text.encode())
        f.write("}".encode())                   # Close the dictionary.

import numpy as np
class NumpyEncoder(json.JSONEncoder):
    def default(self, o):
        """
        The object will be sent to the .default() method if it can't be handled
        by the native ,encode() method.
        The original JSONEncoder.default method only raises a TypeError;
        so in this class we'll make sure it handles these specific cases (numpy, openmc and uncertainties)
        before defaulting to the JSONEncoder.default's error raising.
        """
        # numpy types
        if isinstance(o, np.integer):
            return int(o)
        elif isinstance(o, np.ndarray):
            return o.tolist()
        elif isinstance(o, np.float):
            return float(o)
        else:
            return super().default(o)

class ExampleClassSaver(HashSaver):
    def __init__(self, parameters, trim_length=10, encoder=NumpyEncoder):
        super().__init__(trim_length)
        self.parameters = parameters
        self.encoder = encoder
        self.saved = False

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Normal method for handling exiting
        """
        if exc_type is None: # when quitting without error:
            return True
        else:
            return False

    def save(self):
        dump_dict = {self.hash_name : self.parameters}
        if not os.path.exists(JSON_FILENAME):
            with open(JSON_FILENAME, "w") as j:
                json.dump(dump_dict, j, cls=self.encoder)
        else:
            _append_dict_into_json_dict(dump_dict, JSON_FILENAME, self.encoder)
        self.saved = True

if __name__=='__main__':
    with ExampleClassSaver({"parameters" : np.empty(3)}, 16) as example_parameters:
        example_parameters.save()