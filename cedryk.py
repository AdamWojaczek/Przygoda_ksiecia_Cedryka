import os
import json
import textwrap
from termcolor import colored
from enum import IntEnum
from enum import StrEnum
#from pathlib import Path

##----------------------------------------------------------------------------------------------------------------------

class Script(IntEnum):
	BEGINING = 1
	END = 100

class Color(StrEnum):
	CLEAR = ""
	RED = "light_red"
	GREEN = "light_green"
	BLUE = "light_blue"
	YELLOW = "light_yellow"
	WHITE = "white"
	BLACK = "black"

class Align(IntEnum):
	LEFT = 0
	CENTER = 1
	RIGHT = 2

##----------------------------------------------------------------------------------------------------------------------
class Page:
	def __init__(self, number, title, text, actions, default_next_page):
		self._number = number
		self._title = title
		self._text = text
		self._actions = actions
		self._default_next_page = default_next_page

	def _print(self, text, color = Color.GREEN, bgcolor = Color.CLEAR, align = Align.LEFT):
		page_width = os.get_terminal_size().columns
		match align:
			case Align.RIGHT:
				align_tag = '>'
			case Align.CENTER:
				align_tag = '^'
			case Align.LEFT | _:
				align_tag = '<'
		#wrapped = textwrap.fill(text, width=page_width, replace_whitespace=False)
		wrapped = "\n".join([textwrap.fill(line, width=page_width, replace_whitespace=False) for line in text.splitlines()])
		text_out = f"{wrapped:{align_tag}{page_width}}"
		if bgcolor == Color.CLEAR:
			print(colored(text_out, color))
		else:
			print(colored(text_out, color, "on_" + bgcolor))

	def _print_story(self):
		os.system('cls')
		self._print("[STRONA " + str(self._number) + "]", Color.YELLOW, Color.CLEAR, Align.RIGHT)
		title = self._title.strip()
		if len(title) > 0:
			self._print(self._title, Color.WHITE, Color.BLUE, Align.CENTER)
		self._print(self._text, Color.GREEN)

	def _print_actions(self):
		for i in range(len(self._actions)):
			self._print("[" + str(i + 1) + "] " + self._actions[i][0] + "   --->   str. " + str(self._actions[i][1]),
			            Color.BLUE)

	def _choose_action_and_next_page(self):
		next_page = self._default_next_page
		action_number = 0
		while (action_number == 0):
			try:
				action_number = int(input(colored("Twoja decyzja:", Color.WHITE, "on_" + Color.BLUE) + " "))
			except ValueError:
				action_number = 0
				self._print("Wprowadzono nieprawidłową wartość!", Color.WHITE, Color.RED)
			else:
				if (action_number > 0) and (action_number <= len(self._actions)):
					next_page = self._actions[action_number - 1][1]
				else:
					action_number = 0
					self._print("Taka akcja nie jest dostępna! Wybierz ponownie.", Color.YELLOW, Color.RED)
		return next_page

	def _press_enter_key(self):
		input("\nNaciśnij ENTER, aby kontynuować podróż...")

	def read_and_play_the_page(self):
		self._print_story()
		self._print_actions()
		if self._number == Script.END:
			next_page = Script.END
			end = True
		else:
			if (len(self._actions) > 0):
				next_page = self._choose_action_and_next_page()
			else:
				next_page = self._default_next_page
				self._press_enter_key()
			end = False
		return next_page, end

	def get_number(self):
		return self._number

##----------------------------------------------------------------------------------------------------------------------
class Book:
	def __init__(self):
		self._current_page = Script.BEGINING
		self._end = False
		self._pages = []
		self._prepare_book()

	def _prepare_book(self):
		book_data = self._read_file()
		if (len(book_data) > 0):
			for page in book_data:
				number = page['NUMBER']
				title = page["TITLE"]
				text = page['TEXT']
				actions = page['ACTIONS']
				next = page['NEXT']
				self._pages.append(Page(number, title, text, actions, next))
			print("LICZBA STRON KSIĄŻKI = " + str(len(self._pages)))
		else:
			print(colored("Książka z grą paragrafową 'Przygoda księcia Cedryka' jest pusta!", Color.YELLOW))
			self._end = True

	def _read_file(self):
		book_data = []
		#path_to_file = Path(__file__).parent.absolute() / "book.json"
		path_to_file = "book.json"
		try:
			with open(path_to_file, 'r', encoding='utf-8') as book_file:
				book_data = json.load(book_file)
		except FileNotFoundError:
			print(colored("BŁĄD: Brak pliku z treścią przygody!", Color.YELLOW, Color.RED))
		except json.JSONDecodeError:
			print(colored("BŁĄD: Nie udało się skonwertować pliku (JSON) z treścią!", Color.YELLOW, Color.RED))
		return book_data

	def _find_page(self, number):
		index = -1
		i = 0
		while (i < len(self._pages)) and (index == -1):
			if (self._pages[i].get_number() == number):
				index = i
			else:
				i += 1
		return index

	def set_page(self, page):
		self._current_page = page

	def read_and_play(self):
		while (self._end == False):
			index = self._find_page(self._current_page)
			if (index > -1):
				self._current_page, self._end = self._pages[index].read_and_play_the_page()
			else:
				self._end = True
				print(colored("KONIEC - ktoś wyrwał stronę!", Color.YELLOW, "on_" + Color.RED))
		input("\nNaciśnij ENTER, aby zakończyć...\n")
		quit()

## BEGIN ##-------------------------------------------------------------------------------------------------------------

book = Book()
book.read_and_play()

## END ##---------------------------------------------------------------------------------------------------------------