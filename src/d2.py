def is_safe(row):
    inc = [row[i + 1] - row[i] for i in range(len(row) - 1)]
    if set(inc) <= {1, 2, 3} or set(inc) <= {-1, -2, -3}:
        return True
    return False

data = [[int(y) for y in x.split(' ')] for x in open('02.txt').read().split('\n')]

safe_count = sum([is_safe(row) for row in data])
print(safe_count)

safe_count = sum([any([is_safe(row[:i] + row[i + 1:]) for i in range(len(row))]) for row in data])
print(safe_count)