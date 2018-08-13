""" 
Implements on disk caching of transformed dataframes 

Used on a function that returns a single pandas object, 
this decorator will execute the function, cache the dataframe as a pickle
file using the hash of the raw code as a unique identifier. 
The next time the function runs, if the hash of the raw code matches 
what is on disk, the decoratored function will simply load and return 
the pickled pandas object.
This can result in speedups of 10 to 100 times, or more, depending on the 
complexity of the function that creates the dataframe.

If the function changes since the last hash, this decorator will automatically delete 
the previously cached pickle and save a new one, preventing disk pollutionself.
The caveat is that if the function name changes or the function is deleted, previously
cached dataframes will remain on disk. For this purpose there is a 'del_cached' function
that is will simply delete any objects cached by this decorator. 
"""

from functools import wraps

import pandas as pd
import os
from glob import glob
import hashlib
import inspect


def pd_cache(func):

    try:
        os.mkdir('.pd_cache')
        print('created `./.pd_cache/ dir')

    except FileExistsError:
        pass

    @wraps(func)
    def cache(*args, **kw):
        # Get raw code of function as str and hash it
        func_code = ''.join(inspect.getsourcelines(func)[0]).encode('utf-8')
        hsh = hashlib.md5(func_code).hexdigest()[:6]

        f = '.pd_cache/' + func.__name__ + '_' + hsh + '.pkl'

        if os.path.exists(f):
            df = pd.read_pickle(f)
            print(f'\t | read {f}')
            return df

        else:
            # Delete any file name that has `cached_[func_name]_[6_chars]_.pkl`

            for cached in glob(f'./.pd_cache/{func.__name__}_*.pkl'):
                if (len(cached) - len(func.__name__)) == 20:
                    os.remove(cached)
                    print(f'\t | removed', cached)
            # Write new
            df = func(*args, **kw)
            df.to_pickle(f)
            print(f'\t | wrote {f}')
            return df

    return cache


@pd_cache
def test():

    return pd.DataFrame([5, 54])


def del_cached():
    # TODO: update this to use the glob format from pd_cache to safeguard deleting arbitrary files.
    cached = os.listdir('./.pd_cache/')
    print(cached)
    if len(cached) > 0:
        [os.remove(x) for x in cached]
        print(f'removed {cached}')
        return
    else:
        return 'No cached DataFrames'


if __name__ == '__main__':
    test()
    # del_cached()