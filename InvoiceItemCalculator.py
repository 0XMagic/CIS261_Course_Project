def ask_float(phrase: str) -> float:
	value = input(phrase + ":\t")
	try:
		result = float(value)
	except ValueError:
		print("That's not a valid float...")
		result = ask_float(phrase)
	return result


def ask_int(phrase: str) -> int:
	value = input(phrase + ":\t")
	try:
		result = int(value)
	except ValueError:
		print("That's not a valid int...")
		result = ask_int(phrase)
	return result


def ask_item():
	price = ask_float("Enter price")
	quantity = ask_int("Enter quantity")
	print("\n".join(
			f"{k}:\t{v}" for k, v in {
					"PRICE":    f"{price:.2f}",
					"QUANTITY": quantity,
					"TOTAL":    f"{price * float(quantity):.2f}"
			}.items()
	))


def main():
	print("Invoice item calculator")
	run = "y"
	while run == "y":
		ask_item()
		run = ""
		while run not in ("y", "n"):
			run = input("Input another item? (y/n)").lower()
	print("Bye bye!")


if __name__ == '__main__':
	main()
