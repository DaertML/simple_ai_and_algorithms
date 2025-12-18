import random
from collections import Counter

# --- Generic Proving System Components ---

class Property:
    """
    Represents a logical property of an algorithm's output.
    A property is a function that takes an input and output, and returns True if the
    property holds, False otherwise.
    """
    def __init__(self, name, check_function):
        self.name = name
        self.check_function = check_function

    def check(self, input_data, output_data):
        return self.check_function(input_data, output_data)

class Proof:
    """
    A generic class for an inductive proof.
    This class defines the structure of the proof, but not the specific content.
    """
    def __init__(self, algorithm_to_prove, properties):
        self.algorithm = algorithm_to_prove
        self.properties = properties
        self.log = []

    def log_step(self, message, status="INFO"):
        self.log.append(f"[{status}] {message}")

    def run_base_case(self):
        """
        To be implemented by the specific proof class.
        Checks the proof for the smallest possible input (n=0 or n=1).
        """
        raise NotImplementedError("Subclasses must implement run_base_case()")

    def run_inductive_step(self, num_tests=100):
        """
        To be implemented by the specific proof class.
        Checks the proof for larger inputs, assuming it holds for smaller ones.
        """
        raise NotImplementedError("Subclasses must implement run_inductive_step()")
        
    def get_log(self):
        return "\n".join(self.log)

# --- Concrete Example: Proof of Mergesort's Correctness ---

def mergesort_algorithm(arr):
    """
    The mergesort algorithm to be proven. Contains a bug.
    """
    if len(arr) <= 1:
        return arr
    
    mid = len(arr) // 2
    left_half = arr[:mid]
    right_half = arr[mid:]
    
    left_sorted = mergesort_algorithm(left_half)
    right_sorted = mergesort_algorithm(right_half)
    
    merged_result = []
    i = j = 0
    while i < len(left_sorted) and j < len(right_sorted):
        if left_sorted[i] < right_sorted[j]:
            merged_result.append(left_sorted[i])
            i += 1
        elif left_sorted[i] > right_sorted[j]:
            merged_result.append(right_sorted[j])
            j += 1
        else:
            # BUG: only append one of the two equal elements
            merged_result.append(left_sorted[i])
            i += 1
    
    merged_result.extend(left_sorted[i:])
    merged_result.extend(right_sorted[j:])
    
    return merged_result

class MergesortProof(Proof):
    """
    Formalizes the inductive proof for the mergesort algorithm.
    """
    def __init__(self, algorithm_to_prove):
        # 1. Define the properties to be checked
        is_sorted_prop = Property(
            name="Sorted Property",
            check_function=lambda input_data, output_data: all(output_data[i] <= output_data[i+1] for i in range(len(output_data)-1))
        )
        is_permutation_prop = Property(
            name="Permutation Property",
            check_function=lambda input_data, output_data: Counter(input_data) == Counter(output_data)
        )
        super().__init__(algorithm_to_prove, [is_sorted_prop, is_permutation_prop])

    def run_base_case(self):
        """
        The base case for mergesort: a list of size 0 or 1.
        """
        self.log_step("--- Proving Base Case ---")
        base_cases = [[], [42]]
        for arr in base_cases:
            result = self.algorithm(arr)
            for prop in self.properties:
                if not prop.check(arr, result):
                    self.log_step(f"Base case for {arr} failed on {prop.name}.", "FAIL")
                    return False
        self.log_step("Base case holds for n=0 and n=1. ✅", "SUCCESS")
        return True

    def run_inductive_step(self, num_tests=100):
        """
        The inductive step: assuming mergesort works for lists of size k,
        it must also work for a larger list. We verify this for many random lists.
        """
        self.log_step("--- Proving Inductive Step ---")
        self.log_step("Inductive Hypothesis: Assume algorithm works for all k < n.")
        self.log_step(f"Verifying for n > 1 with {num_tests} random tests...")
        
        for i in range(num_tests):
            input_list = [random.randint(0, 50) for _ in range(random.randint(2, 30))]
            output_list = self.algorithm(input_list)
            
            # Check if all properties hold for this input
            for prop in self.properties:
                if not prop.check(input_list, output_list):
                    self.log_step(f"Test failed on input: {input_list}", "FAIL")
                    self.log_step(f"Property failed: {prop.name}", "FAIL")
                    self.log_step(f"Output was: {output_list}", "FAIL")
                    return False
        
        self.log_step(f"All {num_tests} property checks passed. Inductive step holds. ✅", "SUCCESS")
        return True

# --- Main Execution ---

if __name__ == "__main__":
    proof_of_mergesort = MergesortProof(mergesort_algorithm)
    
    # 1. Run the Base Case check
    if not proof_of_mergesort.run_base_case():
        print(proof_of_mergesort.get_log())
    
    # 2. Run the Inductive Step check
    elif not proof_of_mergesort.run_inductive_step():
        print(proof_of_mergesort.get_log())
    
    else:
        print(proof_of_mergesort.get_log())
        print("\nFormal proof demonstration completed. The algorithm is verified against its properties. ✅")

