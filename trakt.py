from world import World
from square import Square
from location import Location
from hero import Hero
from colorama import init, Fore, Back, Style
from item import Item, Consumable, Food, Drink, Heals, Elixir, Weapon, CloseRange, Ranged, Armor, Shield, Clothes, Tool, Jewellery, Machine, Vehicle, Container, Furniture, Heap
from game import Game, set_items, item_name_convert
from items_dict import all_items
import math
import json
import copy


init(convert=True)


print("Trakt v. 0.2.0")
print("Witaj")
print("---------------")
print("[1] Nowa gra")
print("[2] Wczytaj grę")
print("[3] Poradnik")
print("[4] Wyjdź z gry")

castle = None
hero = None

correct = False
while not correct:
	choice = input()
	if choice =="1":
		correct = True
		print("Nowa gra")
		print("---------------")
		game = Game()
		hero = Hero()
		game.hero = hero
		maps = ["initial/castle.json","initial/castle2.json","initial/castle3.json","initial/castle4.json","initial/castle5.json","initial/castle6.json",]
		world = World(maps)
		game.world = world
		game.items = set_items("initial/items.json", game.world)
		hero.current_location = game.world
		hero.current_location.show_location(hero.x,hero.y,hero.z)
	elif choice=="2":
		correct = True
		print("Wczytujesz grę")
		print("---------------")
	elif choice=="3":
		correct = True
		print("Tutorial")
		print("---------------")
	elif choice=="4":
		exit()
	else:
		print("Wprowadź poprawny wybór")


