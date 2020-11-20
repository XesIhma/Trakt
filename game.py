import math
import json
from colorama import Fore, Back, Style
from world import World
from item import Item, Consumable, Food, Drink, Heals, Elixir, Weapon, CloseRange, Ranged, Armor, Shield, Clothes, Tool, Jewellery, Machine, Vehicle, Container, Furniture, Heap

class Game:
	def __init__(self):
		self.time = {
			"s" : 0,
			"m" : 0,
			"h" : 9,
			"w_day" : 3,
			"week" : 14,
			"day" : 14,
			"month" : 5,
			"year" : 218
		}
		self.god_mode = True
		self.world = None
		self.hero = None
		self.items = []
		
	def time_progress(self, sec):
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
	def show_time(self):
		if self.time["h"]>0 and self.time["h"]<=5 and self.time["h"]>20: T="noc"
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
	
	def player_travel(self, direction):
		if self.hero.travel(direction):
			#POKAZUJE OPIS LOKACJI
			self.hero.current_location.show_location(self.hero.x, self.hero.y, self.hero.z)
			#POKAZUJE ITEMY
			for i in range(len(self.items)):
				if self.items[i].compare_coords(self.hero):
					print(Fore.BLUE + Style.BRIGHT + self.items[i].name + Style.RESET_ALL)
			#POKAZUJE NPC

			#UPŁYW CZASU
			if direction in [0, 2, 4, 5, 6, 8]:
				self.time_progress(10)
			elif direction in [1, 3, 5, 7]:
				self.time_progress(14)

	def find_item(self, command, compare):
		item_name = item_name_convert(command)
		for i in range(len(self.items)):
			if self.items[i].name.lower() == item_name:
				if compare:
					if self.hero.compare_coords(self.items[i]):
						return self.items[i]
				else:
					return self.items[i]
		return 0
	def use_item(self, item, being, info):
		item.use(being, info)
		self.items.remove(item)

	def save_items(self):
		data = []
		for i in range(len(self.items)):
			data_temp = {}
			data_temp['class'] = self.items[i].__class__.__name__
			data_temp['name'] = self.items[i].name
			data_temp['description'] = self.items[i].description
			data_temp['weight'] = self.items[i].weight
			data_temp['price'] = self.items[i].price
			data_temp['x'] = self.items[i].x
			data_temp['y'] = self.items[i].y
			data_temp['z'] = self.items[i].z
			if data_temp['class'] == "Food":
				data_temp['nourish'] = self.items[i].nourish
				data_temp['stamina_suppl'] = self.items[i].stamina_suppl
			elif data_temp['class'] == "Drink": 
				data_temp['nourish'] = self.items[i].nourish
				data_temp['stamina_suppl'] = self.items[i].stamina_suppl
				data_temp['alcohol'] = self.items[i].alcohol
			elif data_temp['class'] == "Heals":
				data_temp['hp_suppl'] = self.items[i].hp_suppl
			elif data_temp['class'] == "Elixir":
				data_temp['duration'] = self.items[i].duration
				data_temp["hp_sup"] = self.items[i].hp_suppl
				data_temp["st_av_sup"] = self.items[i].stamina_aviable_suppl
				data_temp["st_sup"] = self.items[i].stamina_suppl
				data_temp["mn_sup"] = self.items[i].mana_suppl
				data_temp["str"]  = self.items[i].bonus["strength"]
				data_temp["agl"]  = self.items[i].bonus["agility"]
				data_temp["spd"]  = self.items[i].bonus["speed"]
				data_temp["dfc"]  = self.items[i].bonus["defence"]
				data_temp["per"]  = self.items[i].bonus["perceptivity"]
				data_temp["stl"]  = self.items[i].bonus["stealth"]
				data_temp["hp_b"]   = self.items[i].bonus["hp"]
				data_temp["mn_b"]  = self.items[i].bonus["mana"]
			elif data_temp['class'] == "CloseRange":
				data_temp['type'] = self.items[i].type
				data_temp['damage'] = self.items[i].damage
				data_temp['strength_req'] = self.items[i].strength_req
				data_temp['agility_req'] = self.items[i].agility_req
				data_temp['thoughness'] = self.items[i].thoughness
				data_temp['cut'] = self.items[i].cut
				data_temp['stab'] = self.items[i].stab
				data_temp['crush'] = self.items[i].crush
				data_temp['block'] = self.items[i].block
			elif data_temp['class'] == "Ranged":
				data_temp['type'] = self.items[i].type
				data_temp['damage'] = self.items[i].damage
				data_temp['strength_req'] = self.items[i].strength_req
				data_temp['agility_req'] = self.items[i].agility_req
				data_temp['ammo_type'] = self.items[i].ammo_type
				data_temp['range'] = self.items[i].range
			elif data_temp['class'] == "Armor":
				data_temp['body_part'] = self.items[i].body_part
				data_temp['material'] = self.items[i].material
				data_temp['defence'] = self.items[i].defence
				data_temp['strength_req'] = self.items[i].strength_req
				data_temp['agility_minus'] = self.items[i].agility_minus
				data_temp['speed_minus'] = self.items[i].speed_minus
			elif data_temp['class'] == "Clothes":
				data_temp['body_part'] = self.items[i].body_part
				data_temp['cold_protection'] = self.items[i].cold_protection
				data_temp['water_protection'] = self.items[i].water_protection
			elif data_temp['class'] == "Tool":
				pass
			elif data_temp['class'] == "Jewellery":
				data_temp['body_part'] = self.items[i].body_part
			elif data_temp['class'] == "Machine":
				pass
			elif data_temp['class'] == "Vehicle":
				data_temp['strength_req'] = self.items[i].strength_req
				data_temp['speed_minus'] = self.items[i].speed_minus
			elif data_temp['class'] == "Container":
				data_temp['capacity']  = self.items[i].capacity
				data_temp['for_liquids'] = self.items[i].for_liquids
			elif data_temp['class'] == "Furniture":
				data_temp['openable'] = self.items[i].openable
			elif data_temp['class'] == "Heap":
				pass
			data.append(data_temp)
		with open('save/items.json', 'w') as outfile:
			json.dump(data, outfile, indent=2)
			print("Poprawnie zapisano stan gry")

	
				


