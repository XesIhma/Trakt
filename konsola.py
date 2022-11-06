from colorama import init, Fore, Back, Style
import math
import os
import msvcrt
import time
import keyboard
import textwrap 
import random

#czasami wyświetlało kod koloru zamiast koloru bez tej linijki
init(convert=True) 

f_reset = Fore.RESET
b_reset = Back.RESET
c_reset = Fore.RESET + Back.RESET

f_blue = Fore.BLUE
f_cyan = Fore.CYAN
f_green = Fore.GREEN
f_magenta = Fore.MAGENTA
f_red = Fore.RED
f_white = Fore.WHITE
f_yellow = Fore.YELLOW
f_lblack = Fore.LIGHTBLACK_EX
f_lblue = Fore.LIGHTBLUE_EX
f_lcyan = Fore.LIGHTCYAN_EX
f_lgreen = Fore.LIGHTGREEN_EX
f_lmagenta = Fore.LIGHTMAGENTA_EX
f_lred = Fore.LIGHTRED_EX
f_lwhite = Fore.LIGHTWHITE_EX
f_lyellow = Fore.LIGHTYELLOW_EX

b_blue = Back.BLUE
b_cyan = Back.CYAN
b_green = Back.GREEN
b_magenta = Back.MAGENTA
b_red = Back.RED
b_white = Back.WHITE
b_yellow = Back.YELLOW
b_lblack = Back.LIGHTBLACK_EX
b_lblue = Back.LIGHTBLUE_EX
b_lcyan = Back.LIGHTCYAN_EX
b_lgreen = Back.LIGHTGREEN_EX
b_lmagenta = Back.LIGHTMAGENTA_EX
b_lred = Back.LIGHTRED_EX
b_lwhite = Back.LIGHTWHITE_EX
b_lyellow = Back.LIGHTYELLOW_EX


