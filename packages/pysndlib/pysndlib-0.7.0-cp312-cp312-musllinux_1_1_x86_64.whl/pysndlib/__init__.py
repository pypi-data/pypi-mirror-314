import os

def get_include():
    import pysndlib
    import os.path
    return os.path.dirname(pysndlib.__file__)
    
