MOVIES = list()
QUIT = False
COMMANDS = dict()


def load_movies():
	MOVIES.clear()
	with open("movies.txt", "r") as fl:
		for movie in fl.read().split("\n"):
			MOVIES.append(movie)

def update_movies():
	with open("movies.txt", "w") as fl:
		fl.write("\n".join(MOVIES))

def ask_number(prompt: str, lower: int, upper: int) -> int:
	while True:
		answer = input(prompt + ":\t")

		if not answer.isdigit():
			print("That is not a valid number")
			continue

		answer = int(answer)

		if answer < lower or answer > upper:
			print(f"Number must be between {lower} and {upper} (inclusive)")
			continue

		return answer

def list_movies():
	for i, movie in enumerate(MOVIES):
		print(f"{i+1}. {movie}")

def add_movie():
	while True:
		choice = input("Enter movie name: ").strip()
		if choice:
			print("Movie added")
			if choice in MOVIES:
				print("This movie already exists!")
				continue
			MOVIES.append(choice)
			update_movies()
			return
		print("Invalid name, try again.")

def delete_movie():
	if not MOVIES:
		print("There are no movies to delete!")
		return

	choice: int = ask_number("Enter index", 1, len(MOVIES)) - 1
	print(f"{MOVIES.pop(choice)} was removed.")
	update_movies()

def stop():
	global QUIT
	QUIT = True
	print("Bye bye!")

class Command:
	def __init__(self, callback, desc):
		self.callback = callback
		self.desc = desc

	def __call__(self):
		self.callback()

def make_command(keyword: str, callback, desc: str):
	COMMANDS[keyword.lower()] = Command(callback, desc)


def main():
	make_command("list", list_movies, "List all movies.")
	make_command("add", add_movie, "Add a movie.")
	make_command("del", delete_movie, "Delete a movie by ID.")
	make_command("exit", stop, "Exit program.")
	load_movies()

	while not QUIT:
		print("=====Commands=====")
		print("\n".join([f"{k}: {v.desc}" for k, v in COMMANDS.items()]) + "\n")
		command = input("Enter command:\t").strip().lower()

		if command not in COMMANDS:
			print("Invalid command, try again.")
			continue
		COMMANDS[command]()


if __name__ == '__main__':
	main()
