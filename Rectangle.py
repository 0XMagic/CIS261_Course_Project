class Rectangle:
	def __init__(self, width: int, height: int):
		self.width: int = width
		self.height: int = height

	@classmethod
	def ask(cls) -> "Rectangle":
		w = "?"
		h = "?"
		while not w.isdigit(): w = input("Enter Height:\t")
		while not h.isdigit(): h = input("Enter Height:\t")
		return cls(int(w), int(h))

	@property
	def area(self) -> int:
		return self.width * self.height

	@property
	def perimeter(self) -> int:
		return 2 * self.width + 2 * self.height

	def __str__(self) -> str:
		char = "* "
		space = "  "
		result = char * self.width + "\n"
		if self.height > 2:
			for i in range(self.height - 2):
				result += char
				if self.width > 2:
					result += space * (self.width - 2)
				if self.width >= 2:
					result += char
				result += "\n"
			result += char * self.width + "\n"
		return "\n".join(
				f"{k}: {v}" for k, v in {
						"Area":      self.area,
						"Perimeter": self.perimeter
				}.items()
		) + "\n" + result


def main():
	run = "y"
	while run == "y":
		rect = Rectangle.ask()
		print(rect)
		run = "?"
		while run not in ("y", "n"):
			run = input("Continue? (y/n)").lower()


if __name__ == '__main__':
	main()
