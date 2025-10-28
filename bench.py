import time
import multiprocessing
import zlib
import random
import numpy as np

#integer operations
def integer_operations(n):
    total = 0
    for i in range(n):
        total += i * i
    return total

# floating-point operations
def floating_point_operations(n):
    total = 0.0
    for i in range(n):
        total += np.sin(i) * np.cos(i)
    return total

#compression
def compression_test(data):
    return zlib.compress(data)

#memory access
def memory_access(n):
    arr = [random.randint(0, 100) for _ in range(n)]
    total = sum(arr)
    return total

# multiprocessing wapper
def run_parallel(func, args, num_processes):
    with multiprocessing.Pool(processes=num_processes) as pool:
        results = pool.map(func, args)
    return results
    

def average_time(func, *args, iterations=10):
    times = []
    for _ in range(iterations):
        start = time.time()
        func(*args)
        times.append(time.time() - start)
    return sum(times) / len(times)

# Number of iterations for each test
N = 10**6
data = b"A" * N
num_cores = multiprocessing.cpu_count()
args = [N // num_cores] * num_cores
data_chunks = [data[i * len(data) // num_cores:(i + 1) * len(data) // num_cores] for i in range(num_cores)]

# Run benchmarks single vs multiple

int_single_time = average_time(integer_operations, N)
fp_single_time = average_time(floating_point_operations, N)
comp_single_time = average_time(compression_test, data)
mem_single_time = average_time(memory_access, N)

int_multi_time = average_time(run_parallel, integer_operations, args, num_cores)
fp_multi_time = average_time(run_parallel, floating_point_operations, args, num_cores)
comp_multi_time = average_time(run_parallel, compression_test, data_chunks, num_cores)
mem_multi_time = average_time(run_parallel, memory_access, args, num_cores)

print("Single Core Average of 10 time X 10**6 iterations")
print(f"Int:{int_single_time:.4f}")
print(f"FP:{fp_single_time:.4f}")
print(f"ZIP:{comp_single_time:.4f}")
print(f"Memory:{mem_single_time:.4f}\n")

print("Multi Core Average of 10 time X 10**6 iterations")
print(f"Int:{int_multi_time:.4f}")
print(f"FP:{fp_multi_time:.4f}")
print(f"ZIP:{comp_multi_time:.4f}")
print(f"Memory:{mem_multi_time:.4f}")
