import os
import json
import keyboard
from termcolor import colored
from pathlib import Path
from enum import IntEnum

class Script(IntEnum):
	BEGINING = 1
	END = 100

##----------------------------------------------------------------------------------------------------------------------
class Page:
	def __init__(self, number, title, text, actions, default_next_page = 0):
		self._number = number
		self._title = title
		self._text = text
		self._actions = actions
		self._next_page = default_next_page

	def _print_green(self, text):
		print(colored(text, "light_green"))

	def _print_blue(self, text):
		print(colored(text, "light_blue"))

	def _print_red(self, text):
		print(colored(text, "light_red"))

	def _print_on_green(self, text):
		print(colored(text, "white", "on_light_green"))

	def _print_on_red(self, text):
		print(colored(text, "white", "on_light_red"))

	def _print_title_and_text(self):
		os.system('cls')
		self._print_blue("[STRONA " + str(self._number) + "]")
		title = self._title.strip()
		if len(title) > 0:
			self._print_on_green("\n" + self._title)
		self._print_green(self._text)

	def _print_actions(self):
		for i in range(len(self._actions)):
			self._print_blue("[" + str(i + 1) + "] " + self._actions[i][0] + " ---> " + str(self._actions[i][1]) + " |")

	def _choose_action_and_next_page(self):
		number = 0
		while (number == 0):
			try:
				number = int(input(colored("Twoja decyzja:", "white", "on_light_blue") + " "))
			except ValueError:
				self._print_on_red("Wprowadzono nieprawidłową wartość!")
			else:
				if (number < 1) or (number > len(self._actions)):
					number = 0
					self._print_on_red("Taka opcja nie jest dostepna. Wybierz ponownie.")
				else:
					self._next_page = self._actions[number - 1][1]
		return number

	def _press_enter_key(self):
		input("\nNaciśnij ENTER, aby kontynuować podróż...")

	def read_and_play_the_page(self):
		end = False
		self._print_title_and_text()
		self._print_actions()
		if self._number == Script.END:
			end = True
			next_page = self._next_page

		else:
			if (len(self._actions) > 0):
				self._choose_action_and_next_page()
			else:
				self._press_enter_key()
		return self._next_page, end

	def get_number(self):
		return self._number

##----------------------------------------------------------------------------------------------------------------------
class Book:
	def __init__(self):
		self._current_page = Script.BEGINING
		self._end = False
		self._pages = []
		self._prepare_book()
		print("LICZBA STRON = " + str(len(self._pages)))

	def _prepare_book(self):
		data = self._read_file()

		if (len(data) == 0):
			print("Naciśnij dowolny klawisz, aby zakończyć")
			keyboard.read_key()
			quit()

		for page in data:
			number = page['NUMBER']
			title = page["TITLE"]
			text = page['TEXT']
			actions = page['ACTIONS']
			next = page['NEXT']
			self._pages.append(Page(number, title, text, actions, next))

	def _read_file(self):
		path_to_file = Path(__file__).parent.absolute() / "book.json"
		data = []
		try:
			with open(path_to_file, 'r', encoding='utf-8') as book_file:
				data = json.load(book_file)
		except FileNotFoundError:
			print(colored("BŁĄD: Brak pliku z treścią przygody!", "light_yellow", "on_light_red"))
		except json.JSONDecodeError:
			print(colored("BŁĄD: Nie udało się skonwertować pliku (JSON) z treścią!",
			              "light_yellow", "on_light_red"))
		return data

	def read_and_play(self):
		while (self._end == False):
			index = self._find_page(self._current_page)
			if (index > -1):
				self._current_page, self._end = self._pages[index].read_and_play_the_page()
			else:
				self._end = True
				print(colored("KONIEC - ktoś wyrwał tę stronę!", "light_yellow", "on_light_red"))
		quit()

	def _find_page(self, number):
		index = -1
		i = 0
		while (i < len(self._pages)) and (index == -1):
			if (self._pages[i].get_number() == number):
				index = i
			else:
				i += 1
		return index

## BEGIN ##-------------------------------------------------------------------------------------------------------------

book = Book()
book.read_and_play()

## END ##---------------------------------------------------------------------------------------------------------------