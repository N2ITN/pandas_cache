from pandas_cache.pandas_cache import pd_cache
from pandas_cache.pandas_cache import del_cached
from pandas_cache.timer import timeit


#TODO: What exactly are you trying to do here? Avoid explicit imports???

#TODO: You prly shouldn't be doing this in the first place because it's just a less efficient way to import stuff.
#TODO: Ex: you'll be calling
# `pandas_cache.os.path.join(pandas_cache.os.path.realpath(...),...)`
#TODO: instead of
# `os.path.join(os.path.realpath(...),...)

# import os
# import time
# from functools import wraps
# import pandas as pd # <== NOOOOOOOOOOOO BAD MONKEY