is_playing = True
while is_playing:
	print(Fore.LIGHTGREEN_EX+"<HP: {}/{} Stamina: {}/{}>".format(hero.param["hp"], hero.param["hp_max"], math.ceil(hero.param["stamina"]), math.ceil(hero.param["stamina_aviable"]))+Style.RESET_ALL, end="")
	decision = input().lower()
	command = decision.split()
	if len(command) == 0:
		print("Co chcesz zrobić?")
	elif command[0] == "north" or command[0] == "n" or command[0] == "a" or command[0] == "8":
		 game.player_travel(8)
	elif command[0] == "northeast" or command[0] == "ne" or command[0] == "9":
		game.player_travel(9)
	elif command[0] == "east" or command[0] == "e" or command[0] == "6":
		game.player_travel(6)
	elif command[0] == "southeast" or command[0] == "se" or command[0] == "3":
		game.player_travel(3)
	elif command[0] == "south" or command[0] == "s" or command[0] == "2":
		game.player_travel(2)
	elif command[0] == "southwest" or command[0] == "sw" or command[0] == "1":
		game.player_travel(1)
	elif command[0] == "west" or command[0] == "w" or command[0] == "4":
		game.player_travel(4)
	elif command[0] == "northwest" or command[0] == "nw" or command[0] == "7":
		game.player_travel(7)
	elif command[0] == "up" or command[0] == "u" or command[0] == "r" or command[0] == "5":
		game.player_travel(5)
	elif command[0] == "down" or command[0] == "d" or command[0] == "0":
		game.player_travel(0)
	elif command[0] == "exit" or command[0] == "end":
		is_playing = False
		exit()
	
	elif command[0] == "podnieś" or command[0] == "podnies" or  command[0] == "pick_up":
		that_item = game.find_item(command, True)
		if that_item:
			hero.pick_up(that_item)
			game.time_progress(5)
		else:
			print("Nie ma tu takiej rzeczy")

	elif command[0] == "upuść" or command[0] == "upusc" or  command[0] == "drop":
		item_name = item_name_convert(command)
		if hero.is_in_eq(item_name) == True:
			hero.drop(item_name)
			game.time_progress(5)
		else:
			print("Nie masz czegoś takiego")

	elif command[0] == "ekwipunek" or command[0] == "equip" or  command[0] == "ekw" or  command[0] == "eq":
		hero.show_equip()
	
	elif command[0] == "wyposarzenie" or command[0] == "outfit":
		if hero.right_hand:
			print("W prawej ręce trzymasz  "+hero.right_hand.name)
		if hero.left_hand:
			print("W lewej ręce trzymasz   "+hero.left_hand.name)
		if hero.head:
			print("Na głowie      "+hero.head.name)
		if hero.torso:
			print("Na torsie      "+hero.torso.name)
		if hero.hands:
			print("Na dłoniach    "+hero.hands.name)
		if hero.legs:
			print("Na nogach      "+hero.legs.name)
		if hero.feet:
			print("Na stopach     "+hero.feet.name)

	elif command[0] == "info" or command[0] == "?":
		that_item = game.find_item(command, True)
		if that_item:
			that_item.possible_actions()
		else:
			print("Nie ma tu takiej rzeczy")

	elif command[0] == "zobacz" or command[0] == "see":
		that_item = game.find_item(command, True)
		if that_item:
			that_item.see()
		else:
			print("Nie ma tu takiej rzeczy")

	elif command[0] == "zjedz" or command[0] == "eat":
		if game.find_item(command, True):
			that_item = game.find_item(command, True)
			if isinstance(that_item, Food):
				#that_item.use(hero)
				game.use_item(that_item, hero, True)
				game.time_progress(that_item.nourish*5)
		elif game.find_item(command, False):
			that_item = game.find_item(command, False)
			#if hero.is_in_eq(item_name) == True:
			if that_item in hero.equip:
				if isinstance(that_item, Food):
					game.use_item(that_item, hero, True)
					game.time_progress(that_item.nourish*5)

	elif command[0] == "pij" or command[0] == "drink":
		if game.find_item(command, True):
			that_item = game.find_item(command, True)
			if isinstance(that_item, Drink) or isinstance(that_item, Elixir):
				#that_item.use(hero)
				game.use_item(that_item, hero, True)
				game.time_progress(20)
		elif game.find_item(command, False):
			that_item = game.find_item(command, False)
			if that_item in hero.equip:
				print("Jest")
				if isinstance(that_item, Drink) or isinstance(that_item, Elixir):
					game.use_item(that_item, hero, True)
					game.time_progress(20)
	
	elif command[0] == "użyj" or command[0] == "use":
		if game.find_item(command, True):
			that_item = game.find_item(command, True)
			if isinstance(that_item, Heals):
				#that_item.use(hero)
				game.use_item(that_item, hero, True)
				game.time_progress(60)
		elif game.find_item(command, False):
			that_item = game.find_item(command, False)
			if that_item in hero.equip:
				if isinstance(that_item, Heals):
					game.use_item(that_item, hero, True)
					game.time_progress(60)

	elif command[0] == "dobądź" or command[0] == "dobadz" or command[0] == "draw":
		if game.find_item(command, False):
			that_item = game.find_item(command, False)
			if that_item in hero.equip:
				if isinstance(that_item, Weapon):
					hero.right_hand = that_item
					print("Wziąłeś do ręki "+that_item.name)
				elif isinstance(that_item, Shield):
					hero.left_hand = that_item
					print("Wziąłeś do ręki "+that_item.name)
				else:
					print("To nie jest broń")
			else:
				print("Nie masz takiej broni")
		else:
			print("Nie masz takiej broni")
	
	elif command[0] == "schowaj" or command[0] == "stow":
		if game.find_item(command, False):
			that_item = game.find_item(command, False)
			if hero.right_hand == that_item:
				hero.right_hand = None
				print("Schowałeś "+that_item.name)
			elif hero.right_hand == that_item:
				hero.letf_hand = None
				print("Schowałeś "+that_item.name)

	elif command[0] == "załóż" or command[0] == "zaloz" or command[0] == "put":
		if game.find_item(command, False):
			that_item = game.find_item(command, False)
			if that_item in hero.equip:
				if isinstance(that_item, Armor):
					if that_item.body_part == "head":
						hero.head = that_item
						print("Założyłeś "+that_item.name)
					elif that_item.body_part == "hands":
						hero.hands = that_item
						print("Założyłeś "+that_item.name)
					elif that_item.body_part == "torso1":
						hero.torso1 = that_item
					elif that_item.body_part == "torso2":
						hero.torso2 = that_item
						print("Założyłeś "+that_item.name)
					elif that_item.body_part == "legs":
						hero.legs = that_item
						print("Założyłeś "+that_item.name)
					elif that_item.body_part == "boots":
						hero.boots = that_item
						print("Założyłeś "+that_item.name)
				elif isinstance(that_item, Jewellery):
					if that_item.body_part == "finger":
						if hero.finger1 is not None:
							if hero.finger2 is not None:
								print("Masz już maksymalną liczbę pierścieni, zdjemij jeden")
							else:
								hero.finger2 = that_item
								print("Założyłeś "+that_item.name)
						else: 
							hero.finger1 = that_item
							print("Założyłeś "+that_item.name)
					elif that_item.body_part == "neck":
						hero.neck = that_item
						print("Założyłeś "+that_item.name)


				else:
					print("To nie jest pancerz ani biżuteria")
			else:
				print("Nie masz czegoś takiego")
		else:
			print("Nie masz takiego pancerza")

	elif command[0] == "zdejmij" or command[0] == "zdejm" or command[0] == "take_off":
		if game.find_item(command, False):
			that_item = game.find_item(command, False)
			if hero.right_hand == that_item:
				hero.right_hand = None
				print("Schowałeś "+that_item.name)
			elif hero.head == that_item:
				hero.head = None
				print("Zdjąłeś "+that_item.name)
			elif hero.torso1 == that_item:
				hero.torso1 = None
				print("Zdjąłeś "+that_item.name)
			elif hero.torso2 == that_item:
				hero.torso2 = None
				print("Zdjąłeś "+that_item.name)
			elif hero.hands == that_item:
				hero.hands = None
				print("Zdjąłeś "+that_item.name)
			elif hero.legs == that_item:
				hero.legs = None
				print("Zdjąłeś "+that_item.name)
			elif hero.boots == that_item:
				hero.boots = None
				print("Zdjąłeś "+that_item.name)
			elif hero.finger1 == that_item:
				hero.finger1 = None
				print("Zdjąłeś "+that_item.name)
			elif hero.finger2 == that_item:
				hero.finger2 = None
				print("Zdjąłeś "+that_item.name)
			elif hero.neck == that_item:
				hero.neck = None
				print("Zdjąłeś "+that_item.name)
	
	elif command[0] == "ubierz" or command[0] == "dress":
		if game.find_item(command, False):
			that_item = game.find_item(command, False)
			if that_item in hero.equip:
				if isinstance(that_item, Clothes):
					if that_item.body_part == "head":
						hero.head = that_item
					elif that_item.body_part == "torso1":
						hero.torso1 = that_item
					elif that_item.body_part == "torso2":
						hero.torso2 = that_item
					elif that_item.body_part == "hands":
						hero.hands = that_item
					elif that_item.body_part == "legs":
						hero.legs = that_item
					elif that_item.body_part == "boots":
						hero.boots = that_item

	elif command[0] == "chwyć" or command[0] == "chwyc":
		if game.find_item(command, False):
			that_item = game.find_item(command, False)
			if that_item in hero.equip:
				if isinstance(that_item, Tool):
					hero.right_hand = that_item
					print("Wziąłeś do ręki "+that_item.name)

	elif command[0] == "statystyki" or command[0] == "stats" or command[0] == "stat":
		hero.parameters()

	elif command[0] == "time" or command[0] == "czas":
		game.show_time()
	
	elif command[0] == "save" or command[0] == "zapisz":
		game.save_items()

	elif command[0] == "godmode":
		try: 
			check = command[1]
		except IndexError:
			check = 'null'
			command.append("incorrect") #sprawdzam czy istnieje druga cząśćkomendy, żeby nie było błędu
		if command[1] == 'e':
			game.god_mode = True
			print ("Jesteś teraz w trybie developerskim, używaj go rozważnie")
		elif command[1] == "leave":
			game.god_mode = False
			print ("Opuściłeś tryb developerski")
		else:
			print (command[1])
			print ("Nie masz uprawnień")

	elif command[0] == "create":
		if game.god_mode == True:
			print("Name: ", end="")
			name = input()
			print("Description: ", end="")
			description = input()
			print("Weight: ", end="")
			weight = float(input())
			print("Price: ", end="")
			price = int(input())
			x = hero.x
			y = hero.y
			z = hero.z
			loc = hero.current_location
			temp_item = None
			if command[1] == "food" or command[1] == "fo":
				print("Nourish: ", end="")
				nourish = int(input())
				print("Stamina suppl: ", end="")
				stamina_suppl = int(input())
				temp_item = Food(name, description, x, y, z, loc, weight, price, nourish, stamina_suppl)		
			elif command[1] == "drink" or command[1] == "dr":
				print("Nourish: ", end="")
				nourish = int(input())
				print("Stamina suppl: ", end="")
				stamina_suppl = int(input())
				print("Alcohol: ", end="")
				alcohol = int(input())
				temp_item = Drink(name, description, x, y, z, loc, weight, price, nourish, stamina_suppl, alcohol)
			elif command[1] == "heals" or command[1] == "he":
				print("Hp suppl: ", end="")
				hp_suppl = int(input())
				temp_item = Heals(name, description, x, y, z, loc, weight, price, hp_suppl)
			elif command[1] == "elixir" or command[1] == "el":
				print("Duration: ", end="")
				duration = int(input())
				b_input = "bemnc"
				while b_input != "end":
					b_input = input()
					bonus_input = b_input.split()
					i_hp_sup = bonus_input[1] if bonus_input[0] == "hp_sup" else 0
					i_st_av_sup = bonus_input[1] if bonus_input[0] == "st_av_sup" else 0
					i_st_sup = bonus_input[1] if bonus_input[0] == "st_sup" else 0
					i_mn_sup = bonus_input[1] if bonus_input[0] == "mn_sup" else 0
					i_str = bonus_input[1] if bonus_input[0] == "str" else 0
					i_agl = bonus_input[1] if bonus_input[0] == "agl" else 0
					i_spd = bonus_input[1] if bonus_input[0] == "spd" else 0
					i_dfc = bonus_input[1] if bonus_input[0] == "dfc" else 0
					i_per = bonus_input[1] if bonus_input[0] == "per" else 0
					i_stl = bonus_input[1] if bonus_input[0] == "stl" else 0
					i_hp_b = bonus_input[1] if bonus_input[0] == "hp_b" else 0
					i_mn_b = bonus_input[1] if bonus_input[0] == "mn_b" else 0
				temp_item = Elixir(name, description, x, y, z, loc, weight, price, duration, hp_sup=i_hp_sup, st_av_sup=i_st_av_sup, st_sup=i_st_sup, mn_sup=i_mn_sup, str=i_str, agl=i_agl, spd=i_spd, dfc=i_dfc, per=i_per, stl=i_stl, hp_b=i_hp_b, mn_b=i_mn_b)
			elif command[1] == "closerange"or command[1] == "cr":
				print("Type: ", end="")
				i_type = input()
				print("Damage: ", end="")
				i_dm = int(input())
				print("Strength req: ", end="")
				i_str_r = int(input())
				print("Agility req: ", end="")
				i_agl_r = int(input())
				print("Thoughness: ", end="")
				i_though = int(input())
				print("Cut: ", end="")
				i_cut = int(input())
				print("Stab: ", end="")
				i_stab = int(input())
				print("Crush: ", end="")
				i_crush = int(input())
				print("Block: ", end="")
				i_block = int(input())
				temp_item = CloseRange(name, description, x, y, z, loc, weight, price, w_type=i_type, dm=i_dm, str_r=i_str_r, agl_r=i_agl_r, skill_r=0, though=i_though, cut=i_cut, stab=i_stab, crush=i_crush, block=i_block)
			elif command[1] == "ranged" or command[1] == "ra":
				print("Type: ", end="")
				i_type = input()
				print("Damage: ", end="")
				i_dm = int(input())
				print("Strength req: ", end="")
				i_str_r = int(input())
				print("Agility req: ", end="")
				i_agl_r = int(input())
				print("Ammo type: ", end="")
				i_ammo = int(input())
				print("Range: ", end="")
				i_range = int(input())
				temp_item = Ranged(name, description, x, y, z, loc, weight, price, w_type=i_type, dm=i_dm, str_r=i_str_r, agl_r=i_agl_r, skill_r=0, ammo_type=I_ammo, range=i_range)
			elif command[1] == "armor" or command[1] == "ar" or command[1] == "shield":
				print("Body part: ", end="")
				i_body = input()
				if command[1] == "shield":
					i_body = "left_hand"
				print("Material: ", end="")
				i_material = input()
				print("Defence: ", end="")
				i_defence = input()
				print("Strength req: ", end="")
				i_str_r = int(input())
				print("Agility min: ", end="")
				i_agl_min = int(input())
				print("Speed min: ", end="")
				i_spd_min = int(input())
				if command[1] == "armor":
					temp_item = Armor(name, description, x, y, z, loc, weight, price, body=i_body, material=i_material, defe=i_defence, str_r=i_str_r, agl_min=i_agl_min, spd_min=i_spd_min)
				elif command[1] == "shield":
					temp_item = Shield(name, description, x, y, z, loc, weight, price, body=i_body, material=i_material, defe=i_defence, str_r=i_str_r, agl_min=i_agl_min, spd_min=i_spd_min)		
			elif command[1] == "clothes" or command[1] == "cl":
				print("Body part: ", end="")
				i_body = input()
				print("Cold protection: ", end="")
				i_cold = int(input())
				print("Water protection: ", end="")
				i_water = int(input())
				temp_item = Clothes(name, description, x, y, z, loc, weight, price, body=i_body, cold=i_cold, water=i_water)
			elif command[1] == "tool" or command[1] == "tl":
				temp_item = Tool(name, description, x, y, z, loc, weight, price)
			elif command[1] == "jewellery" or command[1] == "jw":
				print("Body part: ", end="")
				i_body = input()
				temp_item = Jewellery(name, description, x, y, z, loc, weight, price, body=i_body)
			elif command[1] == "machine" or command[1] == "mc":
				temp_item = Machine(name, description, x, y, z, loc, weight, price)
			elif command[1] == "vehicle" or command[1] == "vc":	
				print("Strength req: ", end="")
				i_str_r = int(input())
				print("Speed min: ", end="")
				i_spd_min = int(input())
				temp_item = Vehicle(name, description, x, y, z, loc, weight, price, str_r=i_str_r, spd_min=i_spd_min)
			elif command[1] == "container" or command[1] == "ct":	
				print("Capacity: ", end="")
				i_cap = float(input())
				print("Liquids: ", end="")
				i_liquids = bool(input())
				temp_item = Container(name, description, x, y, z, loc, weight, price, capacity=i_cap, liquids=i_liquids)
			elif command[1] == "furniture" or command[1] == "fu":	
				print("Openable: ", end="")
				i_open = bool(input())
				temp_item = Furniture(name, description, x, y, z, loc, weight, price, open=i_open)
			elif command[1] == "heap" or command[1] == "hp":
				temp_item = Heap(name, description, x, y, z, loc, weight, price)
			game.items.append(temp_item)
			print("Stworzyłeś przedmiot: "+ temp_item.name)
		else:
			print("Nie możesz tego zrobić")
	
	elif command[0] == "insert":
		if game.god_mode == True:
			temp_item = game.find_item(command, False)
			if temp_item:
				that_item = copy.deepcopy(temp_item)
				that_item.id = game.items[-1].id+1 #id ostatniego itemu w liście itemów w grze jest najwyższe, więc po dodaniu 1 dostaniemy niezajęte id 
				print(that_item.id)
				that_item.x = hero.x
				that_item.y = hero.y
				that_item.z = hero.z
				that_item.current_location = hero.current_location
				game.items.append(that_item)
				print("Dodałeś przedmiot: "+ that_item.name)
				print(str(id(that_item)))
			else:
				print("Taki przedmiot jeszcze nie istnieje")

	elif command[0] == "goto":
		if game.god_mode == True:
			x = int(command[1])
			y = int(command[2])
			z = int(command[3])
			hero.x = x
			hero.y = y
			hero.z = z
			hero.current_location.show_location(x, y, z)
		else:
			print("Nie możesz tego zrobić")

	elif command[0] == "colorama":
		print(Fore.BLUE + 'BLUE')
		print(Fore.CYAN + 'CYAN')
		print(Fore.GREEN + 'GREEN')
		print(Fore.LIGHTBLACK_EX + 'LIGHTBLACK_EX')
		print(Fore.LIGHTBLUE_EX + 'LIGHTBLUE_EX')
		print(Fore.LIGHTCYAN_EX + 'LIGHTCYAN_EX')
		print(Fore.LIGHTGREEN_EX + 'LIGHTGREEN_EX')
		print(Fore.LIGHTMAGENTA_EX + 'LIGHTMAGENTA_EX')
		print(Fore.LIGHTRED_EX + 'LIGHTRED_EX')
		print(Fore.LIGHTWHITE_EX + 'LIGHTWHITE_EX')
		print(Fore.LIGHTYELLOW_EX + 'LIGHTYELLOW_EX')
		print(Fore.MAGENTA + 'MAGENTA')
		print(Fore.RED + 'RED')
		print(Fore.RESET + 'RESET')
		print(Fore.WHITE + 'WHITE')
		print(Fore.YELLOW + 'YELLOW' + Style.RESET_ALL)
		print("")
		print(Back.BLUE + 'BLUE')
		print(Back.CYAN + 'CYAN')
		print(Back.GREEN + 'GREEN')
		print(Back.LIGHTBLACK_EX + 'LIGHTBLACK_EX')
		print(Back.LIGHTBLUE_EX + 'LIGHTBLUE_EX')
		print(Back.LIGHTCYAN_EX + 'LIGHTCYAN_EX')
		print(Back.LIGHTGREEN_EX + 'LIGHTGREEN_EX')
		print(Back.LIGHTMAGENTA_EX + 'LIGHTMAGENTA_EX')
		print(Back.LIGHTRED_EX + 'LIGHTRED_EX')
		print(Back.LIGHTWHITE_EX + 'LIGHTWHITE_EX')
		print(Back.LIGHTYELLOW_EX + 'LIGHTYELLOW_EX')
		print(Back.MAGENTA + 'MAGENTA')
		print(Back.RED + 'RED')
		print(Back.RESET + 'RESET')
		print(Back.WHITE + 'WHITE')
		print(Back.YELLOW + 'YELLOW' + Style.RESET_ALL)

	elif command[0] == "help" or command[0] == "pomoc" or command[0] == "?":
		print("DOSTĘPNE KOMENDY: ")
		print("> KIERUNKI: ")
		print(Fore.WHITE+Style.BRIGHT+"    north     | n  | 8"+Style.RESET_ALL+" - przemieść się na północ")
		print(Fore.WHITE+Style.BRIGHT+"    east      | e  | 6"+Style.RESET_ALL+" - przemieść się na wschód")
		print(Fore.WHITE+Style.BRIGHT+"    south     | s  | 2"+Style.RESET_ALL+" - przemieść się na południe")
		print(Fore.WHITE+Style.BRIGHT+"    west      | w  | 4"+Style.RESET_ALL+" - przemieść się na zachód")
		print(Fore.WHITE+Style.BRIGHT+"    northeast | ne | 9"+Style.RESET_ALL+" - przemieść się na północny wschód")
		print(Fore.WHITE+Style.BRIGHT+"    southeast | se | 3"+Style.RESET_ALL+" - przemieść się na południowy wschód")
		print(Fore.WHITE+Style.BRIGHT+"    southwest | sw | 1"+Style.RESET_ALL+" - przemieść się na południowy zachód")
		print(Fore.WHITE+Style.BRIGHT+"    northwest | nw | 7"+Style.RESET_ALL+" - przemieść się na północny zachód")
		print(Fore.WHITE+Style.BRIGHT+"    up        | u  | 5"+Style.RESET_ALL+" - przemieść się w górę")
		print(Fore.WHITE+Style.BRIGHT+"    down      | d  | 0"+Style.RESET_ALL+" - przemieść się w dół")
		print("> POZOSTAŁE: ")
		print(Fore.WHITE+Style.BRIGHT+"    podnieś [nazwa przedmiotu]"+Style.RESET_ALL+" - podnieś przedmiot i umieść w ekwipunku")
		print(Fore.WHITE+Style.BRIGHT+"    upuść [nazwa przedmiotu]"+Style.RESET_ALL+" - usuń przedmiot z ekwipunku")
		print(Fore.WHITE+Style.BRIGHT+"    ? [nazwa przedmiotu]"+Style.RESET_ALL+" - wyświetl możliwe działania")
		print(Fore.WHITE+Style.BRIGHT+"    ekwipunek"+Style.RESET_ALL+" - pokaż zawartość ekwipunku")
		print(Fore.WHITE+Style.BRIGHT+"    czas"+Style.RESET_ALL+" - wyświetl aktualny czas w grze")
		print(Fore.WHITE+Style.BRIGHT+"    save"+Style.RESET_ALL+" - zapisz grę")
		print(Fore.WHITE+Style.BRIGHT+"    exit"+Style.RESET_ALL+" - zakończ grę")
	
	else:
		print("Nie rozumiem. Jesli chcesz sprawdzić komendy wpisz 'help' lub 'pomoc'")