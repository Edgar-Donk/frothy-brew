import timeit
from numba import jit

def yiq_to_rgb_normal(y, i, q):
    # assume I and Q between ±1, correct for coloursys
    y = min(max(y, 0), 100)
    i = min(max(i, -100), 100)
    q = min(max(q, -100), 100)
    y = y / 100
    i = 0.599 * i / 100
    q = 0.5251 * q / 100

    red = y + 0.9468822170900693 * i + 0.6235565819861433 * q
    green = y - 0.27478764629897834 * i - 0.6356910791873801 * q
    blue = y - 1.1085450346420322 * i + 1.7090069284064666 * q
    red = min(max(red, 0), 1)
    green = min(max(green, 0), 1)
    blue = min(max(blue, 0), 1)

    return (int(red * 255 + 0.5), int(green * 255 + 0.5), int(blue * 255 + 0.5))

@jit
def yiq_to_rgb_jit(y, i, q):
    # assume I and Q between ±1, correct for coloursys
    y = min(max(y, 0), 100)
    i = min(max(i, -100), 100)
    q = min(max(q, -100), 100)
    y = y / 100
    i = 0.599 * i / 100
    q = 0.5251 * q / 100

    red = y + 0.9468822170900693 * i + 0.6235565819861433 * q
    green = y - 0.27478764629897834 * i - 0.6356910791873801 * q
    blue = y - 1.1085450346420322 * i + 1.7090069284064666 * q
    red = min(max(red, 0), 1)
    green = min(max(green, 0), 1)
    blue = min(max(blue, 0), 1)

    return (int(red * 255 + 0.5), int(green * 255 + 0.5), int(blue * 255 + 0.5))

# compute normal yiq_to_rgb convert time
def normal_time():
    SETUP_CODE = '''
from __main__ import yiq_to_rgb_normal'''

    TEST_CODE = '''
y = 30
i = 60
q = -35
yiq_to_rgb_normal(y, i, q)'''

    # timeit.repeat statement
    times = timeit.repeat(setup = SETUP_CODE,
                          stmt = TEST_CODE,
                          repeat = 3,
                          number = 10000)

    # printing minimum exec time
    print('normal yiq_to_rgb convert time: {}'.format(min(times)))

# compute jit yiq_to_rgb convert time
def numba_time():
    SETUP_CODE = '''
from __main__ import yiq_to_rgb_jit
from numba import jit'''

    TEST_CODE = '''
y = 30
i = 60
q = -35
yiq_to_rgb_jit(y, i, q)'''

    # timeit.repeat statement
    times = timeit.repeat(setup = SETUP_CODE,
                          stmt = TEST_CODE,
                          repeat = 3,
                          number = 10000)

    # printing minimum exec time
    print('numba yiq_to_rgb convert time: {}'.format(min(times)))

if __name__ == "__main__":
    normal_time()
    numba_time()

"""
normal yiq_to_rgb convert time: 0.0738138880000001
numba yiq_to_rgb convert time: 0.005452893999999819

# running python 3.12.7
normal yiq_to_rgb convert time: 0.06757891501183622
numba yiq_to_rgb convert time: 0.008976934012025595
"""