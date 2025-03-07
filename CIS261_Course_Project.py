import os
import json


class Login:
	def __init__(self, userid: str, password: str, auth: str):
		self.userid: str = userid
		self.password: str = password
		self.auth: str = auth.capitalize()

	def __eq__(self, other: "Login"):
		#prevent normal users from logging in as admin
		if other.is_admin and not self.is_admin:
			return False
		return self.userid == other.userid and self.password == other.password

	@property
	def is_admin(self) -> bool:
		return self.auth == "Admin"

	@property
	def as_list(self) -> list:
		return [self.userid, self.password, self.auth]

	@classmethod
	def from_list(cls, lst: list):
		if len(lst) != 3:
			raise Exception(f"Parse error: Invalid user")
		return cls(*lst)

	def exists(self, userid_only = False):
		with open("users.json", "r") as fl:
			users = [Login.from_list(u) for u in json.load(fl)]

		if userid_only:
			return any(self.userid == user.userid for user in users)
		return any(self == user for user in users)

	@classmethod
	def get_all(cls) -> list["Login"]:
		with open("users.json", "r") as fl:
			users = [Login.from_list(u) for u in json.load(fl)]
		return users

	@classmethod
	def ask(cls, create = False):
		result = None
		while result is None:
			userid = ""
			password = ""
			auth = ""
			while not userid: userid = input("Enter userID:\t")
			while not password: password = input("Enter password:\t")
			while auth not in ("user", "admin"): auth = input("Login type (User/Admin):\t").lower()
			result = cls(userid, password, auth)
			exists = result.exists(create)
			if exists == create:
				if create:
					print("Error: User already exists! Try again...")
				else:
					print("Error: User does not exist! Try again...")
				result = None

		if create:
			with open("users.json", "r") as fl:
				users = json.load(fl) + [result.as_list]

			with open("users.json", "w") as fl:
				json.dump(users, fl)

		return result


ACTIVE_EMPLOYEE = ""
data = dict()


def load():
	if not os.path.isfile("data.json"):
		return
	global data
	with open("data.json", "r") as fl:
		data = json.load(fl)


def save():
	with open("data.json", "w") as fl:
		json.dump(data, fl)


def employee_name(name: str):
	print(f"Now entering data for {name}")
	data[name] = dict()
	global ACTIVE_EMPLOYEE
	ACTIVE_EMPLOYEE = name
	return name


def total_hours(hours: str):
	if not ACTIVE_EMPLOYEE:
		print("NO ACTIVE EMPLOYEE, USE NAME COMMAND!")
		return 0
	if not hours.isnumeric():
		print("INVALID HOUR AMOUNT")
		return 0
	print(f"Hours set to {hours}")
	data[ACTIVE_EMPLOYEE]["hours"] = int(hours)
	return data[ACTIVE_EMPLOYEE]["hours"]


def rate(hourly_rate: str):
	if not ACTIVE_EMPLOYEE:
		print("NO ACTIVE EMPLOYEE, USE NAME COMMAND!")
		return 0
	if not hourly_rate.isnumeric():
		print("INVALID RATE AMOUNT")
		return 0
	print(f"Rate set to {hourly_rate}")
	data[ACTIVE_EMPLOYEE]["rate"] = int(hourly_rate)
	return data[ACTIVE_EMPLOYEE]["rate"]


def taxes(tax: str):
	if not ACTIVE_EMPLOYEE:
		print("NO ACTIVE EMPLOYEE, USE NAME COMMAND!")
		return 0.0
	try:
		data[ACTIVE_EMPLOYEE]["tax"] = float(tax)
		print(f"Tax rate set to {tax}")
		return data[ACTIVE_EMPLOYEE]["tax"]
	except ValueError:
		print("INVALID TAX AMOUNT")
	return 0.0


def everything_input(hours: str, hourly_rate: str, tax: str):
	if not hours.isnumeric() or not hourly_rate.isnumeric():
		print("INVALID ARGUMENT(S)")
		return 0

	hours = int(hours)
	hourly_rate = int(hourly_rate)

	try:
		tax = float(tax)
	except ValueError:
		print("INVALID ARGUMENT(S)")
		return 0.0

	gross = hours * hourly_rate
	net = hours * hourly_rate * (1.0 - tax)
	print(f"Gross pay: {gross}\nNet pay: {net}")


