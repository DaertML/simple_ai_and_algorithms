import bisect

def find_latest_non_overlapping_class(classes, current_class_index):
    """
    Helper function to find the index of the latest class that finishes
    before the current class starts. Uses binary search (bisect_right)
    on the sorted end times to be efficient.

    Args:
        classes (list): A list of tuples, where each tuple represents a class
                        (start_time, end_time, value).
        current_class_index (int): The index of the current class.

    Returns:
        int: The index of the latest non-overlapping class, or -1 if none exists.
    """
    # Get the start time of the current class
    current_start_time = classes[current_class_index][0]

    # Extract all end times for binary search
    end_times = [c[1] for c in classes]

    # bisect_right returns an insertion point which comes after any
    # existing entries of the same value. We want the one just before
    # the start time of the current class.
    # The search is on a slice up to the current class's index to avoid
    # looking at later classes.
    i = bisect.bisect_right(end_times, current_start_time, hi=current_class_index)

    # We found a potential non-overlapping class, but the index i needs to be
    # adjusted to point to the actual latest finishing class.
    # The bisect_right function returns the index to insert the item, so
    # the index of the found element is i-1.
    if i > 0:
        return i - 1
    else:
        # No such class exists
        return -1


def solve_class_schedule(classes):
    """
    Solves the class schedule problem using dynamic programming and
    reconstructs the optimal schedule.

    The problem is to find the maximum value of a set of non-overlapping classes.
    This is also known as the weighted interval scheduling problem.

    The algorithm works as follows:
    1. Sort the classes by their end times. This is crucial for the DP approach.
    2. Initialize a DP table `dp` where dp[i] will store the maximum value
       that can be obtained using a subset of the first i+1 classes.
    3. Iterate through the sorted classes from the first to the last.
    4. For each class `i`:
       - `incl_val`: The value if we *include* the current class. This is the
                     class's own value plus the maximum value we could have
                     obtained from a non-overlapping predecessor class.
                     We use a helper function and binary search to find this
                     predecessor efficiently.
       - `excl_val`: The value if we *exclude* the current class. This is simply
                     the maximum value obtained from the first i classes,
                     which is stored in `dp[i-1]`.
       - `dp[i]` is the maximum of `incl_val` and `excl_val`.
    5. After filling the DP table, we backtrack from the end to reconstruct
       the optimal schedule. We do this by checking at each step whether the
       current optimal value came from including or excluding the class.

    Args:
        classes (list): A list of tuples, where each tuple represents a class
                        in the format (start_time, end_time, value).
                        Example: [(1, 3, 20), (2, 5, 30), (4, 6, 40)]

    Returns:
        tuple: A tuple containing the maximum total value (int) and a list
               of the classes in the optimal schedule.
    """
    n = len(classes)
    if n == 0:
        return 0, []

    # 1. Sort classes by their end times. This is a critical step.
    classes.sort(key=lambda x: x[1])

    # 2. Initialize DP table
    dp = [0] * n
    dp[0] = classes[0][2]

    # 3. Iterate through classes to fill the DP table
    for i in range(1, n):
        current_class = classes[i]
        
        # Case 1: Include the current class
        incl_val = current_class[2]
        latest_non_overlapping_index = find_latest_non_overlapping_class(classes, i)

        if latest_non_overlapping_index != -1:
            incl_val += dp[latest_non_overlapping_index]

        # Case 2: Exclude the current class
        excl_val = dp[i-1]

        # Take the maximum of including or excluding the current class
        dp[i] = max(incl_val, excl_val)

    # 5. Backtrack to reconstruct the schedule
    schedule = []
    i = n - 1
    while i >= 0:
        # Check if the current value in DP table came from including the current class
        # We need to compare with the value we would have from the non-overlapping
        # predecessor.
        latest_non_overlapping_index = find_latest_non_overlapping_class(classes, i)
        
        incl_val_check = classes[i][2]
        if latest_non_overlapping_index != -1:
            incl_val_check += dp[latest_non_overlapping_index]
        
        # We check if dp[i] equals the value of including class i. This implies
        # that class i was chosen. We also add a small epsilon for floating
        # point comparisons, though not strictly necessary here.
        if dp[i] == incl_val_check:
            schedule.append(classes[i])
            i = latest_non_overlapping_index
        else:
            # The current optimal value came from excluding this class
            i -= 1

    schedule.reverse() # Reverse to get the schedule in chronological order

    return dp[n - 1], schedule


# --- Example Usage ---
if __name__ == "__main__":
    # Example from a classic dynamic programming problem
    # Classes are (start, end, value)
    classes_list = [
        (1, 4, 20),  # Class 1
        (3, 5, 20),  # Class 2 (overlaps with 1)
        (6, 7, 50),  # Class 3
        (5, 9, 30),  # Class 4 (overlaps with 3)
        (8, 10, 60), # Class 5
    ]

    # Expected output:
    # Max value is 80, with schedule [(3, 5, 20), (8, 10, 60)]
    max_value, optimal_schedule = solve_class_schedule(classes_list)
    print(f"The maximum value of non-overlapping classes is: {max_value}")
    print(f"The optimal schedule is: {optimal_schedule}")

    # Another example
    classes_list_2 = [
        (1, 2, 5),
        (3, 4, 10),
        (2, 6, 8),
        (5, 7, 12)
    ]
    max_value_2, optimal_schedule_2 = solve_class_schedule(classes_list_2)
    print(f"\nFor the second list, the maximum value is: {max_value_2}")
    print(f"The optimal schedule is: {optimal_schedule_2}") # Expected: [(1, 2, 5), (5, 7, 12)]

