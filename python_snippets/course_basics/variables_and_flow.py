name = "Learner"
score = 87
passed = score >= 70

if passed:
    print(f"{name} passed with score={score}")
else:
    print(f"{name} did not pass")

numbers = [1, 2, 3, 4, 5]
odd_squares = [n * n for n in numbers if n % 2 == 1]
print("odd_squares=", odd_squares)
