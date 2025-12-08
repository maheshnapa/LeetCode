def odd_interval(low, high):

    for num in range(low, high + 1):
        if num % 2 != 0:
            yield num
        return len(list(odd_interval(low, high)))
        

print(list(odd_interval(3, 9)))   
print(odd_interval(3, 9))
print(odd_interval(2, 8))