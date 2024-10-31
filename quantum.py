import numpy as np
import time
from concurrent.futures import ThreadPoolExecutor

# Quantum Sort Implementation
def quantum_sort(arr, num_buckets=10):
    sample_size = min(len(arr), 100)
    sample = np.random.choice(arr, sample_size, replace=False)
    bucket_bounds = np.percentile(sample, np.linspace(0, 100, num_buckets + 1))
    
    buckets = [[] for _ in range(num_buckets)]
    for elem in arr:
        for i in range(num_buckets):
            if bucket_bounds[i] <= elem < bucket_bounds[i + 1]:
                buckets[i].append(elem)
                break
        if elem == bucket_bounds[-1]:
            buckets[-1].append(elem)
    
    def sort_bucket(bucket):
        return sorted(bucket)
    
    with ThreadPoolExecutor() as executor:
        sorted_buckets = list(executor.map(sort_bucket, buckets))
    
    sorted_arr = []
    for bucket in sorted_buckets:
        sorted_arr.extend(bucket)
    
    return sorted_arr

# Quick Sort Implementation
def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)

# Merge Sort Implementation
def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    
    merged = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged

# Timing Function
def time_algorithm(algorithm, arr, name):
    start_time = time.time()
    sorted_arr = algorithm(arr.copy())
    end_time = time.time()
    print(f"{name} took {end_time - start_time:.6f} seconds")
    return sorted_arr

# Example usage and timing comparison
arr = np.random.randint(0, 10000, 10000).tolist()  # Random array of 10,000 integers

print("Timing comparisons for different sorting algorithms:")
sorted_quantum = time_algorithm(quantum_sort, arr, "Bucket Sort")
sorted_builtin = time_algorithm(sorted, arr, "Built-in Timsort")
sorted_quick = time_algorithm(quick_sort, arr, "Quick Sort")
sorted_merge = time_algorithm(merge_sort, arr, "Merge Sort")