class Konsola:
	def __init__(self):
		pass
	@classmethod
	def print(cls, text, f=f_reset, b=b_reset, lineEnd="\n"):
		color = cls.colorParser(f, b)

		if isinstance(text,int):
			text = str(text)

		print(color + text + c_reset, end=lineEnd)
		
	@classmethod
	def wrap(cls, textToWrap, f=f_reset, b=b_reset):
		wrapper = textwrap.TextWrapper(width=100)
		word_list = wrapper.wrap(text=textToWrap)
		for element in word_list: 
			cls.print(element, f, b)
			#time.sleep(0.1)

	@classmethod
	def landing(cls):
		os.system('cls')
		print("Trakt v. 0.3.0")
		print("Witaj")
		print("---------------")
		print("[1] Nowa gra")
		print("[2] Wczytaj grę")
		print("[3] Poradnik")
		print("[4] Arena")
		print("[5] Wyjdź z gry")
		print(" > ", end="")


	@classmethod
	def prompt(cls, hero, inp=True):
		if inp:colorr = f_lgreen
		else: colorr = f_lmagenta
		print(colorr+"<HP: {}/{} Stamina: {}/{}>".format(math.ceil(hero.param["hp"]), hero.param["hp_max"], math.ceil(hero.param["stamina"]), math.ceil(hero.param["stamina_aviable"]))+c_reset, end="")
		if inp:
			decision = input().lower()
			command = decision.split()
			return command
		else:
			timeout = 1
			startTime = time.time()
			inputText = ''
			enter = False
			while True:
				if msvcrt.kbhit():
					byte_arr = msvcrt.getche()
					if ord(byte_arr) == 13: # enter_key
						enter=True
						break
					elif ord(byte_arr) >= 32: #space_char
						inputText += "".join(map(chr,byte_arr))
						startTime = time.time()
			
				if (time.time() - startTime) > timeout:break
					
			print('')  # needed to move to next line
			if len(inputText) > 0:
				return inputText
			else:
				return 0
		
	@classmethod
	def clear(cls):
		os.system('cls')
	
	@classmethod
	def printRandom(cls, komunikat):
		print(random.choice(komunikat))
	@classmethod
	def hr(cls):
		print("---------------")
	@classmethod
	def sleep(cls, long):
		time.sleep(long)
	@classmethod
	def compas(cls, s, world, mob):
		mobX = mob.x + mob.currentLocation.x
		mobY = mob.y + mob.currentLocation.y
		mobZ = mob.z + (world.groundLevel - mob.currentLocation.groundLevel)
		#nw n ne up
		#w    e	 down
		#sw s se
		try: 
			print(cls.surfColor(world.sSurf[mobX-1][mobY-1][mobZ]), end="") if s.northwest else print(Fore.BLACK + Style.BRIGHT, end="")
			print("nw" + Style.RESET_ALL, end="")
			print(cls.surfColor(world.sSurf[mobX][mobY-1][mobZ]), end="") if s.north else print(Fore.BLACK + Style.BRIGHT, end="")
			print(" n " + Style.RESET_ALL, end="")
			print(cls.surfColor(world.sSurf[mobX+1][mobY-1][mobZ]), end="") if s.northeast else print(Fore.BLACK + Style.BRIGHT, end="")
		except: pass
		try:
			print("ne" + Style.RESET_ALL, end="")
			print(" ", end="")
		except IndexError: 
			print("ne" + Style.RESET_ALL, end="")
			print(" ", end="")
		try:
			print(cls.surfColor(world.sSurf[mobX][mobY][mobZ+1]), end="") if s.up else print(Fore.BLACK + Style.BRIGHT, end="")
			print("up" + Style.RESET_ALL)
			print(cls.surfColor(world.sSurf[mobX-1][mobY][mobZ]), end="") if s.west else print(Fore.BLACK + Style.BRIGHT, end="")
			print("w " + Style.RESET_ALL, end="")
			print("   ", end="")
			print(cls.surfColor(world.sSurf[mobX+1][mobY][mobZ]), end="") if s.east else print(Fore.BLACK + Style.BRIGHT, end="")
		except: pass
		try:
			print(" e" + Style.RESET_ALL, end="")
			print(" ", end="")
		except IndexError: 
			print("e" + Style.RESET_ALL, end="")
			print(" ", end="")
		try:
			print(cls.surfColor(world.sSurf[mobX][mobY][mobZ-1]), end="") if s.down else print(Fore.BLACK + Style.BRIGHT, end="")
			print("down" + Style.RESET_ALL)
		except: pass
		try:
			print(cls.surfColor(world.sSurf[mobX-1][mobY+1][mobZ]), end="") if s.southwest else print(Fore.BLACK + Style.BRIGHT, end="")
			print("sw" + Style.RESET_ALL, end="")
		except IndexError: 
			print("sw" + Style.RESET_ALL, end="")
			print(" ", end="")
		try:
			print(cls.surfColor(world.sSurf[mobX][mobY+1][mobZ]), end="") if s.south else print(Fore.BLACK + Style.BRIGHT, end="")
			print(" s " + Style.RESET_ALL, end="")
		except IndexError: 
			print("s" + Style.RESET_ALL, end="")
			print(" ", end="")
		try:
			print(cls.surfColor(world.sSurf[mobX+1][mobY+1][mobZ]), end="") if s.southeast else print(Fore.BLACK + Style.BRIGHT, end="")
			print("se" + Style.RESET_ALL)
		except IndexError: 
			print("se" + Style.RESET_ALL)
		
	@classmethod
	def colorParser(cls, f, b):
		if f != "reset":
			if f == "blue":
				color = f_blue
			elif f == "cyan":
				color = f_cyan
			elif f == "green":
				color = f_green
			elif f == "magenta":
				color = f_magenta
			elif f == "red":
				color = f_red
			elif f == "white":
				color = f_white
			elif f == "yellow":
				color = f_yellow
			elif f == "lblack":
				color = f_lblack	
			elif f == "lblue":
				color = f_lblue
			elif f == "lcyan":
				color = f_lcyan
			elif f == "lgreen":
				color = f_lgreen
			elif f == "lmagenta":
				color = f_lmagenta
			elif f == "lred":
				color = f_lred
			elif f == "lwhite":
				color = f_lwhite
			elif f == "lyellow":
				color = f_lyellow
			else: 
				color = Fore.RESET
		else: 
			color = Fore.RESET
		if b != "reset":
			if b == "blue":
				color += b_blue
			elif b == "cyan":
				color += b_cyan
			elif b == "green":
				color += b_green
			elif b == "magenta":
				color += b_magenta
			elif b == "red":
				color += b_red
			elif b == "white":
				color += b_white
			elif b == "yellow":
				color += b_yellow
			elif b == "lblack":
				color += b_lblack	
			elif b == "lblue":
				color += b_lblue
			elif b == "lcyan":
				color += b_lcyan
			elif b == "lgreen":
				color += b_lgreen
			elif b == "lmagenta":
				color += b_lmagenta
			elif b == "lred":
				color += b_lred
			elif b == "lwhite":
				color += b_lwhite
			elif b == "lyellow":
				color += b_lyellow
			else: 
				color += Back.RESET
		else: 
			color += Back.RESET
		return color

	@classmethod
	def surfColor(cls, surf):
		# 1 droga
		# 2 pokój
		# 3 łąka
		# 4 las
		# 5 góry
		# 6 bagna
		# 7 rzeka
		# 8 ocean
		# 9 korytarz
		if surf == 1:
			return  Back.LIGHTYELLOW_EX + Fore.BLACK
		elif surf == 2:
			return Back.RED + Fore.LIGHTWHITE_EX
		elif surf == 9:
			return Back.LIGHTRED_EX  + Fore.BLACK
		elif surf == 3:
			return Back.LIGHTGREEN_EX + Fore.BLACK
		elif surf == 4:
			return Back.GREEN + Fore.WHITE
		elif surf == 5:
			return Back.LIGHTBLACK_EX + Fore.BLACK
		elif surf == 6:
			return Back.CYAN + Fore.LIGHTWHITE_EX
		elif surf == 7:
			return Back.LIGHTCYAN_EX + Fore.BLACK
		elif surf == 8:
			return Back.BLUE + Fore.LIGHTWHITE_EX
	
	@classmethod
	def help(cls):
		cls.print("DOSTĘPNE KOMENDY: ", "white")
		cls.print("> KIERUNKI: ", "white")
		cls.print("    north     | n  | 8 - przemieść się na północ", "lwhite")
		cls.print("    east      | e  | 6 - przemieść się na wschód", "lwhite")
		cls.print("    south     | s  | 2 - przemieść się na południe", "lwhite")
		cls.print("    west      | w  | 4 - przemieść się na zachód", "lwhite")
		cls.print("    northeast | ne | 9 - przemieść się na północny wschód", "lwhite")
		cls.print("    southeast | se | 3 - przemieść się na południowy wschód", "lwhite")
		cls.print("    southwest | sw | 1 - przemieść się na południowy zachód", "lwhite")
		cls.print("    northwest | nw | 7 - przemieść się na północny zachód", "lwhite")
		cls.print("    up        | u  | 5 - przemieść się w górę", "lwhite")
		cls.print("    down      | d  | 0 - przemieść się w dół", "lwhite")
		cls.print("> PRZEDMIOTY: ", "white")
		cls.print("    podnieś [nazwa przedmiotu] - podnieś przedmiot i umieść w ekwipunku", "lwhite")
		cls.print("    upuść [nazwa przedmiotu] - usuń przedmiot z ekwipunku", "lwhite")
		cls.print("    ? [nazwa przedmiotu] - wyświetl możliwe działania", "lwhite")
		cls.print("    zobacz [nazwa przedmiotu] - wyświetl opis przedmiotu", "lwhite")
		cls.print("    zjedz [nazwa przedmiotu] - zjedz, jeśli to jest jedzenie", "lwhite")
		cls.print("    wypij [nazwa przedmiotu] - wypij, jeśli to jest napój lub eliksir", "lwhite")
		cls.print("    użyj [nazwa przedmiotu] - użyj, jeśli to lekarstwo", "lwhite")
		cls.print("    dobądź [nazwa przedmiotu] - weź do ręki, jeśli to miecz lub tarcza", "lwhite")
		cls.print("    chwyć [nazwa przedmiotu] - weź do ręki, jeśli to narzędzie", "lwhite")
		cls.print("    schowaj [nazwa przedmiotu] - odłóż, jeśli to miecz lub tarcza", "lwhite")
		cls.print("    zaloz [nazwa przedmiotu] - załóż, jeśli to zbroja lub biżuteria", "lwhite")
		cls.print("    ubierz [nazwa przedmiotu] - ubierz, jeśli ubranie", "lwhite")
		cls.print("    zdejmij [nazwa przedmiotu] - zdejmij, jeśli to zbroja, ubranie lub biżuteria", "lwhite")
		cls.print("> NPC: ", "white")
		cls.print("    zabij [nazwa npc] - rozpocznij walkę", "lwhite")
		cls.print("> DANE: ", "white")
		cls.print("    ekwipunek - pokaż zawartość ekwipunku", "lwhite")
		cls.print("    wyposazenie - pokaż to co masz aktualnie na sobie (broń, pancerz itd)", "lwhite")
		cls.print("    statystyki - pokaż statystyki gracza", "lwhite")
		cls.print("    czas - wyświetl aktualny czas w grze", "lwhite")
		cls.print("> FUNCKJE GRY: ", "white")
		cls.print("    save - zapisz grę", "lwhite")
		cls.print("    exit - zakończ grę", "lwhite")
	@classmethod
	def map(cls, hero):
		loc = hero.currentLocation
		os.system('CLS')
		for y in range(loc.sizeY):
			for x in range(loc.sizeX):
				if hero.x == x and hero.y == y:
					print(Back.MAGENTA + Style.BRIGHT, end="")
				else:
					print(cls.surfColor(loc.s[x][y][loc.groundLevel].surface), end="")
				print(loc.s[x][y][loc.groundLevel].surface, end="")
				print(" ", end="")
			print("")
		print(Style.RESET_ALL, end='')
	@classmethod
	def nameConvert(cls, command):
		name = ""
		if len(command) == 1:
			return 0
		elif len(command) == 2:
			name = command[1]
		elif len(command) > 2:
			for x in range(len(command)-1):
				name = name+command[x+1]+' '
			name = name[:-1] #usuwa ostatni znak czyli spacje
		return name
	@classmethod
	def parameters(cls, mob):
		print("HP:         "+Style.BRIGHT+str(mob.param["hp"])+"/"+str(mob.param["hp_max"])+Style.RESET_ALL)
		print("Stamina:    "+Style.BRIGHT+str(math.ceil(mob.param["stamina"]))+"/"+str(math.ceil(mob.param["stamina_aviable"]))+Style.RESET_ALL)
		print("Mana:       "+Style.BRIGHT+str(mob.param["mana"])+"/"+str(mob.param["mana_max"])+Style.RESET_ALL)
		print("Sytość:     "+Style.BRIGHT+str(mob.param["nourish"])+"/"+str(mob.param["nourish_max"])+Style.RESET_ALL)
		print("")
		print("Siła: "+Style.BRIGHT+str(mob.stat["strength"])+Style.RESET_ALL)
		print("Zręczność: "+Style.BRIGHT+str(mob.stat["agility"])+Style.RESET_ALL)
		print("Szybkość: "+Style.BRIGHT+str(mob.stat["speed"])+Style.RESET_ALL)
		print("Spostrzegawczość: "+Style.BRIGHT+str(mob.stat["perceptivity"])+Style.RESET_ALL)
		print("Widoczność: "+Style.BRIGHT+str(mob.stat["visibility"])+Style.RESET_ALL)
	@classmethod
	def edit(cls, hero, what, exit):
		if what == "n":
			print("Wprowadź nazwę: ", end="")
			keyboard.write(hero.currentLocation.s[hero.x][hero.y][hero.z].name)
			new_name = input()
			print("================")
			print(new_name)
			print("Czy chcesz zapisać nową nazwę? (Y/N)")
			is_it_ok = input()
			if is_it_ok in ("Y", "y"):
				hero.currentLocation.s[hero.x][hero.y][hero.z].name = new_name
		elif what == "d":
			print("Wprowadź opis: ", end="")
			keyboard.write(hero.currentLocation.s[hero.x][hero.y][hero.z].description)
			new_description = input()
			print("================")
			print(new_description)
			print("Czy chcesz zapisać nowy opis? (Y/N)")
			is_it_ok = input()
			if is_it_ok in ("Y", "y"):
				hero.currentLocation.s[hero.x][hero.y][hero.z].description = new_description
		elif what == "e":
			sq = hero.currentLocation.s[hero.x][hero.y][hero.z]
			if exit == "n": sq.north  = not sq.north 
			elif exit == "ne": sq.northeast = not sq.northeast
			elif exit == "e": sq.east = not sq.east
			elif exit == "se": sq.southeast = not sq.southeast
			elif exit == "s": sq.south = not sq.south
			elif exit == "sw": sq.southwest = not sq.southwest
			elif exit == "w": sq.west = not sq.west
			elif exit == "nw": sq.northwest = not sq.northwest
			elif exit == "u": sq.up= not sq.up
			elif exit == "d": sq.down= not sq.down
			elif exit == "0":
				sq.north = False
				sq.northeast = False
				sq.east = False
				sq.southeast = False
				sq.south = False
				sq.southwest = False
				sq.west = False
				sq.northwest = False
				sq.up = False
				sq.down = False
			elif exit == "1":
				sq.north = True
				sq.northeast = True
				sq.east = True
				sq.southeast = True
				sq.south = True
				sq.southwest = True
				sq.west = True
				sq.northwest = True
				sq.up = True
				sq.down = True
		elif what == "s":
			exit = int(exit)
			if exit in (1,2,3,4,5,6,7,8,9):
				print(hero.currentLocation.s[hero.x][hero.y][hero.z].surface)
				hero.currentLocation.s[hero.x][hero.y][hero.z].surface = exit
				print(hero.currentLocation.s[hero.x][hero.y][hero.z].surface)