#DODATKOWE FUNKCJE
def set_items(path, location):
	items = []
	with open(path, "r", encoding='utf-8') as f:
		data = json.loads(f.read())
		for i in range(len(data)):
			class_name = data[i]['class']
			name = data[i]['name']
			description = data[i]['description']
			weight = data[i]['weight']
			price = data[i]['price']
			x = data[i]['x']
			y = data[i]['y']
			z = data[i]['z']
			loc = location
			#item_id = data[i]['id']
			if class_name == "Food":
				temp_item = Food(name, description, x, y, z, loc, weight, price, data[i]['nourish'], data[i]['stamina_suppl'])
				items.append(temp_item)
			elif class_name == "Drink": 
				temp_item = Drink(name, description, x, y, z, loc, weight, price, data[i]['nourish'], data[i]['stamina_suppl'], data[i]['alcohol'])
				items.append(temp_item)
			elif class_name == "Heals":
				temp_item = Heals(name, description, x, y, z, loc, weight, price, data[i]['hp_suppl'])
				items.append(temp_item)
			elif class_name == "Elixir":
				temp_item = Elixir(name, description, x, y, z, loc, weight, price, data[i]['duration'], hp_sup=data[i]["hp_sup"], st_av_sup=data[i]["st_av_sup"], st_sup=data[i]["st_sup"], mn_sup=data[i]["mn_sup"], str=data[i]["str"], agl=data[i]["agl"], spd=data[i]["spd"], dfc=data[i]["dfc"], per=data[i]["per"], stl=data[i]["stl"], hp_b=data[i]["hp_b"], mn_b=data[i]["mn_b"])
				items.append(temp_item)
			elif class_name == "CloseRange":
				temp_item = CloseRange(name, description, x, y, z, loc, weight, price, w_type=data[i]['type'], dm=data[i]['damage'], str_r=data[i]['strength_req'], agl_r=data[i]['agility_req'], skill_r=0, though=data[i]['thoughness'], cut=data[i]['cut'], stab=data[i]['stab'], crush=data[i]['crush'], block=data[i]['block'])
				items.append(temp_item)
			elif class_name == "Ranged":
				temp_item = Ranged(name, description, x, y, z, loc, weight, price, w_type=data[i]['type'], dm=data[i]['damage'], str_r=data[i]['strength_req'], agl_r=data[i]['agility_req'], skill_r=0, ammo_type=data[i]['ammo_type'], range=data[i]['range'])
				items.append(temp_item)   
			elif class_name == "Armor":
				temp_item = Armor(name, description, x, y, z, loc, weight, price, body=data[i]['body_part'], material=data[i]['material'], defe=data[i]['defence'], str_r=data[i]['strength_req'], agl_min=data[i]['agility_minus'], spd_min=data[i]['speed_minus'])
				items.append(temp_item)
			elif class_name == "Shield":
				temp_item = Shield(name, description, x, y, z, loc, weight, price, body=data[i]['body_part'], material=data[i]['material'], defe=data[i]['defence'], str_r=data[i]['strength_req'], agl_min=data[i]['agility_minus'], spd_min=data[i]['speed_minus'])
				items.append(temp_item)
			elif class_name == "Clothes":
				temp_item = Clothes(name, description, x, y, z, loc, weight, price, body=data[i]['body_part'], cold=data[i]['cold_protection'], water=data[i]['water_protection'])
				items.append(temp_item)
			elif class_name == "Tool":
				temp_item = Tool(name, description, x, y, z, loc, weight, price)
				items.append(temp_item)
			elif class_name == "Jewellery":
				temp_item = Jewellery(name, description, x, y, z, loc, weight, price, body=data[i]['body_part'])
				items.append(temp_item)
			elif class_name == "Machine":
				temp_item = Machine(name, description, x, y, z, loc, weight, price)
				items.append(temp_item)
			elif class_name == "Vehicle":
				temp_item = Vehicle(name, description, x, y, z, loc, weight, price, str_r=data[i]['strength_req'], spd_min=data[i]['speed_minus'])
				items.append(temp_item)
			elif class_name == "Container":
				temp_item = Container(name, description, x, y, z, loc, weight, price, capacity=data[i]['capacity'], liquids=data[i]['for_liquids'])
				items.append(temp_item)
			elif class_name == "Furniture":
				temp_item = Furniture(name, description, x, y, z, loc, weight, price, open=data[i]['openable'])
				items.append(temp_item)
			elif class_name == "Heap":
				temp_item = Heap(name, description, x, y, z, loc, weight, price)
				items.append(temp_item)
	return items
def item_name_convert(command):
	item_name = ""
	if len(command) == 1:
		return 0
	elif len(command) == 2:
		item_name = command[1]
	elif len(command) > 2:
		for x in range(len(command)-1):
			item_name = item_name+command[x+1]+' '
		item_name = item_name[:-1] #usuwa ostatni znak czyli spacje
	return item_name