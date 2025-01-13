import random


def game(force_goal = -1):
	print("Im thinking of a number between 1 and 100 (inclusive)...")
	goal = random.randint(1, 100) if force_goal == -1 else force_goal
	answer_number = -1

	while answer_number != goal:
		answer = input("Enter guess:\t")
		if not answer.isdigit():
			print(f"{answer} not a number!")
			continue
		answer_number = int(answer)
		if answer_number > goal:
			print(f"{answer_number} is too high!")
		elif answer_number < goal:
			print(f"{answer_number} is too low!")
		else:
			print(f"You got it!!! {goal} was the correct answer.")


def choice(prompt, a, b):
	c = input(prompt + ":\t").lower()
	while c != a and c != b:
		print(f"Your choice must be [{a}] or [{b}].")
		c = input(prompt + ":\t").lower()
	return c


def main(force_goal = -1):
	play = "y"
	while play != "n":
		game(force_goal = force_goal)
		play = choice("Play again?", "y", "n")
	print("Thanks for playing!")


if __name__ == '__main__':
	main(12)