def display(conclusion = False):
	if not ACTIVE_EMPLOYEE:
		if not conclusion:
			print("NO ACTIVE EMPLOYEE!")
		return
	print(f"{ACTIVE_EMPLOYEE}:")
	print("\n".join(
			f"\t{k.capitalize()}: {v}" for k, v in data[ACTIVE_EMPLOYEE].items()
	))
	gross_pay = data[ACTIVE_EMPLOYEE].get("hours", 0.0) * data[ACTIVE_EMPLOYEE].get("rate", 0.0)
	tax = data[ACTIVE_EMPLOYEE].get("tax", 0.0)
	net_pay = (1.0 - tax) * gross_pay

	print("\n".join(
			f"\t{k}: {v}" for k, v in {
					"Gross pay": gross_pay,
					"Net pay":   net_pay
			}.items()
	))


def compare_dates(source: str, target: str):
	s_month, s_day, s_year = [int(x) for x in source.split("/")]
	t_month, t_day, t_year = [int(x) for x in target.split("/")]
	if t_year > s_year:
		return True
	if t_month > s_month:
		return True
	if t_day >= s_day:
		return True
	return False


def display_range():
	s_date = input("Enter from-date mm/dd/yyyy or 'All':\t").lower().replace(" ", "")
	if s_date == "all":
		s_date = "0/0/0"

	global ACTIVE_EMPLOYEE
	for k, v in data.items():
		if "start date" not in v or not compare_dates(s_date, v["start date"]):
			continue
		ACTIVE_EMPLOYEE = k
		display()


def count():
	print("\n".join(
			f"{k}: {v}" for k, v in {
					"Employees": len(data),
					"Hours":     sum(value.get("hours", 0) for value in data.values()),
					"Gross pay": sum(value.get("hours", 0) * value.get("rate", 0) for value in data.values()),
					"Taxes":     sum(
							value.get("hours", 0) * value.get("rate", 0) * value.get("tax", 0)
							for value in data.values()),
					"Net pay":   sum(
							value.get("hours", 0) * value.get("rate", 0) * (1.0 - value.get("tax", 0)) for value in
							data.values())
			}.items()
	))


def date_from(month_str: str, day_str: str, year_str: str):
	if not ACTIVE_EMPLOYEE:
		print("NO ACTIVE EMPLOYEE, USE NAME COMMAND!")
		return
	if not month_str.isnumeric() or not day_str.isnumeric() or not year_str.isnumeric():
		print("INVALID ARGUMENT(S)")
		return
	date = f"{month_str}/{day_str}/{year_str}"
	data[ACTIVE_EMPLOYEE]["start date"] = date
	print("Start date set to " + date)
	return date


def date_to(month_str: str, day_str: str, year_str: str):
	if not ACTIVE_EMPLOYEE:
		print("NO ACTIVE EMPLOYEE, USE NAME COMMAND!")
		return
	if not month_str.isnumeric() or not day_str.isnumeric() or not year_str.isnumeric():
		print("INVALID ARGUMENT(S)")
		return
	date = f"{month_str}/{day_str}/{year_str}"
	data[ACTIVE_EMPLOYEE]["end date"] = date
	print("End date set to " + date)
	return date


def create_user():
	Login.ask(True)
	print("User created!")


def display_users():
	for user in Login.get_all():
		print("\n\n".join([
				f"{k}: {v}" for k, v in {
						"Username": user.userid,
						"Password": user.password,
						"Auth":     user.auth,
				}.items()
		]))


def main():
	load()
	functions = {
			"name":        [1, employee_name, True],
			"hours":       [1, total_hours, True],
			"rate":        [1, rate, True],
			"tax":         [1, taxes, True],
			"calculator":  [3, everything_input, True],
			"display":     [0, display, False],
			"count":       [0, count, False],
			"start_date":  [3, date_from, True],
			"end_date":    [3, date_to, True],
			"create_user": [0, create_user, True]
	}

	user = Login.ask()

	while True:
		value = input("Enter Command:\t").strip()
		args = []
		if " " in value:
			value = value.split(" ")
			args = value[1:]
			value = value[0].lower()
		if value == "end":
			display(True)
			display_range()
			display_users()
			save()
			break
		elif value not in functions:
			print("INVALID COMMAND!")
		else:
			if functions[value][2] and not user.is_admin:
				print("This command requires admin authorization.")
				continue
			if len(args) != functions[value][0]:
				print(f"Command \"{value}\" takes exactly {functions[value][0]} arguments.")
				continue
			if functions[value][0]:
				functions[value][1](*args)
			else:
				functions[value][1]()


if __name__ == '__main__':
	main()
