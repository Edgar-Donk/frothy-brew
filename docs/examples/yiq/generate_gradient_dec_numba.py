from functools import wraps
from timeit import default_timer as timer
# Use timeit.default_timer instead of timeit.timeit
from time import time
from numba import jit, njit
import numpy as np

def timing(f):
    @wraps(f)
    def wrap(*args, **kw):
        ts = time()
        result = f(*args, **kw)
        te = time()
        print ('func:%r args:[%r, %r] took: %2.4f sec' % \
          (f.__name__, args, kw, te-ts))
        return result
    return wrap

'''
@timing
def f(a):
    for _ in range(a):
        i = 0
    return -1

a = 100000000
f(a)
'''
@timing
def generate_gradient_norm(from_colour, to_colour, height, width):
    new_ch = [np.tile(np.linspace(from_colour[i], to_colour[i], width,
                                  dtype=np.uint8),
                      [height, 1]) for i in range(len(from_colour))]
    return np.dstack(new_ch)

#@timing
@njit
def generate_gradient(from_colour, to_colour, height, width):
    new_ch = [np.tile(np.linspace(from_colour[i], to_colour[i], width,
                                  dtype=np.uint8),
                      [height, 1]) for i in range(len(from_colour))]
    return np.dstack(new_ch)

from_colour = (123, 26, 245)
to_colour = (245, 203, 45)
height=26
width=300

generate_gradient(from_colour, to_colour, height, width)

print('repeat')

generate_gradient(from_colour, to_colour, height, width)

print('normal')

generate_gradient_norm(from_colour, to_colour, height, width)
"""
'rgb_to_yiq'  375.82 ms
repeat
'rgb_to_yiq'  0.00 ms
normal
'rgb_to_yiq_norm'  0.00 ms
"""