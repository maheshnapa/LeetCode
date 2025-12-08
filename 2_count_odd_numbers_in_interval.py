class solution:
    def countodds(self, low: int, high: int) -> int:
        count = 0
        list_odd = []
        for i in range(low, high + 1):
            if i % 2 != 0:
                count += 1
                list_odd.append(i)
        return count, list_odd
    
obj = solution()
print(obj.countodds(3, 7))




class solution2:
    def countodds(self, low: int, high: int) -> int:
        return (high + 1) // 2 - low // 2
    
obj2 = solution2()
print(obj2.countodds(3, 11))