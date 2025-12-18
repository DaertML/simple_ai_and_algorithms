import random
from collections import Counter

def mergesort(arr):
    """
    Mergesort algorithm implementation for demonstration.
    """
    if len(arr) <= 1:
        return arr
    
    mid = len(arr) // 2
    left_half = arr[:mid]
    right_half = arr[mid:]
    
    left_sorted = mergesort(left_half)
    right_sorted = mergesort(right_half)
    
    # In a real proof, we'd formally prove this part is correct.
    merged_result = []
    i = j = 0
    while i < len(left_sorted) and j < len(right_sorted):
        if left_sorted[i] <= right_sorted[j]:
            merged_result.append(left_sorted[i])
            i += 1
        else:
            merged_result.append(right_sorted[j])
            j += 1
    
    merged_result.extend(left_sorted[i:])
    merged_result.extend(right_sorted[j:])
    
    return merged_result


def is_sorted(arr):
    """
    Checks if a list is sorted.
    This corresponds to the 'Correctness' property from our proof.
    """
    for i in range(len(arr) - 1):
        if arr[i] > arr[i+1]:
            return False
    return True

def prop_based_check(num_tests=1000):
    """
    Checks the two main properties of mergesort's correctness.
    This acts as our Python 'formal proof log'.
    """
    print("Beginning property-based checks...")
    for i in range(num_tests):
        # Generate a random list to test
        random_list = [random.randint(0, 50) for _ in range(random.randint(2, 30))]
        
        # Store the original list's element counts for the 'Permutation' check
        original_counts = Counter(random_list)
        
        # Run the mergesort function
        result_list = mergesort(random_list)

        # Check Property 1: Is the result sorted?
        if not is_sorted(result_list):
            print(f"Test failed for list: {random_list}")
            print(f"Result is not sorted: {result_list}")
            print("\nMergesort has a bug! The 'Correctness' property failed. ❌")
            return False

        # Check Property 2: Are the element counts the same?
        # This confirms no elements were lost or gained.
        result_counts = Counter(result_list)
        if original_counts != result_counts:
            print(f"Test failed for list: {random_list}")
            print(f"Expected counts: {original_counts}")
            print(f"Got counts: {result_counts}")
            print("\nMergesort has a bug! The 'Completeness' property failed. ❌")
            return False
    
    print("\nAll property checks passed! The algorithm seems robust. ✅")
    return True

# Run the property-based check
prop_based_check()
