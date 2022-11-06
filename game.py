from humanoid import Humanoid
from item import CloseRange
from konsola import Konsola
from world import World
from hero import Hero
from myjson import MyJson
from item import Item, Consumable, Food, Drink, Heals, Elixir, Weapon, CloseRange, Ranged, Armor, Shield, Clothes, Tool, Jewellery, Machine, Vehicle, Container, Furniture, Heap
import math

class Game:
	def __init__(self):
		self.gameNumer = 0
		self.godMode = True
		self.world = None
		self.hero = None
		self.isPlaying = False
		self.itID = 41
		self.time = {
			"s" : 0,
			"m" : 0,
			"h" : 9,
			"w_day" : 3,
			"week" : 14,
			"day" : 14,
			"month" : 5,
			"year" : 298
		}
		
	def timeProgress(self, sec):
		self.time["s"] += sec
		if self.time["s"] > 59:
			self.time["m"] += math.floor(self.time["s"]/60)
			self.time["s"] %= 60
		if self.time["m"] > 59:
			self.time["h"] += math.floor(self.time["m"]/60)
			self.time["m"] %= 60
		if self.time["h"] > 23:
			self.time["day"] += math.floor(self.time["h"]/24)
			self.time["w_day"] += math.floor(self.time["h"]/24)
			self.time["h"] %= 24
		if self.time["w_day"] > 7:
			self.time["week"] = math.floor(self.time["w_day"]/7)
			self.time["w_day"] %= 7
		if self.time["day"] > 30:
			self.time["month"] += 1
			self.time["day"] %= 30
		if self.time["month"] > 12:
			self.time["year"] += 1
			self.time["month"] = 1
		#print(self.time)
	def showTime(self):
		if self.time["h"]>0 and self.time["h"]<=5 or self.time["h"]>20: T="noc"
		elif self.time["h"]>5 and self.time["h"]<=9: T="rano"
		elif self.time["h"]>9 and self.time["h"]<=11: T="przed południem"
		elif self.time["h"]>11 and self.time["h"]<=12: T="południe"
		elif self.time["h"]>12 and self.time["h"]<=17: T="po południu"
		elif self.time["h"]>17 and self.time["h"]<=20: T="wieczór"

		if self.time["w_day"]==1 : D="poniedziałek"
		elif self.time["w_day"]==2: D="wtorek"
		elif self.time["w_day"]==3: D="środa"
		elif self.time["w_day"]==4: D="czwartek"
		elif self.time["w_day"]==5: D="piątek"
		elif self.time["w_day"]==6: D="sobota"
		elif self.time["w_day"]==7: D="niedziela"

		if self.time["month"]==1: M="stycznia"
		elif self.time["month"]==2: M="lutego"
		elif self.time["month"]==3: M="marca"
		elif self.time["month"]==4: M="kwietnia"
		elif self.time["month"]==5: M="maja"
		elif self.time["month"]==6: M="czerwca"
		elif self.time["month"]==7: M="lipca"
		elif self.time["month"]==8: M="sierpnia"
		elif self.time["month"]==9: M="września"
		elif self.time["month"]==10: M="październiks"
		elif self.time["month"]==11: M="listopads"
		elif self.time["month"]==12: M="grudnia"
		print("Jest {}, {}, {} {} roku {}".format(T, D, self.time["day"], M, self.time["year"]))

	def choseGame(self):
		Konsola.landing()
		correct = False
		while not correct:
			choice = input()
			if choice =="1":
				correct = True
				self.newGame()
			elif choice=="2":
				correct = True
				saves = self.openSaves()
				Konsola.print("Wybierz zapis", "green")
				if not saves:
					Konsola.print("Nie ma żadnych zapisów", "lred")
					correct = False
					input()
					Konsola.landing()
				else:
					for s in saves:
						zapis = " " + str(s["save_number"]+1) + " - " + s["loc_name"]
						Konsola.print(zapis, "lgreen")
					nrChosen = -2
					while nrChosen != -1:
						print(" > ", end="")
						nrChosen = input()
						print(nrChosen.isdigit())
						if nrChosen.isdigit():
							nrChosen = int(nrChosen)
							nrChosen -= 1
							for s in saves:
								if nrChosen == s["save_number"]:
									self.loadGame(s)
									nrChosen = -1
							if nrChosen != -1:
								Konsola.print("Nie ma zapisu o takim numerze", "lred")
						else:
							nrChosen = -1
							correct = False
							Konsola.landing()
							

			elif choice=="3":
				correct = True
				self.tutorial()
			elif choice=="4":
				correct = True
				self.arena()
			elif choice=="5":
				self.endGame()
			else:
				Konsola.print("Wprowadź poprawny wybór", "red", "green")
	def openSaves(self):
		savesPath = "save/saves.json"
		saves = []
		data = MyJson.readJson(savesPath)
		for i in data:
			nrSave = i['save_number']
			locName = i['loc_name']
			time = i['time']
			hero = i['hero']
			locPaths = i['loc_paths']
			save = {"save_number" : nrSave, "loc_paths" : locPaths, "loc_name" : locName, "time" : time, "hero" : hero}
			saves.append(save)
		return saves
	def endGame(self):
		self.isPlaying = False
		Konsola.print("Czy na pewno chcesz wyjść? Upewnij się, że zapisałeś grę (Y/N)", "lyellow", "red")
		#is_it_ok = input()
		is_it_ok = "Y"
		if is_it_ok in ("Y", "y"):
			exit()
	def newGame(self):
		self.isPlaying = True
		Konsola.clear()
		Konsola.print("Nowa gra", "lwhite")
		Konsola.hr()
		maps = ["initial/tantar.json", "initial/czarny_las.json"]
		self.world = World(maps)
		self.hero = self.world.location[0].mobs[0]
		self.hero.currentLocation.showSquare(self.world, self.hero)
		self.time = {
			"s" : 0,
			"m" : 0,
			"h" : 9,
			"w_day" : 3,
			"week" : 14,
			"day" : 14,
			"month" : 5,
			"year" : 298
		}
		saves = self.openSaves()
		try:
			self.gameNumer = saves[-1]["save_number"]+1
		except IndexError:
			self.gameNumer = 0
	def loadGame(self, save):
		self.isPlaying = True
		# Konsola.clear()
		Konsola.print("Wczytałeś grę!", "lwhite")
		Konsola.hr()
		maps = save["loc_paths"]
		self.world = World(maps)
		self.time = save["time"]
		x = save["hero"]["x"]
		y = save["hero"]["y"]
		z = save["hero"]["z"]
		keywords = save["hero"]["keywords"]
		self.hero = Hero(0, x,y,z, "Erlod", ["erlod"], "To tylko ty", "Human", 70, [], **keywords)
	
		nrLoc = save["hero"]["current_location"]
		self.hero.currentLocation = self.world.location[nrLoc]
		self.hero.currentLocation.showSquare(self.world, self.hero)
	def tutorial(self):
		self.isPlaying = True
		Konsola.clear()
		Konsola.print("Tutorial", "lwhite")
		Konsola.hr()
		maps = ["testy/map0.json","testy/map1.json","testy/map2.json","testy/map3.json"]
		self.world = World(maps)
		self.hero = Hero()
		self.hero.currentLocation = self.world.location[0]
		self.hero.x = 2
		self.hero.y = 0
		self.hero.z = 2
		self.hero.param["hp"] = 30
	def arena(self):
		self.isPlaying = True
		Konsola.clear()
		Konsola.print("Arena", "lwhite")
		Konsola.hr()
		saves = self.openSaves()
		try:
			self.gameNumer = saves[-1]["save_number"]+1
		except IndexError:
			self.gameNumer = 0
		maps = ["arena/arena.json"]
		self.world = World(maps)
		self.hero = self.world.location[0].mobs[0]
		self.hero.currentLocation = self.world.location[0]
		self.hero.currentLocation.showSquare(self.world, self.hero)



	def save(self):
		locPaths = []
		iterator = 0
		for l in self.world.location:
			data = {}
			data["name"] = l.name
			data["x"] = l.x
			data["y"] = l.y
			data["size_x"] = l.sizeX
			data["size_y"] = l.sizeY
			data["size_z"] = l.sizeZ
			data["ground_level"] = l.groundLevel
			data["square"] = []
			data["door"] = []
			data["items"] = []
			data["mobs"] = []

			for z in range(l.sizeZ):
				for y in range(l.sizeY):
					for x in range(l.sizeX):
						data_temp = {}
						data_temp['name'] = l.s[x][y][z].name
						data_temp['description'] = l.s[x][y][z].description
						data_temp['coord'] = {}
						data_temp['coord']['x'] = x
						data_temp['coord']['y'] = y
						data_temp['coord']['z'] = z
						data_temp['surface'] = l.s[x][y][z].surface
						data_temp['items'] = l.s[x][y][z].itemIds
						data_temp['exit'] = [None for x in range(10)]
						data_temp['exit'][0] = int(l.s[x][y][z].north)
						data_temp['exit'][1] = int(l.s[x][y][z].northeast)
						data_temp['exit'][2] = int(l.s[x][y][z].east)
						data_temp['exit'][3] = int(l.s[x][y][z].southeast)
						data_temp['exit'][4] = int(l.s[x][y][z].south)
						data_temp['exit'][5] = int(l.s[x][y][z].southwest)
						data_temp['exit'][6] = int(l.s[x][y][z].west)
						data_temp['exit'][7] = int(l.s[x][y][z].northwest)
						data_temp['exit'][8] = int(l.s[x][y][z].up)
						data_temp['exit'][9] = int(l.s[x][y][z].down)
						
						if data_temp['name'] != "Pustka":
							data["square"].append(data_temp)
			
			for d in l.doors:
				data_temp = {}
				data_temp['id'] = d.id
				data_temp['coord'] = {}
				data_temp['coord']['x'] = d.x
				data_temp['coord']['y'] = d.y
				data_temp['coord']['z'] = d.z
				data_temp['direction']  = d.direction
				data_temp['key']  = d.key
				data_temp['open'] = int(d.open)
				data["door"].append(data_temp)
			
			for i in l.items:
				data_temp = {}
				data_temp['class'] = i.__class__.__name__
				data_temp['name'] = i.name
				data_temp['alias'] = i.alias
				data_temp['description'] = i.description
				data_temp['weight'] = i.weight
				data_temp['price'] = i.price
				data_temp['id'] = i.id
				if data_temp['class'] == "Food":
					data_temp['nourish'] = i.nourish
					data_temp['stamina_suppl'] = i.stamina_suppl
				elif data_temp['class'] == "Drink": 
					data_temp['nourish'] = i.nourish
					data_temp['stamina_suppl'] = i.stamina_suppl
					data_temp['alcohol'] = i.alcohol
				elif data_temp['class'] == "Heals":
					data_temp['hp_suppl'] = i.hp_suppl
				elif data_temp['class'] == "Elixir":
					data_temp['duration'] = i.duration
					data_temp["hp_sup"] = i.hp_suppl
					data_temp["st_av_sup"] = i.stamina_aviable_suppl
					data_temp["st_sup"] = i.stamina_suppl
					data_temp["mn_sup"] = i.mana_suppl
					data_temp["str"]  = i.bonus["strength"]
					data_temp["agl"]  = i.bonus["agility"]
					data_temp["spd"]  = i.bonus["speed"]
					data_temp["dfc"]  = i.bonus["defence"]
					data_temp["per"]  = i.bonus["perceptivity"]
					data_temp["stl"]  = i.bonus["stealth"]
					data_temp["hp_b"]   = i.bonus["hp"]
					data_temp["mn_b"]  = i.bonus["mana"]
				elif data_temp['class'] == "CloseRange":
					data_temp['type'] = i.type
					data_temp['damage'] = i.damage
					data_temp['strength_req'] = i.strength_req
					data_temp['agility_req'] = i.agility_req
					data_temp['thoughness'] = i.thoughness
					data_temp['cut'] = i.cut
					data_temp['stab'] = i.stab
					data_temp['crush'] = i.crush
					data_temp['block'] = i.block
				elif data_temp['class'] == "Ranged":
					data_temp['type'] = i.type
					data_temp['damage'] = i.damage
					data_temp['strength_req'] = i.strength_req
					data_temp['agility_req'] = i.agility_req
					data_temp['ammo_type'] = i.ammo_type
					data_temp['range'] = i.range
				elif data_temp['class'] == "Armor" or data_temp['class'] == "Shield":
					data_temp['body_part'] = i.body_part
					data_temp['material'] = i.material
					data_temp['defence'] = i.defence
					data_temp['strength_req'] = i.strength_req
					data_temp['agility_minus'] = i.agility_minus
					data_temp['speed_minus'] = i.speed_minus
				elif data_temp['class'] == "Clothes":
					data_temp['body_part'] = i.body_part
					data_temp['cold_protection'] = i.cold_protection
					data_temp['water_protection'] = i.water_protection
				elif data_temp['class'] == "Tool":
					pass
				elif data_temp['class'] == "Jewellery":
					data_temp['body_part'] = i.body_part
				elif data_temp['class'] == "Machine":
					pass
				elif data_temp['class'] == "Vehicle":
					data_temp['strength_req'] = i.strength_req
					data_temp['speed_minus'] = i.speed_minus
				elif data_temp['class'] == "Container":
					data_temp['capacity']  = i.capacity
					data_temp['for_liquids'] = i.for_liquids
				elif data_temp['class'] == "Furniture":
					data_temp['openable'] = i.openable
					data_temp['function'] = i.function
				elif data_temp['class'] == "Heap":
					pass
				data["items"].append(data_temp)

			for m in l.mobs:
				data_temp = {}
				data_temp['id'] = m.id
				data_temp['x'] = m.x
				data_temp['y'] = m.y
				data_temp['z'] = m.z
				data_temp['name'] = m.name
				data_temp['alias'] = m.alias
				data_temp['description'] = m.description
				data_temp['species'] = m.species
				data_temp['lift'] = m.lift
				data_temp["current_location"] = iterator
				data_temp["equip"] = m.itemIds
				data_temp["keywords"] = {}
				data_temp["keywords"]["hp"] = m.param["hp"]
				data_temp["keywords"]["hp_max"] = m.param["hp_max"]
				data_temp["keywords"]["st"] = m.param["stamina"]
				data_temp["keywords"]["st_av"] = m.param["stamina_aviable"]
				data_temp["keywords"]["st_max"] = m.param["stamina_max"]
				data_temp["keywords"]["mn"] = m.param["mana"]
				data_temp["keywords"]["mn_max"] = m.param["mana_max"]
				data_temp["keywords"]["nou"] = m.param["nourish"]
				data_temp["keywords"]["nou_max"] = m.param["nourish_max"]
				data_temp["keywords"]["str"] = m.stat["strength"]
				data_temp["keywords"]["agl"] = m.stat["agility"]
				data_temp["keywords"]["spd"] = m.stat["speed"]
				data_temp["keywords"]["dfc"] = m.stat["defence"]
				data_temp["keywords"]["per"] = m.stat["perceptivity"]
				data_temp["keywords"]["vis"] = m.stat["visibility"]
				data_temp["keywords"]["sword"] = m.skills["sword"]
				data_temp["keywords"]["axe"] = m.skills["axe"]
				data_temp["keywords"]["spear"] = m.skills["spear"]
				data_temp["keywords"]["cudgel"] = m.skills["cudgel"]
				data_temp["keywords"]["bow"] = m.skills["bow"]
				data["mobs"].append(data_temp)

			path = 'save/'+	data["name"]+str(self.gameNumer)+'.json'
			path = path.lower()
			path = path.replace(" ", "_")
			print(path)
			locPaths.append(path)
			MyJson.saveJson(path, data)
			iterator+=1
		
		saves = self.openSaves()
		locNum = 0
		for i in range(len(self.world.location)):
			if self.world.location[i] == self.hero.currentLocation:
				locNum = i
		inSaves = False
		saveNumber = None
		for s in saves:
			if self.gameNumer == s["save_number"]:
				inSaves = True
				saveNumber = s["save_number"]
				saves[saveNumber]["save_number"] = saveNumber
				
		if not inSaves:
			saveNumber = self.gameNumer
			saves.append({})
			saves[saveNumber] = {}
			saves[saveNumber]["save_number"] = saveNumber
			saves[saveNumber]["time"] = {}
			saves[saveNumber]["loc_paths"] = []
			saves[saveNumber]["hero"] = {}

		saves[saveNumber]["loc_paths"] = locPaths
		saves[saveNumber]["loc_name"] = self.hero.currentLocation.name

		saves[saveNumber]["time"]["s"] = self.time["s"]
		saves[saveNumber]["time"]["m"] = self.time["m"]
		saves[saveNumber]["time"]["h"] = self.time["h"]
		saves[saveNumber]["time"]["w_day"] = self.time["w_day"]
		saves[saveNumber]["time"]["week"] = self.time["week"]
		saves[saveNumber]["time"]["day"] = self.time["day"]
		saves[saveNumber]["time"]["month"] = self.time["month"]
		saves[saveNumber]["time"]["year"] = self.time["year"]

		saves[saveNumber]["hero"]["x"] = self.hero.x
		saves[saveNumber]["hero"]["y"] = self.hero.y
		saves[saveNumber]["hero"]["z"] = self.hero.z
		saves[saveNumber]["hero"]["current_location"] = locNum
		saves[saveNumber]["hero"]["keywords"] = {}
		saves[saveNumber]["hero"]["keywords"]["hp"] = self.hero.param["hp"]
		saves[saveNumber]["hero"]["keywords"]["hp_max"] = self.hero.param["hp_max"]
		saves[saveNumber]["hero"]["keywords"]["st"] = self.hero.param["stamina"]
		saves[saveNumber]["hero"]["keywords"]["st_av"] = self.hero.param["stamina_aviable"]
		saves[saveNumber]["hero"]["keywords"]["st_max"] = self.hero.param["stamina_max"]
		saves[saveNumber]["hero"]["keywords"]["mn"] = self.hero.param["mana"]
		saves[saveNumber]["hero"]["keywords"]["mn_max"] = self.hero.param["mana_max"]
		saves[saveNumber]["hero"]["keywords"]["nou"] = self.hero.param["nourish"]
		saves[saveNumber]["hero"]["keywords"]["nou_max"] = self.hero.param["nourish_max"]
		saves[saveNumber]["hero"]["keywords"]["str"] = self.hero.stat["strength"]
		saves[saveNumber]["hero"]["keywords"]["agl"] = self.hero.stat["agility"]
		saves[saveNumber]["hero"]["keywords"]["spd"] = self.hero.stat["speed"]
		saves[saveNumber]["hero"]["keywords"]["dfc"] = self.hero.stat["defence"]
		saves[saveNumber]["hero"]["keywords"]["per"] = self.hero.stat["perceptivity"]
		saves[saveNumber]["hero"]["keywords"]["vis"] = self.hero.stat["visibility"]
		saves[saveNumber]["hero"]["keywords"]["sword"] = self.hero.skills["sword"]
		saves[saveNumber]["hero"]["keywords"]["axe"] = self.hero.skills["axe"]
		saves[saveNumber]["hero"]["keywords"]["spear"] = self.hero.skills["spear"]
		saves[saveNumber]["hero"]["keywords"]["cudgel"] = self.hero.skills["cudgel"]
		saves[saveNumber]["hero"]["keywords"]["bow"] = self.hero.skills["bow"]

		path = 'save\saves.json'
		MyJson.saveJson(path, saves)
						
	def travel(self, mob, direction):
		didMove = False
		if direction in (7,8,9) and mob.y == 0:
			didMove = self.moveToLocation(mob, direction)
		elif direction in (7,4,1) and mob.x == 0:
			didMove = self.moveToLocation(mob, direction)
		elif direction in (9,6,3) and mob.x == mob.currentLocation.sizeX-1:
			didMove = self.moveToLocation(mob, direction)
		elif direction in (1,2,3) and mob.y == mob.currentLocation.sizeY-1:
			didMove = self.moveToLocation(mob, direction)
		else:
			didMove = mob.travel(direction)
		if mob == self.hero and didMove:
			self.timeProgress(15)
			self.hero.currentLocation.showSquare(self.world, self.hero)
	
	def moveToLocation(self, mob, direction):
		if mob.currentLocation.s[mob.x][mob.y][mob.z].checkExit(direction):
			mobX = mob.x + mob.currentLocation.x
			mobY = mob.y + mob.currentLocation.y
			mobZ = mob.z + (self.world.groundLevel - mob.currentLocation.groundLevel)
			if direction == 8:
				for loc in self.world.location:
					#sprawdzam, czy obecnie(!) hero znajduje się dokładnie jedną kratkę na południe od lokacji
					if loc.y + loc.sizeY == mobY and loc.x <= mobX <= loc.x+loc.sizeX: 
						mob.x = mobX - loc.x
						mob.y = mobY - loc.y - 1
						mob.z = mobZ - (self.world.groundLevel - loc.groundLevel)
						mob.currentLocation = loc
						return True
			elif direction == 6:
				for loc in self.world.location:
					if loc.x - 1 == mobX and loc.y <= mobY <= loc.y+loc.sizeY:
						mob.x = 0
						mob.y = mobY - loc.y 
						mob.z = mobZ - (self.world.groundLevel - loc.groundLevel)
						mob.currentLocation = loc
						return True
			elif direction == 2:
				for loc in self.world.location:
					if loc.y - 1 == mobY and loc.x <= mobX <= loc.x+loc.sizeX:
						mob.x = mobX - loc.x
						mob.y = 0
						mob.z = mobZ - (self.world.groundLevel - loc.groundLevel)
						mob.currentLocation = loc
						return True
			elif direction == 4:
				for loc in self.world.location:
					if loc.x + loc.sizeX == mobX and loc.y <= mobY <= loc.y+loc.sizeY:
						mob.x = mobX - loc.x -1
						mob.y = mobY - loc.y 
						mob.z = mobZ - (self.world.groundLevel - loc.groundLevel)
						mob.currentLocation = loc
						return True
			elif direction == 9:
				for loc in self.world.location:
					#spr, czy hero.x + 1 i hero y - 1 jest na obszarze lokacji
					if loc.y <= mobY - 1 <= loc.y + loc.sizeY - 1 and loc.x <= mobX + 1 <= loc.x + loc.sizeX -1:
						mob.x = mobX - loc.x + 1
						mob.y = mobY - loc.y - 1
						mob.z = mobZ - (self.world.groundLevel - loc.groundLevel)
						mob.currentLocation = loc
						return True
			elif direction == 3:
				for loc in self.world.location:
					#spr, czy hero.x + 1 i hero y + 1 jest na obszarze lokacji
					if loc.y <= mobY + 1 <= loc.y + loc.sizeY - 1 and loc.x <= mobX + 1 <= loc.x + loc.sizeX -1:
						mob.x = mobX - loc.x + 1
						mob.y = mobY - loc.y + 1
						mob.z = mobZ - (self.world.groundLevel - loc.groundLevel)
						mob.currentLocation = loc
						return True
			elif direction == 1:
				for loc in self.world.location:
					#spr, czy hero.x - 1 i hero y + 1 jest na obszarze lokacji
					if loc.y <= mobY + 1 <= loc.y + loc.sizeY - 1 and loc.x <= mobX - 1 <= loc.x + loc.sizeX -1:
						mob.x = mobX - loc.x - 1
						mob.y = mobY - loc.y + 1
						mob.z = mobZ - (self.world.groundLevel - loc.groundLevel)
						mob.currentLocation = loc
						return True
			elif direction == 7:
				for loc in self.world.location:
					#spr, czy hero.x - 1 i hero y - 1 jest na obszarze lokacji
					if loc.y <= mobY - 1 <= loc.y + loc.sizeY - 1 and loc.x <= mobX - 1 <= loc.x + loc.sizeX -1:
						mob.x = mobX - loc.x - 1
						mob.y = mobY - loc.y - 1
						mob.z = mobZ - (self.world.groundLevel - loc.groundLevel)
						mob.currentLocation = loc
						return True
		return False

	def goto(self, command):
		if self.godMode == True:
			if command[1] == "n":
				self.hero.y = self.hero.y-1
				self.hero.currentLocation.showSquare(self.world, self.hero)
			elif command[1] == "e":
				self.hero.x = self.hero.x+1
				self.hero.currentLocation.showSquare(self.world, self.hero)
			elif command[1] == "s":
				self.hero.y = self.hero.y+1
				self.hero.currentLocation.showSquare(self.world, self.hero)
			elif command[1] == "w":
				self.hero.x = self.hero.x-1
				self.hero.currentLocation.showSquare(self.world, self.hero)
			elif command[1] == "u":
				self.hero.z = self.hero.z+1
				self.hero.currentLocation.showSquare(self.world, self.hero)
			elif command[1] == "d":
				self.hero.z = self.hero.z-1
				self.hero.currentLocation.showSquare(self.world, self.hero)
			else:
				try: 
					x = int(command[1])
					y = int(command[2])
					z = int(command[3])
					self.hero.x = x
					self.hero.y = y
					self.hero.z = z
					self.hero.currentLocation.showSquare(self.world, self.hero)
				except:
					print("Podaj koordyanty")
		else:
			print("Nie możesz tego zrobić")

	def findItem(self, itemName):
		return self.hero.currentLocation.findItem(itemName, self.hero)
	
	def findMob(self, mobName):
		return self.hero.currentLocation.findMob(mobName, self.hero)
