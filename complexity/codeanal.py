import time
import random
import matplotlib.pyplot as plt
import inspect
import re

def measure_runtime(algorithm, input_generator, input_sizes):
    """
    Measures the runtime of a given algorithm for various input sizes.

    Args:
        algorithm (function): The function to be tested.
        input_generator (function): A function that takes an integer 'n' and
                                     returns a suitable input for the algorithm.
        input_sizes (list): A list of integer sizes to test.

    Returns:
        list: A list of tuples (n, runtime) where n is the input size and
              runtime is the measured time in seconds.
    """
    timings = []
    for n in input_sizes:
        # Generate the input data
        input_data = input_generator(n)
        
        # Start the timer
        start_time = time.perf_counter()
        
        # Run the algorithm
        algorithm(input_data)
        
        # Stop the timer
        end_time = time.perf_counter()
        
        # Calculate and store the runtime
        runtime = end_time - start_time
        timings.append((n, runtime))
        print(f"Algorithm took {runtime:.6f}s for input size {n}.")

    return timings

def analyze_complexity_static(algorithm):
    """
    Analyzes the complexity of a given algorithm by inspecting its source code.
    This is a simplified prototype and not a full-fledged formal analysis tool.

    Args:
        algorithm (function): The function to be analyzed.

    Returns:
        str: An estimated Big O complexity notation.
    """
    try:
        source_code = inspect.getsource(algorithm)
    except (TypeError, OSError):
        return "N/A (Source code not available)"

    # Heuristic-based complexity analysis based on code patterns
    
    # 1. Identify common operations with known complexities
    if 'sorted(' in source_code or '.sort(' in source_code:
        return "O(n log n) - Based on sorted() call"
    
    # 2. Count for loops
    for_loops = len(re.findall(r'for\s+', source_code))
    
    if for_loops >= 2:
        return "O(n^2) - Quadratic"
    
    # 3. Check for recursion and division pattern
    recursion_matches = re.findall(r'\b' + algorithm.__name__ + r'\(', source_code)
    is_recursive = len(recursion_matches) > 1

    if is_recursive and ('len(n_list) // 2' in source_code or 'len(arr) // 2' in source_code):
        return "O(n log n) - Recursive with halving"
        
    # 4. Fallback to simpler heuristics
    if for_loops == 1:
        return "O(n) - Linear"
    if is_recursive:
        return "O(n) - likely recursive"
    
    # 5. Default for no loops or recursion
    return "O(1) - Constant"

# --- Example Algorithms to Analyze ---

def linear_algorithm(n_list):
    """An O(n) algorithm (e.g., linear search)."""
    if not n_list:
        return None
    for item in n_list:
        if item == n_list[-1]: # Worst-case scenario
            return item
    return None

def n_log_n_algorithm(n_list):
    """An O(n log n) algorithm (e.g., mergesort)."""
    # A simple, inefficient implementation for demonstration purposes
    if len(n_list) <= 1:
        return n_list
    
    mid = len(n_list) // 2
    left = n_log_n_algorithm(n_list[:mid])
    right = n_log_n_algorithm(n_list[mid:])
    
    return sorted(left + right) # This sort is for simplicity, not a real merge

def n_squared_algorithm(n_list):
    """An O(n^2) algorithm (e.g., bubble sort)."""
    n = len(n_list)
    arr = n_list[:]
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]

# --- Input Generators for Different Scenarios ---

def random_list_generator(n):
    """Generates a random list of integers."""
    return [random.randint(0, 1000) for _ in range(n)]

def sorted_list_generator(n):
    """Generates a sorted list of integers (for best-case scenarios)."""
    return list(range(n))

def reversed_list_generator(n):
    """Generates a reversed list of integers (for worst-case scenarios)."""
    return list(range(n, 0, -1))

# --- Main Execution and Visualization ---

if __name__ == '__main__':
    # Define the input sizes we want to test
    input_sizes = [1000, 2000, 4000, 8000, 16000, 32000]

    # Measure runtimes for different algorithms
    print("--- Measuring O(n) Runtime ---")
    o_n_timings = measure_runtime(linear_algorithm, random_list_generator, input_sizes)
    
    print("\n--- Measuring O(n^2) Runtime ---")
    # For O(n^2), we need smaller inputs because it grows so fast
    o_n2_input_sizes = [100, 200, 400, 800, 1600]
    o_n2_timings = measure_runtime(n_squared_algorithm, random_list_generator, o_n2_input_sizes)

    print("\n--- Measuring O(n log n) Runtime ---")
    o_nlogn_timings = measure_runtime(n_log_n_algorithm, random_list_generator, input_sizes)

    # Separate the data for plotting
    x_n, y_n = zip(*o_n_timings) if o_n_timings else ([], [])
    x_n2, y_n2 = zip(*o_n2_timings) if o_n2_timings else ([], [])
    x_nlogn, y_nlogn = zip(*o_nlogn_timings) if o_nlogn_timings else ([], [])

    # Plot the results to visualize the complexities
    plt.figure(figsize=(10, 6))
    
    plt.plot(x_n, y_n, label='O(n) - Linear', marker='o')
    plt.plot(x_n2, y_n2, label='O(n^2) - Quadratic', marker='s')
    plt.plot(x_nlogn, y_nlogn, label='O(n log n) - Log-Linear', marker='^')
    
    plt.title('Algorithm Runtime vs. Input Size')
    plt.xlabel('Input Size (n)')
    plt.ylabel('Time (seconds)')
    plt.grid(True)
    plt.legend()
    plt.show()

    # --- Best-case vs. Worst-case scenario analysis ---

    print("\n--- Best vs. Worst Case Scenario for Bubble Sort ---")
    bubble_sort_best_timings = measure_runtime(n_squared_algorithm, sorted_list_generator, o_n2_input_sizes)
    bubble_sort_worst_timings = measure_runtime(n_squared_algorithm, reversed_list_generator, o_n2_input_sizes)

    x_best, y_best = zip(*bubble_sort_best_timings)
    x_worst, y_worst = zip(*bubble_sort_worst_timings)

    plt.figure(figsize=(10, 6))
    plt.plot(x_best, y_best, label='Best Case (Sorted)', marker='o')
    plt.plot(x_worst, y_worst, label='Worst Case (Reversed)', marker='s')
    
    plt.title('Bubble Sort: Best vs. Worst Case Runtime')
    plt.xlabel('Input Size (n)')
    plt.ylabel('Time (seconds)')
    plt.grid(True)
    plt.legend()
    plt.show()

    # --- Static Complexity Analysis ---
    print("\n\n--- Static Complexity Analysis ---")
    print(f"linear_algorithm: {analyze_complexity_static(linear_algorithm)}")
    print(f"n_squared_algorithm: {analyze_complexity_static(n_squared_algorithm)}")
    print(f"n_log_n_algorithm: {analyze_complexity_static(n_log_n_algorithm)}")
