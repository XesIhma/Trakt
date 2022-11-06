from humanoid import Humanoid
from hero import Hero
from konsola import Konsola
from square import Square
from door import Door
from myjson import MyJson
from item import Item, Consumable, Food, Drink, Heals, Elixir, Weapon, CloseRange, Ranged, Armor, Shield, Clothes, Tool, Jewellery, Machine, Vehicle, Container, Furniture, Heap

class Location:
	def __init__(self, filePath):
		self.name = "Nigdzie"
		self.x = 0
		self.y = 0
		self.sizeX = 1
		self.sizeY = 1
		self.sizeZ = 1
		self.ground_level = 0
		self.s = None
		self.doors = []
		self.items = []
		self.mobs = []

		data = MyJson.readJson(filePath)
		self.name = data['name']
		self.x = data['x']
		self.y = data['y']
		self.sizeX = data['size_x']
		self.sizeY = data['size_y']
		self.sizeZ = data['size_z']
		self.groundLevel = data['ground_level']
		squareList = data['square']
		doorList = data['door']
		itemList = data['items']
		mobList = data['mobs']
		
		for d in doorList:
			newDoor = Door(d['id'], d['coord']['x'], d['coord']['y'], d['coord']['z'], d['direction'], d['key'], bool(d['open']))
			self.doors.append(newDoor)
		for i in itemList:
			keywords = i["keywords"]
			class_name = i['class']
			name = i['name']
			alias = i['alias']
			if not name.lower() in alias:
				alias.append(name.lower())
			description = i['description']
			weight = i['weight']
			price = i['price']
			itemId = i['id']
			if class_name == "Food":
				newItem = Food(itemId, name, alias, description, weight, price, **keywords)
				self.items.append(newItem)
			elif class_name == "Drink": 
				newItem = Drink(itemId, name, alias, description, weight, price, **keywords)
				self.items.append(newItem)
			elif class_name == "Heals":
				newItem = Heals(itemId, name, alias, description, weight, price, **keywords)
				self.items.append(newItem)
			elif class_name == "Elixir":
				newItem = Elixir(itemId, name, alias, description, weight, price, **keywords)
				self.items.append(newItem)
			elif class_name == "CloseRange":
				newItem = CloseRange(itemId, name, alias, description, weight, price, **keywords)
				if not i['keywords']['type'] in alias: newItem.alias.append(i['keywords']['type'])
				self.items.append(newItem)
			elif class_name == "Ranged":
				newItem = Ranged(itemId, name, alias, description, weight, price, **keywords)
				if not i['keywords']['type'] in alias: newItem.alias.append(i['keywords']['type'])
				self.items.append(newItem)   
			elif class_name == "Armor":
				newItem = Armor(itemId, name, alias, description, weight, price, **keywords)
				self.items.append(newItem)
			elif class_name == "Shield":
				newItem = Shield(itemId, name, alias, description, weight, price, **keywords)
				if not "shield" in alias: newItem.alias.append("shield")
				self.items.append(newItem)
			elif class_name == "Clothes":
				newItem = Clothes(itemId, name, alias, description, weight, price, **keywords)
				self.items.append(newItem)
			elif class_name == "Tool":
				newItem = Tool(itemId, name, alias, description, weight, price)
				self.items.append(newItem)
			elif class_name == "Jewellery":
				newItem = Jewellery(itemId, name, alias, description, weight, price, **keywords)
				self.items.append(newItem)
			elif class_name == "Machine":
				newItem = Machine(itemId, name, alias, description, weight, price)
				self.items.append(newItem)
			elif class_name == "Vehicle":
				newItem = Vehicle(itemId, name, alias, description, weight, price, **keywords)
				self.items.append(newItem)
			elif class_name == "Container":
				newItem = Container(itemId, name, alias, description, weight, price, **keywords)
				self.items.append(newItem)
			elif class_name == "Furniture":
				newItem = Furniture(itemId, name, alias, description, weight, price, **keywords)
				self.items.append(newItem)
			elif class_name == "Heap":
				newItem = Heap(itemId, name, alias, description, weight, price)
				self.items.append(newItem)
		
		## PIERWSZE PODEJŚCIE ##
		for m in mobList:
			keywords = m["keywords"]
			if m['id'] == 0:
					newMob = Hero(m['id'], m['x'], m['y'], m['z'], m['name'], m['alias'], m['description'], m['species'], m['lift'], m['equip'], **keywords)
			else:
				newMob = Humanoid(m['id'], m['x'], m['y'], m['z'], m['name'], m['alias'], m['description'], m['species'], m['lift'], m['equip'], **keywords)
			newMob.currentLocation = self
			self.mobs.append(newMob)

		self.s = [[[Square(i, j, k, 5, "Pustka", "Nic tu nie ma", [], n=1,ne=1,e=1,se=1,s=1,sw=1,w=1,nw=1,u=1,d=1) for k in range(self.sizeZ)] for j in range(self.sizeY)] for i in range(self.sizeX)]
		for s in range(len(squareList)):
			x = squareList[s]["coord"]["x"]
			y = squareList[s]["coord"]["y"]
			z = squareList[s]["coord"]["z"]
			self.s[x][y][z] = Square(x, y, z, squareList[s]["surface"], squareList[s]["name"], squareList[s]["description"], squareList[s]["items"],
									n=bool(squareList[s]["exit"][0]), ne=bool(squareList[s]["exit"][1]), 
									e=bool(squareList[s]["exit"][2]), se=bool(squareList[s]["exit"][3]), 
									s=bool(squareList[s]["exit"][4]), sw=bool(squareList[s]["exit"][5]), 
									w=bool(squareList[s]["exit"][6]), nw=bool(squareList[s]["exit"][7]), 
									u=bool(squareList[s]["exit"][8]), d=bool(squareList[s]["exit"][9]))
		#DODAWANIE DRZWI
		for d in self.doors:
			x = d.x
			y = d.y
			z = d.z
			if d.direction == 8:
				self.s[x][y][z].doorN = d
				self.s[x][y-1][z].doorS = d
			elif d.direction == 4:
				self.s[x][y][z].doorW = d
				self.s[x-1][y][z].doorE = d
			elif d.direction == 0:
				self.s[x][y][z].doorD = d
				self.s[x][y][z-1].doorU = d
		#DODAWANIE ITEMÓW
		for i in self.items:
			for x in range(self.sizeX):
				for y in range(self.sizeY):
					for z in range(self.sizeZ):
						itemIds = self.s[x][y][z].itemIds
						for j in range(len(itemIds)):
							if i.id == itemIds[j]:
								self.s[x][y][z].items.append(i)
		for i in self.items:
			for m in self.mobs:
				itemIds = m.itemIds
				for j in range(len(itemIds)):
					if i.id == itemIds[j]:
						m.equip.append(i)

	def test(self):
		licznik = 0
		for z in range(self.sizeZ):
			for y in range(self.sizeY):
				for x in range(self.sizeX):
					print(licznik)
					licznik+=1
					print("X: {}, Y: {}, Z: {}".format(x, y, z))
					print(self.s[x][y][z].name)
					#print(self.s[x][y][z].showContent())
	def showSquare(self, world, hero):
		self.s[hero.x][hero.y][hero.z].showSquare(world, hero)
		
	def findItem(self, itemName, hero):
		items = self.s[hero.x][hero.y][hero.z].items
		hit = []
		for i in items:
			for a in i.alias:
				if itemName == a:
					hit.append(i)
		if len(hit) == 1:
			return hit[0]
		elif len(hit) > 1:
			Konsola.print("O którą rzecz dokładnie Ci chodzi", "red")
			return self.choseHit(hit)
		else: 
			Konsola.print("Nie ma tu takiej rzeczy", "red")
			return 0
	def findMob(self, mobName, hero):
		hit = []
		for m in self.mobs:
			if hero.coordComp(m):
				for a in m.alias:
					if mobName == a:
						hit.append(m)
		if len(hit) == 1:
			return hit[0]
		elif len(hit) > 1:
			Konsola.print("O kogo Ci dokładnie chodzi?", "red")
			return self.choseHit(hit)

		else: 
			Konsola.print("Nie ma tu kogoś takiego", "red")
			return 0	
	
	def choseHit(self, hit):
			for i in range(len(hit)):
				print(str(i+1)+". "+hit[i].name)
			correct = False
			while not correct:
				decision = int(input())-1
				for i in range(len(hit)):
					if decision == i:
						return hit[decision]

	#GODMODE STUFF
	def createItem(self, hero, className):
			print("Name: ", end="")
			name = input()
			print("Alias: ", end="")
			alias = []
			alias.append(input())
			print("Description: ", end="")
			description = input()
			print("Weight: ", end="")
			weight = float(input())
			print("Price: ", end="")
			price = int(input())
			x = hero.x
			y = hero.y
			z = hero.z
			temp_item = None
			if className == "food" or className == "fo":
				print("Nourish: ", end="")
				nourish = int(input())
				print("Stamina suppl: ", end="")
				stamina_suppl = int(input())
				temp_item = Food(-1, name, alias, description, weight, price, nourish, stamina_suppl)		
			elif className == "drink" or className == "dr":
				print("Nourish: ", end="")
				nourish = int(input())
				print("Stamina suppl: ", end="")
				stamina_suppl = int(input())
				print("Alcohol: ", end="")
				alcohol = int(input())
				temp_item = Drink(-1, name, alias, description, weight, price, nourish, stamina_suppl, alcohol)
			elif className == "heals" or className == "he":
				print("Hp suppl: ", end="")
				hp_suppl = int(input())
				temp_item = Heals(-1, name, alias, description, weight, price, hp_suppl)
			elif className == "elixir" or className == "el":
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
				temp_item = Elixir(-1, name, alias, description, weight, price, duration, hp_sup=i_hp_sup, st_av_sup=i_st_av_sup, st_sup=i_st_sup, mn_sup=i_mn_sup, str=i_str, agl=i_agl, spd=i_spd, dfc=i_dfc, per=i_per, stl=i_stl, hp_b=i_hp_b, mn_b=i_mn_b)
			elif className == "closerange"or className == "cr":
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
				temp_item = CloseRange(-1, name, alias, description, weight, price, w_type=i_type, dm=i_dm, str_r=i_str_r, agl_r=i_agl_r, skill_r=0, though=i_though, cut=i_cut, stab=i_stab, crush=i_crush, block=i_block)
			elif className == "ranged" or className == "ra":
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
				temp_item = Ranged(-1, name, alias, description, weight, price, w_type=i_type, dm=i_dm, str_r=i_str_r, agl_r=i_agl_r, skill_r=0, ammo_type=i_ammo, range=i_range)
			elif className == "armor" or className == "ar" or className == "shield":
				print("Body part: ", end="")
				i_body = input()
				if className == "shield":
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
				if className == "armor":
					temp_item = Armor(-1, name, alias, description, weight, price, body=i_body, material=i_material, dfc=i_defence, str_r=i_str_r, agl_min=i_agl_min, spd_min=i_spd_min)
				elif className == "shield":
					temp_item = Shield(-1, name, alias, description, weight, price, body=i_body, material=i_material, dfc=i_defence, str_r=i_str_r, agl_min=i_agl_min, spd_min=i_spd_min)		
			elif className == "clothes" or className == "cl":
				print("Body part: ", end="")
				i_body = input()
				print("Cold protection: ", end="")
				i_cold = int(input())
				print("Water protection: ", end="")
				i_water = int(input())
				temp_item = Clothes(-1, name, alias, description, weight, price, body=i_body, cold=i_cold, water=i_water)
			elif className == "tool" or className == "tl":
				temp_item = Tool(-1, name, alias, description, weight, price)
			elif className == "jewellery" or className == "jw":
				print("Body part: ", end="")
				i_body = input()
				temp_item = Jewellery(-1, name, alias, description, weight, price, body=i_body)
			elif className == "machine" or className == "mc":
				temp_item = Machine(-1, name, alias, description, weight, price)
			elif className == "vehicle" or className == "vc":	
				print("Strength req: ", end="")
				i_str_r = int(input())
				print("Speed min: ", end="")
				i_spd_min = int(input())
				temp_item = Vehicle(-1, name, alias, description, weight, price, str_r=i_str_r, spd_min=i_spd_min)
			elif className == "container" or className == "ct":	
				print("Capacity: ", end="")
				i_cap = float(input())
				print("Liquids: ", end="")
				i_liquids = bool(input())
				temp_item = Container(-1, name, alias, description, weight, price, capacity=i_cap, liquids=i_liquids)
			elif className == "furniture" or className == "fu":	
				print("Openable: ", end="")
				i_open = bool(input())
				print("Funkcja: ", end="")
				i_function = input()
				temp_item = Furniture(-1, name, alias, description, weight, price, open=i_open, function=i_function)
			elif className == "heap" or className == "hp":
				temp_item = Heap(-1, name, alias, description, weight, price)
			hero.currentLocation.items.append(temp_item)
			hero.currentLocation.s[x][y][z].addItem(temp_item)
			print("Stworzyłeś przedmiot: "+ temp_item.name)