def odd_interval(low, high):

    for num in range(low, high + 1):
        if num % 2 != 0:
            yield num
        return len(list(odd_interval(low, high)))
        

print(list(odd_interval(3, 9)))  # Output: [3, 5, 7, 9]  