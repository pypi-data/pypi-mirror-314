def geometric_progression(start, multiplier, n):
    return [start * (multiplier ** i) for i in range(n)]


results = geometric_progression(1, 2, 12)
gener = [1 * (2 ** i) for i in range(12)]
print(gener)
