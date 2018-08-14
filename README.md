# 🐼 💸 Pandas Cache


## Purpose
This module reduces loading times for resource-intensive pandas operations dramatically by memoizing the results of functions that return pandas DataFrames and Series. This can reduce over-dependence on jupyter notebooks for slow data operations.


The `@pd_cache` decorator function wraps a function that returns a pandas object. The `@timeit` decorator is optional, and provides benchmarking times. The `del_cached()` function deletes all cached objects if desired.

## Example Usage

```
from pandas_cache import pd_cache, timeit
import pandas as pd

@timeit
@pd_cache
def time_consuming_dataframe_operation():
    # Make a large dictionary 
    x = {i: k for i, k in enumerate(range(2**16))}
    return pd.DataFrame([x])


time_consuming_dataframe_operation()
```

Output on first run:

```
	 > function time_consuming_dataframe_operation time: 2.5 s
	 | wrote .pd_cache/time_consuming_dataframe_operation_ace6f4.pkl
```
Output on second run:
```
	 | read .pd_cache/time_consuming_dataframe_operation_ace6f4.pkl
	 > function time_consuming_dataframe_operation time: 6.0 ms
```

## How It Works
At runtime, the `@pd_cache` decorator :
* Takes the hash of the decorated function's plain text code
* Pickles the pandas object returned by the decorated function
* Saves the pickle to a new `./pd_cache/` dir and includes a slice of the hash and the name of the decorated fucntion in the filename.  Upon running a second time the decorator:
* Hashes the function code again
* If the file already exists in the cache folder, it is loaded. 
* If the code in the function has changed in any way, the decorator deletes the original pickle file and replaces it with the new output.

## Caveats
* Only works with functions that return pandas objects with the `.to_pickle()` method.
* If the function takes input args and these are changed after a cache operation, the decorator will naively load the existing pickle. To mitigate this `pandas_cache.del_cached()` can be invoked to remove all pickled pandas objects, or alternatively the pickle file can be deleted manually.




