import itertools
import time
from time import perf_counter_ns

input = 10
loops = 100000
overall_timer = time.perf_counter_ns()
for _ in itertools.repeat(None, loops):
    counter = time.perf_counter_ns()
    return_value = input
    # time.perf_counter_ns()
completed_overall_timer = time.perf_counter_ns() - overall_timer
print(f"Loop Overall time: {completed_overall_timer/loops}")


overall_timer = time.perf_counter_ns()
for _ in itertools.repeat(None, loops):
    pass
looping_overall_timer = time.perf_counter_ns() - overall_timer
print(f"Loop Overall time: {looping_overall_timer/loops}")

print(f"Pure overhead = {completed_overall_timer/loops - looping_overall_timer/loops}")

overall_timer = perf_counter_ns()
for _ in itertools.repeat(None, loops):
    counter = perf_counter_ns()
    return_value = input
    # time.perf_counter_ns()
completed_overall_timer = perf_counter_ns() - overall_timer
print(f"Loop Overall time: {completed_overall_timer/loops}")


overall_timer = perf_counter_ns()
for _ in itertools.repeat(None, loops):
    pass
looping_overall_timer = perf_counter_ns() - overall_timer
print(f"Loop Overall time: {looping_overall_timer/loops}")

print(f"Pure overhead = {completed_overall_timer/loops - looping_overall_timer/loops}")
