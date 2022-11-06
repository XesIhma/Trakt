from game import Game
from konsola import Konsola
from item import Item, Consumable, Food, Drink, Heals, Elixir, Weapon, CloseRange, Ranged, Armor, Shield, Clothes, Tool, Jewellery, Machine, Vehicle, Container, Furniture, Heap

game = Game()
print = Konsola.print
game.choseGame()

while game.isPlaying:

	command = Konsola.prompt(game.hero)
	if len(command) == 0:
		print("Co chcesz zrobić?")
	elif command[0] in ("north", "n", "8"):
		game.travel(game.hero, 8)
	elif command[0] in ("northeast", "ne", "9"):
		game.travel(game.hero, 9)
	elif command[0] in ("east", "e", "6"):
		game.travel(game.hero, 6)
	elif command[0] in ("southeast", "se", "3"):
		game.travel(game.hero, 3)
	elif command[0] in ("south", "s", "2"):
		game.travel(game.hero, 2)
	elif command[0] in ("southwest", "sw", "1"):
		game.travel(game.hero, 1)
	elif command[0] in ("west", "w", "4"):
		game.travel(game.hero, 4)
	elif command[0] in ("northwest", "nw", "7"):
		game.travel(game.hero, 7)
	elif command[0] in ("up", "u", "5"):
		game.travel(game.hero, 5)
	elif command[0] in ("down", "d", "0"):
		game.travel(game.hero, 0)
	elif command[0] in ("exit", "end", "quit", "q"):
		game.endGame()
	elif command[0] in ("whereami"):
		game.hero.whereami()
	elif command[0] in ("whoami"):
		game.hero.whoami()
	elif command[0] in ("help", "pomoc"):
		Konsola.help()

	elif command[0] in ("podnieś", "podnies", "pick"):	
		itemName = Konsola.nameConvert(command)
		thatItem = game.findItem(itemName)
		if thatItem:
			game.hero.pickUp(thatItem, True)

	elif command[0] in ("upuść", "upusc", "drop"):
		itemName = Konsola.nameConvert(command)
		thatItem = game.hero.drop(itemName, True)

	elif command[0] in ("info", "?"):
		itemName = Konsola.nameConvert(command)
		thatItem = game.findItem(itemName)
		if thatItem:
			thatItem.possible_actions()

	elif command[0] in ("zobacz", "see"):
		itemName = Konsola.nameConvert(command)
		thatItem = game.findItem(itemName)
		if thatItem:
			thatItem.see()

	elif command[0] in ("zjedz", "eat"):
		itemName = Konsola.nameConvert(command)
		thatItem = game.hero.isInEq(itemName)
		if thatItem:
			if isinstance(thatItem, Food):
				thatItem.use(game.hero, True)
				game.timeProgress(thatItem.nourish*2)

	elif command[0] in ("wypij", "drink"):
		itemName = Konsola.nameConvert(command)
		thatItem = game.hero.isInEq(itemName)
		if thatItem:
			if isinstance(thatItem, Drink) or isinstance(thatItem, Elixir):
				thatItem.use(game.hero, True)
				game.timeProgress(20)

	elif command[0] in ("użyj", "uzyj"):
		itemName = Konsola.nameConvert(command)
		thatItem = game.hero.isInEq(itemName)
		if thatItem:
			if isinstance(thatItem, Heals):
				thatItem.use(game.hero, True)
				game.timeProgress(60)

	elif command[0] in ("dobądź", "dobadz", "draw"):
		itemName = Konsola.nameConvert(command)
		thatItem = game.hero.isInEq(itemName)
		if thatItem:
			game.hero.draw(thatItem, True)
		else:
			print("Nie masz takiej broni")

	elif command[0] in ("schowaj", "stow"):
		itemName = Konsola.nameConvert(command)
		thatItem = game.hero.isInEq(itemName)
		if thatItem:
			game.hero.stow(thatItem, True)
		else:
			print("Nie masz takiej broni w ręce")

	elif command[0] in ("załóż", "zaloz"):
		itemName = Konsola.nameConvert(command)
		thatItem = game.hero.isInEq(itemName)
		if thatItem:
			game.hero.putOn(thatItem, True)
		else:
			print("Nie masz czegoś takiego")
	
	elif command[0] in ("zdejmij", "zdejm"):
		itemName = Konsola.nameConvert(command)
		thatItem = game.hero.isInEq(itemName)
		if thatItem:
			game.hero.takeOff(thatItem, True)

	elif command[0] in ("ubierz", "dress"):
		itemName = Konsola.nameConvert(command)
		thatItem = game.hero.isInEq(itemName)
		if thatItem:
			game.hero.dress(thatItem, True)
		else:
			print("Nie masz czegoś takiego")
			
	elif command[0] in ("chwyć", "chwyc"):
		itemName = Konsola.nameConvert(command)
		thatItem = game.hero.isInEq(itemName)
		if thatItem:
			game.hero.grab(thatItem, True)
		else:
			print("Nie masz czegoś takiego")

	elif command[0] in ("prowadź", "prowadz"):	
		itemName = Konsola.nameConvert(command)
		thatItem = game.findItem(itemName)
		if thatItem:
			game.hero.drive(thatItem, True)

	elif command[0] in ("zostaw"):	
		itemName = Konsola.nameConvert(command)
		game.hero.leave(itemName, True)
	
	elif command[0] in ("zabij"):
		mobName = Konsola.nameConvert(command)
		thatMob = game.findMob(mobName)
		if thatMob:
			howLong = game.hero.kill(thatMob)
			game.timeProgress(howLong)
			
	elif command[0] in ("odpoczywaj", "odpocznij", "odp", "rest"):
		try: 
			howLong = int(command[1])
		except:
			howLong = 1
		game.hero.rest(howLong)
		game.timeProgress(howLong*3600)

	elif command[0] in ("śpij", "spij", "sleep"):
		if game.hero.param["stamina_aviable"]/game.hero.param["stamina_max"] > 0.5:
			print("Nie chce Ci się jeszcze spać")
		else:
			for i in game.hero.currentLocation.s[game.hero.x][game.hero.y][game.hero.z].items:
				try:
					if i.function == "bed":
						howLong = game.hero.sleep()
						game.timeProgress(howLong*3600)
					else: print("Tu nie ma na czym spać!")
				except: 
					print("Tu nie ma na czym spać!")

	elif command[0] in ("ekwipunek", "equip", "ekw", "eq"):
		game.hero.showEquip()
	
	elif command[0] in ("wyposażenie", "wyposazenie", "wyp", "outfit"):
		game.hero.outfit()

	elif command[0] in ("statystyki", "stats", "stat"):
		game.hero.parameters()

	elif command[0] in ("time", "czas"):
		game.showTime()

	elif command[0] in ("zapisz", "save"):
		game.save()
		
#GODMODE STUFF
	elif command[0] in ("goto"):
		game.goto(command)
	elif command[0] in ("create"):
		if game.godMode == True:
			game.hero.currentLocation.createItem(game.hero, command[1])
			
			
	
	elif command[0] in ("insert"):
		if game.godMode == True:
			game.hero.currentLocation.insertItem(game.hero, command)
	
	elif command[0] in ("edit"):
		if game.godMode == True:
			try: 
				what = command[1]
				try:
					exit = command[2]
				except: exit = "benc"
				Konsola.edit(game.hero, what, exit)
			except: print("Co chesz zmienić?")
	
	elif command[0] in ("map"):
		if game.godMode == True:
			Konsola.map(game.hero)

	else:
		print("Nie rozumiem. Jesli chcesz sprawdzić komendy wpisz 'help' lub 'pomoc'", "grey")
	