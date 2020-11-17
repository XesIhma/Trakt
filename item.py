from colorama import Fore, Back, Style
from items_dict import all_items

class Item:
	id = 0
	@classmethod
	def increment_ID(cls):
		cls.id += 1 
		return cls.id
	#@classmethod
	#def check(cls, attr):
		#if isinstance(attr, list):
			#for x in attr:
	def __init__(self, n, desc, x, y, z, loc, w, price):
		self.id=Item.increment_ID()
		self.exist = True
		self.name = n
		self.full_name = n
		self.description = desc
		self.is_static = False
		self.owner = None
		being = None
		self.x = x
		self.y = y
		self.z = z
		self.current_location = loc
		self.weight = w
		self.condition = 1
		self.price = price
		self.actions = ["zobacz", "podnieś"]
		#print("ID {}".format(Item.id))
	def see(self):
		print(Fore.BLUE + Style.BRIGHT + self.name + Style.RESET_ALL)
		print(self.description)
	def possible_actions(self):
		print("Możliwe dzałania: ")
		for x in self.actions:
			print(" - {}".format(x))
	def display(self, i):
		if i == 0:
			print("|lp.| NAZWA          | WAGA|")
			print("----------------------------")
		print("|{:<3}| {:<15}| {:4}|".format(i+1, self.name, self.weight))
	def compare_coords(self, other):
		if self.x == other.x and self.y == other.y and self.z == other.z and self.current_location == other.current_location:
			return True
		else: return False
	def get_name(self):
		name = self.name
		return name
class Consumable(Item):
	def __init__(self, n, desc, x, y, z, loc, w, price):
		super(Consumable, self).__init__(n, desc, x, y, z, loc, w, price)
		self.actions.append("użyj")
	def use(self, being):
		pass

class Food(Consumable):
	def __init__(self, n, desc, x, y, z, loc, w, price, nou, st_sup):
		super(Food, self).__init__(n, desc, x, y, z, loc, w, price)
		self.nourish = nou
		self.stamina_suppl = st_sup
		self.quality = 100
		self.actions.remove("użyj")
		self.actions.append("zjedz")
	def use(self, being, info):
		being.param["nourish"]+=self.nourish
		being.param["stamina"]+=self.stamina_suppl
		if being.param["nourish"] > being.param["nourish_max"]:
			#surplus = being.param["nourish"] - being.param["nourish_max"]
			#being.param["stamina"] -= surplus
			#being.param["stamina_aviable"] -= surplus/2
			being.param["nourish"] = being.param["nourish_max"]
			if info:
				print("Zjadłeś za dużo!")
		if info:
			print("Zjadłeś "+self.name)

class Drink(Consumable):
	def __init__(self, n, desc, x, y, z, loc, w, price, nou, st_sup, alc):
		super(Drink, self).__init__(n, desc, x, y, z, loc, w, price)
		self.nourish = nou
		self.stamina_suppl = st_sup
		self.alcohol = alc
		self.quality = 100
		self.actions.remove("użyj")
		self.actions.append("wypij")
	def use(self, being, info):
		being.param["nourish"]+=self.nourish
		being.param["stamina"]+=self.stamina_suppl
		if being.param["nourish"] > being.param["nourish_max"]:
			surplus = being.param["nourish"] - being.param["nourish_max"]
			being.param["stamina"] -= surplus
			being.param["stamina_aviable"] -= surplus/2
			being.param["nourish"] = being.param["nourish_max"]
			if info:
				print("Wypiłeś za dużo!")
		if info:
			print("Wypiłeś "+self.name)

class Heals(Consumable):
	def __init__(self, n, desc, x, y, z, loc, w, price, hp_sup):
		super(Heals, self).__init__(n, desc, x, y, z, loc, w, price)
		self.hp_suppl = hp_sup
	def use(self, being, info):
		being.param["hp"]+=self.hp_suppl
		if being.param["hp"] > being.param["hp_max"]:
			being.param["hp"] = being.param["hp_max"]

