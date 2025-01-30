COUNTRIES = dict()
QUIT = False
COMMANDS = dict()

def pre_populate():
	COUNTRIES.clear()
	COUNTRIES["usa"] = "United States of America"
	COUNTRIES["ger"] = "Germany"
	COUNTRIES["jap"] = "Japan"

def list_countries():
	for code, country in COUNTRIES.items():
		print(f"{code}:\t{country}")

def add_country():
	while True:
		choice = input("Enter country code:\t").strip()
		if choice:
			if choice in COUNTRIES:
				print("This country code already exists!")
				continue

			name = input("Enter country name:\t")
			print("Country added")
			COUNTRIES[choice] = name
			return
		print("Invalid code, try again.")

def delete_country():
	if not COUNTRIES:
		print("There are no countries to delete!")
		return

	choice = input("Enter country code:\t")
	if choice not in COUNTRIES:
		print("That is not a valid country code.")
		return

	print(f"{COUNTRIES.pop(choice)} was deleted.")


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
	make_command("list", list_countries, "List all countries.")
	make_command("add", add_country, "Add a country.")
	make_command("del", delete_country, "Delete a country by code.")
	make_command("exit", stop, "Exit program.")
	pre_populate()


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
