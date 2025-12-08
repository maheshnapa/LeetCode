from typing import List

class solution:
    def minProductSum(self, nums1: List[int], nums2: List[int]) -> int:
        nums1.sort()
        nums2.sort(reverse=True)
        return sum(x * y for x, y in zip(nums1, nums2))
    

class solution:
    def minProductSum(self, nums1: List[int], nums2: List[int]) -> int:
        for i , j in zip(sorted(nums1), sorted(nums2)):
            total += i * j
        return total
    



import math

def min_product_sum_strict(a: List[int], b: List[int]) -> int:
    """Requires len(a) == len(b). Raises ValueError otherwise."""
    if len(a) != len(b):
        raise ValueError("Lists must have equal length")
    a_sorted = sorted(a)
    b_sorted = sorted(b, reverse=True)
    return sum(x * y for x, y in zip(a_sorted, b_sorted))

def min_product_sum_trim(a: List[int], b: List[int]) -> int:
    """Trims to the shorter length and computes min product-sum for those pairs."""
    n = min(len(a), len(b))
    a_sorted = sorted(a)[:n]
    b_sorted = sorted(b, reverse=True)[:n]
    return sum(x * y for x, y in zip(a_sorted, b_sorted))

def min_product_sum_pad_zero(a: List[int], b: List[int]) -> int:
    """Pads the shorter list with zeros so lengths match, then computes min product-sum."""
    la, lb = len(a), len(b)
    if la < lb:
        a_extended = a + [0] * (lb - la)
        b_extended = b.copy()
    elif lb < la:
        b_extended = b + [0] * (la - lb)
        a_extended = a.copy()
    else:
        a_extended, b_extended = a.copy(), b.copy()

    a_sorted = sorted(a_extended)
    b_sorted = sorted(b_extended, reverse=True)
    return sum(x * y for x, y in zip(a_sorted, b_sorted))

def min_product_sum(a: List[int], b: List[int], mode: str = "strict") -> int:
    """General wrapper. mode in {"strict", "trim", "pad"}."""
    if mode == "strict":
        return min_product_sum_strict(a, b)
    if mode == "trim":
        return min_product_sum_trim(a, b)
    if mode == "pad":
        return min_product_sum_pad_zero(a, b)
    raise ValueError("Unknown mode: choose 'strict', 'trim', or 'pad'")