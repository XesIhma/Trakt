from location import Location
from game import Game
import math
import json

class Being:
	def __init__(self):
		self.current_location = None
		self.x = 3
		self.y = 2
		self.z = 2
		self.name = "Istota"
		self.species = "Domyślna"
		self.param = {
			"hp" : 50,
			"hp_max" : 50,
			"stamina" : 50,
			"stamina_aviable" : 90,
			"stamina_max" : 100,
			"mana" : 5,
			"mana_max" : 10,
			"nourish" : 30,
			"nourish_max" : 50
		}
		self.stat = {
			"strength" : 10,
			"agility" : 10,
			"speed" : 5,
			"defence" : 10,
			"perceptivity" : 20,
			"visibility" : 5
		}
		self.skills = {
			"sword" : 5,
			"cudgel" : 5,
			"bow" : 2,
			"crossbow" : 0 
		}
		self.active_bonus = []
		self.lift = 50
		self.equip = []
	def toJSON(self):
		return json.dumps(self.__dict__)
	def travel(self, direction):
		if self.current_location.s[self.x][self.y][self.z].check_exit(direction):
			self.move_myself(direction)
			self.move_cost()
			self.travel_show()
	def move_myself(self, direction):
		if direction == 0:
			self.z-=1
		elif direction == 1:
			self.y+=1
			self.x-=1
		elif direction == 2:
			self.y+=1
		elif direction == 3:
			self.y+=1
			self.x+=1
		elif direction == 4:
			self.x-=1
		elif direction == 5:
			self.z+=1
		elif direction == 6:
			self.x+=1
		elif direction == 7:
			self.y-=1
			self.x-=1
		elif direction == 8:
			self.y-=1
		elif direction == 9:
			self.y-=1
			self.x+=1
	def move_cost(self):
		x=self.stat["strength"]
		y=0.1
		#cost= y - y*(-1*(pow(2,-1*((0.1*x)-2))+2)/4) ma dać wynik z przedziału 0d 0 do 0.5 dla strength od 10 do niesk
		cost= y*((pow(2,-1*((0.1*x)-2))+2)/4)
		self.param["stamina_aviable"]-=cost
		if self.param["stamina"] > self.param["stamina_aviable"]:
			self.param["stamina"] = self.param["stamina_aviable"]
	def travel_show(self):
		pass
	def compare_coords(self, other):
		if self.x == other.x and self.y == other.y and self.z == other.z and self.current_location == other.current_location:
			return True
		else: return False

	def get_hp(self):
		hp = self.param["hp"]
		return hp
	def stamina_(self):
		stamina = self.param["stamina"]
		#for key, value in self.bonus:
			#if 
		return stamina

	def whereami(self):
		print("{} - X: {} Y: {} Z: {}".format(self.name, self.x, self.y, self.z))
	def whoami(self):
		print("Imię/nazwa: {}, rasa: {}".format(self.name, self.species))
	def show_equip(self):
		if len(self.equip) > 1:
			i = 0
			for item in self.equip:
				item.display(i)
				i+=1
		elif len(self.equip) == 1:
			self.equip[0].display(0)
		else: 
			print("Ekwipunek jest pusty!")
	def pick_up(self, item):
		equip_weight = 0
		for x in self.equip:
			equip_weight += x.weight
		if item.weight + equip_weight <= self.lift:
			self.equip.append(item)
			item.z = -10
			item.actions.append("upuść")
			item.actions.remove("podnieś")
			print("Podniosłeś "+ item.name)
		else:
			print("Twój ekwipunek waży za dużo. Wyrzuć coś innego aby to podnieść")
	def drop(self, item_name):
		for i in self.equip:
			if i.name.lower() == item_name:
				i.x = self.x
				i.y = self.y
				i.z = self.z
				i.actions.append("podnieś")
				i.actions.remove("upuść")
				print("Upuściłeś "+ i.name)
				self.equip.remove(i)	
	def is_in_eq(self, item_name):
		flag = False
		for i in self.equip:
			if i.name.lower() == item_name:
				flag = True
		return False

