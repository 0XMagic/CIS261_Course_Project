def factorial_iter(n: int):
	result = 1
	for i in range(1, n):
		result *= i
	return result


def factorial_recur(n: int):
	if n <= 1:
		return max(n, 1)
	return n * factorial_recur(n - 1)


numbers = [
		0, 5, 10, 25, 50, 100
]

print("Iterative factorial:")
for n in numbers:
	print(f"{n}! = {factorial_iter(n)}")

print()
print("Recursive factorial:")
for n in numbers:
	print(f"{n}! = {factorial_recur(n)}")
