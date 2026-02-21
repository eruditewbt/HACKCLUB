def add_vec(a, b):
    return [x + y for x, y in zip(a, b)]


def sub_vec(a, b):
    return [x - y for x, y in zip(a, b)]


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def scalar_mul(a, scalar):
    return [scalar * x for x in a]


def transpose(m):
    if not m:
        return []
    return [list(row) for row in zip(*m)]


def matmul(a, b):
    if not a or not b:
        return []
    b_t = transpose(b)
    return [[dot(row, col) for col in b_t] for row in a]


def shape(m):
    if not m:
        return (0, 0)
    return (len(m), len(m[0]))
