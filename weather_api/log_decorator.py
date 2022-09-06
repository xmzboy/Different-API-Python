import time
from functools import wraps


def log_dec(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        print(f"Start {func.__name__}")
        start_f = time.time()
        result = func(*args, **kwargs)
        print(f"Stop {func.__name__}, executing time = {time.time() - start_f}")
        return result
    return wrap