class Elixir(Consumable):
	def __init__(self, n, desc, x, y, z, loc, w, price, dur, **kwargs):
		super(Elixir, self).__init__(n, desc, x, y, z, loc, w, price)
		self.bonus = {}
		if "hp_sup" in kwargs: self.hp_suppl = kwargs["hp_sup"]
		if "st_av_sup" in kwargs: self.stamina_aviable_suppl = kwargs["st_av_sup"]
		if "st_sup" in kwargs: self.stamina_suppl = kwargs["st_sup"]
		if "mn_sup" in kwargs: self.mana_suppl = kwargs["mn_sup"]
		if "str" in kwargs: self.bonus["strength"] = kwargs["str"]
		if "agl" in kwargs: self.bonus["agility"] = kwargs["agl"]
		if "spd" in kwargs: self.bonus["speed"] = kwargs["spd"]
		if "dfc" in kwargs: self.bonus["defence"] = kwargs["dfc"]
		if "per" in kwargs: self.bonus["perceptivity"] = kwargs["per"]
		if "stl" in kwargs: self.bonus["stealth"] = kwargs["stl"]
		if "hp_b" in kwargs: self.bonus["hp"] = kwargs["hp_b"]
		if "mn_b" in kwargs: self.bonus["mana"] = kwargs["mn_b"]
		self.duration = dur
	def use(self, being, info):
		if self.hp_suppl: 
			being.param["hp"]+=self.hp_suppl
			if being.param["hp"] > being.param["hp_max"]:
				being.param["hp"] = being.param["hp_max"]
		if self.stamina_aviable_suppl: 
			being.param["stamina"]+=self.stamina_aviable_suppl
			if being.param["stamina_aviable"] > being.param["stamina_max"]:
				being.param["stamina_aviable"] = being.param["stamina_max"]
		if self.stamina_suppl: 
			being.param["stamina"]+=self.stamina_suppl
			if being.param["stamina"] > being.param["stamina_aviable"]:
				being.param["stamina"] = being.param["stamina_aviable"]
		if self.mana_suppl: 
			being.param["mana"]+=self.hp_suppl
			if being.param["mana"] > being.param["mana_max"]:
				being.param["mana"] = being.param["mana_max"]
				
		if self.bonus["strength"]: being.active_bonus.append(["strength", self.bonus["strength"], self.duration])
		if self.bonus["agility"]: being.active_bonus.append(["agility", self.bonus["agility"], self.duration])
		if self.bonus["speed"]: being.active_bonus.append(["speed", self.bonus["speed"], self.duration])
		if self.bonus["defence"]: being.active_bonus.append(["defence", self.bonus["defence"], self.duration])
		if self.bonus["perceptivity"]: being.active_bonus.append(["perceptivity", self.bonus["perceptivity"], self.duration])
		if self.bonus["visibility"]: being.active_bonus.append(["visibility", self.bonus["visibility"], self.duration])
		if self.bonus["hp"]: being.active_bonus.append(["hp", self.bonus["hp"], self.duration])
		if self.bonus["mana"]: being.active_bonus.append(["mana", self.bonus["mana"], self.duration])

class Weapon(Item):
	def __init__(self, n, desc, x, y, z, loc, w, price, **kwargs):
		super(Weapon, self).__init__(n, desc, x, y, z, loc, w, price)
		self.actions.append("dobądź")
		self.type = kwargs['w_type']
		self.damage = kwargs["dm"]
		self.strength_req = kwargs["str_r"]
		self.agility_req = kwargs["agl_r"]
		self.skill_req = kwargs["skill_r"]
	#def grab

class CloseRange(Weapon):
	def __init__(self, n, desc, x, y, z, loc, w, price, **kwargs):
		super(CloseRange, self).__init__(n, desc, x, y, z, loc, w, price, **kwargs) 
		self.thoughness = kwargs["though"]
		self.cut = kwargs["cut"]
		self.stab = kwargs["stab"]
		self.crush = kwargs["crush"]
		self.block = kwargs['block']

class Ranged(Weapon):
	def __init__(self, n, desc, x, y, z, loc, w, price, **kwargs):
		super(Ranged, self).__init__(n, desc, x, y, z, loc, w, price, **kwargs)       
		self.ammo_type = kwargs['ammo_type']
		self.range = kwargs['range'] #10 to jedna kratka

class Armor(Item):
	def __init__(self, n, desc, x, y, z, loc, w, price, **kwargs):
		super(Armor, self).__init__(n, desc, x, y, z, loc, w, price)
		self.actions.append("załóż")
		self.body_part = kwargs["body"] #head, chest, legs, arms, hands, feet, shoulders, shield
		self.material = kwargs["material"]
		self.defence = kwargs["defe"]
		self.strength_req = kwargs["str_r"]
		self.agility_minus = kwargs["agl_min"]
		self.speed_minus = kwargs["spd_min"]
	#def put_on
