import math


def factorial(n):
    if n < 0:
        raise ValueError("n must be >= 0")
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result


def ncr(n, r):
    if r < 0 or r > n:
        return 0
    return factorial(n) // (factorial(r) * factorial(n - r))


def npr(n, r):
    if r < 0 or r > n:
        return 0
    return factorial(n) // factorial(n - r)


def binomial_pmf(k, n, p):
    return ncr(n, k) * (p ** k) * ((1 - p) ** (n - k))


def binomial_cdf(k, n, p):
    return sum(binomial_pmf(i, n, p) for i in range(0, k + 1))


def normal_pdf(x, mean=0.0, std=1.0):
    coef = 1.0 / (std * math.sqrt(2 * math.pi))
    exp = math.exp(-((x - mean) ** 2) / (2 * std ** 2))
    return coef * exp


def normal_cdf(x, mean=0.0, std=1.0):
    return 0.5 * (1 + math.erf((x - mean) / (std * math.sqrt(2))))