class Shield(Armor):
	def __init__(self, n, desc, x, y, z, loc, w, price, **kwargs):
		super(Shield, self).__init__(n, desc, x, y, z, loc, w, price)
		self.actions.append("dobądź")
		self.body_part = kwargs["body"]

class Clothes(Item):
	def __init__(self, n, desc, x, y, z, loc, w, price, **kwargs):
		super(Clothes, self).__init__(n, desc, x, y, z, loc, w, price)
		self.actions.append("ubierz")
		self.body_part = kwargs["body"]
		self.cold_protection = kwargs["cold"]
		self.water_protection = kwargs["water"]
	#def dress_up

class Tool(Item):
	def __init__(self, n, desc, x, y, z, loc, w, price, **kwargs):
		super(Tool, self).__init__(n, desc, x, y, z, loc, w, price)
		self.task = []

class Jewellery(Item):
	def __init__(self, n, desc, x, y, z, loc, w, price, **kwargs):
		super(Jewellery, self).__init__(n, desc, x, y, z, loc, w, price)
		self.actions.append("załóż")
		self.body_part = kwargs["body"] #finger, wrist, neck, forehead, hair

class Machine(Item):
	def __init__(self, n, desc, x, y, z, loc, w, price, **kwargs):
		super(Machine, self).__init__(n, desc, x, y, z, loc, w, price)
		#components

class Vehicle(Item):
	def __init__(self, n, desc, x, y, z, loc, w, price, **kwargs):
		super(Vehicle, self).__init__(n, desc, x, y, z, loc, w, price)
		self.actions.append("prowadź")
		self.strength_req = kwargs["str_r"]
		#self.capacity = kwargs["capacity"]
		#self.stored = None
		self.speed_minus = kwargs["spd_min"]

class Container(Item):
	def __init__(self, n, desc, x, y, z, loc, w, price, **kwargs):
		super(Container, self).__init__(n, desc, x, y, z, loc, w, price)
		self.capacity = kwargs["capacity"]
		self.current_amount = 0
		self.for_liquids = kwargs.get("liquids",False)
		self.stored = None
	def fill(self, source, substance, quantity):
		if substance.type == "liquid" and self.for_liquids == false:
			print("Nie możesz tego tu wlać, znajdź jakiś szczelny pojemnik")
			return
		if not substance.name == self.stored.name:
			print("Nie możesz mieszać różnych rzeczy w tym pojemniku")
			return
		if quantity + self.current_amount > self.capacity:
			taken = self.capacity - self.current_amount
			self.current_amount = self.capacity
			source -= taken
		else: self.current_amount += quantity

class Furniture(Item):
	def __init__(self, n, desc, x, y, z, loc, w, price, **kwargs):
		super(Furniture, self).__init__(n, desc, x, y, z, loc, w, price)
		self.actions.append("podejdź do")
		self.openable = kwargs.get("open",False)
		self.content_on_top = []
		if self.openable:
			self.content_inside = []
			self.actions.append("otwórz")
		def come_closer(self):
			print(self.description)
			if len(self.content_on_top) > 1:
				print("Leży tu kilka rzeczy: ")
				i = 0
				for item in self.content_on_top:
					item.display(i)
					i+=1
			elif len(self.content_on_top) == 1:
				print("Leży tu:")
				self.content_on_top[0].display(0)
			if openable: print("Możesz otworzyć, żeby zajrzeć do środka")
		def open(self):
			if not openable:
				print("Nie da się tego otworzyć")
				return
			if len(self.content_inside) > 1:
				print("Leży tu kilka rzeczy: ")
				i = 0
				for item in self.content_inside:
					item.display(i)
					i+=1
			elif len(self.content_inside) == 1:
				print("Leży tu:")
				self.content_inside[0].display(0)

class Heap(Item):
	def __init__(self, n, desc, x, y, z, loc, w, price, **kwargs):
		super(Container, self).__init__(n, desc, x, y, z, loc, w, price)
		self.actions.append("podejdź do")
		self.content = []
		def come_closer(self):
			print(self.description)
			if len(self.content_on_top) > 1:
				print("Leżą tu: ")
				i = 0
				for item in self.content_on_top:
					item.display(i)
					i+=1
			elif len(self.content_on_top) == 1:
				print("Leży tu:")
				self.content_on_top[0].display(0)

