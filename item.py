from konsola import Konsola

class Item:
	id = 0
	@classmethod
	def increment_ID(cls):
		cls.id += 1 
		return cls.id
	def __init__(self, itemId, n, ali, desc, w, price):
		if itemId == -1:
			self.id=Item.increment_ID()
		else:
			Item.increment_ID()
			self.id = itemId
		self.exist = True
		self.name = n
		self.alias = ali
		self.description = desc
		self.liftable = True
		self.owner = None
		self.weight = w
		self.condition = 1
		self.price = price
		self.actions = ["zobacz", "podnieś"]
	def see(self):
		Konsola.print(self.name, "cyan")
		print(self.description)
		print(self.id)
	def possible_actions(self):
		print("Możliwe dzałania: ")
		for x in self.actions:
			print(" - {}".format(x))
	def display(self, i):
		if i == 0:
			print("|lp.| NAZWA               | WAGA|")
		print("|{:<3}| {:<20}| {:4}|".format(i+1, self.name, self.weight))
	def compare_coords(self, other):
		if self.x == other.x and self.y == other.y and self.z == other.z and self.current_location == other.current_location:
			return True
		else: return False
	def get_name(self):
		name = self.name
		return name

class Consumable(Item):
	def __init__(self, itemId, n, ali, desc, w, price):
		super(Consumable, self).__init__(itemId, n, ali, desc, w, price)
		self.actions.append("użyj")
	def use(self, mob):
		pass

class Food(Consumable):
	def __init__(self, itemId, n, ali, desc, w, price, **kwargs):
		super(Food, self).__init__(itemId, n, ali, desc, w, price)
		self.nourish = kwargs.get("nou", 5)
		self.stamina_suppl = kwargs.get("st_sup", 0)
		self.quality = kwargs.get("quality", 100)
		self.actions.remove("użyj")
		self.actions.append("zjedz")
	def use(self, mob, info=False):
		mob.param["nourish"]+=self.nourish
		mob.param["stamina"]+=self.stamina_suppl
		if mob.param["nourish"] > mob.param["nourish_max"]:
			mob.param["nourish"] = mob.param["nourish_max"]
			if info: print("Zjadłeś za dużo!")
		if info: print("Zjadłeś "+self.name)
		mob.equip.remove(self)

class Drink(Consumable):
	def __init__(self, itemId, n, ali, desc, w, price, **kwargs):
		super(Drink, self).__init__(itemId, n, ali, desc, w, price)
		self.nourish = kwargs.get("nou", 5)
		self.stamina_suppl = kwargs.get("st_sup", 0)
		self.alcohol = kwargs.get("alc", 0)
		self.quality = kwargs.get("quality", 100)
		self.actions.remove("użyj")
		self.actions.append("wypij")
	def use(self, mob, info):
		mob.param["nourish"]+=self.nourish
		mob.param["stamina"]+=self.stamina_suppl
		if mob.param["nourish"] > mob.param["nourish_max"]:
			surplus = mob.param["nourish"] - mob.param["nourish_max"]
			mob.param["stamina"] -= surplus
			mob.param["stamina_aviable"] -= surplus/2
			mob.param["nourish"] = mob.param["nourish_max"]
			if info: print("Wypiłeś za dużo!")
		if info: print("Wypiłeś "+self.name)
		mob.equip.remove(self)

class Heals(Consumable):
	def __init__(self, itemId, n, ali, desc, w, price, **kwargs):
		super(Heals, self).__init__(itemId, n, ali, desc, w, price)
		self.hp_suppl = kwargs.get("hp_sup", 0)
	def use(self, mob, info=False):
		mob.param["hp"]+=self.hp_suppl
		if mob.param["hp"] > mob.param["hp_max"]:
			mob.param["hp"] = mob.param["hp_max"]
		if info: print("Użyłeś "+self.name)

class Elixir(Consumable):
	def __init__(self, itemId, n, ali, desc, w, price, **kwargs):
		super(Elixir, self).__init__(itemId, n, ali, desc, w, price)
		self.bonus = {}

		self.function = kwargs.get("function", None)

		self.hp_suppl = kwargs.get("hp_sup", 0)
		self.stamina_aviable_suppl = kwargs.get("st_av_sup", 0)
		self.stamina_suppl = kwargs.get("st_sup", 0)
		self.mana_suppl = kwargs.get("mn_sup", 0)
		self.bonus["strength"] = kwargs.get("str", 0)
		self.bonus["agility"] = kwargs.get("agl", 0)
		self.bonus["speed"] = kwargs.get("spd", 0)
		self.bonus["defence"] = kwargs.get("dfc", 0)
		self.bonus["perceptivity"]  = kwargs.get("per", 0)
		self.bonus["stealth"] = kwargs.get("stl", 0)
		self.bonus["hp"] = kwargs.get("hp_b", 0)
		self.bonus["mana"] = kwargs.get("str", 0)
		self.duration = kwargs.get("duration", 0)
	def use(self, mob, info=False):
		if self.hp_suppl: 
			mob.param["hp"]+=self.hp_suppl
			if mob.param["hp"] > mob.param["hp_max"]:
				mob.param["hp"] = mob.param["hp_max"]
		if self.stamina_aviable_suppl: 
			mob.param["stamina"]+=self.stamina_aviable_suppl
			if mob.param["stamina_aviable"] > mob.param["stamina_max"]:
				mob.param["stamina_aviable"] = mob.param["stamina_max"]
		if self.stamina_suppl: 
			mob.param["stamina"]+=self.stamina_suppl
			if mob.param["stamina"] > mob.param["stamina_aviable"]:
				mob.param["stamina"] = mob.param["stamina_aviable"]
		if self.mana_suppl: 
			mob.param["mana"]+=self.mana_suppl
			if mob.param["mana"] > mob.param["mana_max"]:
				mob.param["mana"] = mob.param["mana_max"]
				
		if self.bonus["strength"]: mob.activeBonus.append(["strength", self.bonus["strength"], self.duration])
		if self.bonus["agility"]: mob.activeBonus.append(["agility", self.bonus["agility"], self.duration])
		if self.bonus["speed"]: mob.activeBonus.append(["speed", self.bonus["speed"], self.duration])
		if self.bonus["defence"]: mob.activeBonus.append(["defence", self.bonus["defence"], self.duration])
		if self.bonus["perceptivity"]: mob.activeBonus.append(["perceptivity", self.bonus["perceptivity"], self.duration])
		if self.bonus["stealth"]: mob.activeBonus.append(["stealth", self.bonus["stealth"], self.duration])
		if self.bonus["hp"]: mob.activeBonus.append(["hp", self.bonus["hp"], self.duration])
		if self.bonus["mana"]: mob.activeBonus.append(["mana", self.bonus["mana"], self.duration])

		if info: print("Wypiłeś "+self.name)
		mob.equip.remove(self)

class Weapon(Item):
	def __init__(self, itemId, n, ali, desc, w, price, **kwargs):
		super(Weapon, self).__init__(itemId, n, ali, desc, w, price)
		self.actions.append("dobądź")
		self.type = kwargs.get("type", "weapon")
		self.damage = kwargs.get("damage", 10)
		self.strength_req = kwargs.get("strength_req", 5)
		self.agility_req = kwargs.get("agility_req", 5)

class CloseRange(Weapon):
	def __init__(self, itemId, n, ali, desc, w, price, **kwargs):
		super(CloseRange, self).__init__(itemId, n, ali, desc, w, price, **kwargs) 
		self.condition = kwargs.get("condition", 100)
		self.durability = kwargs.get("durability", 90)
		self.cut = kwargs.get("cut", 34)
		self.stab = kwargs.get("stab", 33)
		self.crush = kwargs.get("crush", 33)
		self.block = kwargs.get("block", 5)

class Ranged(Weapon):
	def __init__(self, itemId, n, ali, desc, w, price, **kwargs):
		super(Ranged, self).__init__(itemId, n, ali, desc, w, price, **kwargs)       
		self.ammo_type = kwargs.get("ammo_type", "arrows") #arrows, bolt, rock
		self.range = kwargs.get("range", 20) #10 to jedna kratka

class Armor(Item):
	def __init__(self, itemId, n, ali, desc, w, price, **kwargs):
		super(Armor, self).__init__(itemId, n, ali, desc, w, price)
		self.actions.append("załóż")
		self.body_part = kwargs.get("body_part", 5) #head, torso, legs, arms, hands, feet, shoulders, shield
		self.material = kwargs.get("material", 5)
		self.defence = kwargs.get("defence", 5)
		self.strength_req = kwargs.get("strength_req", 5)
		self.agility_minus = kwargs.get("agility_minus", 5)
		self.speed_minus = kwargs.get("speed_minus", 5)

class Shield(Armor):
	def __init__(self, itemId, n, ali, desc, w, price, **kwargs):
		super(Shield, self).__init__(itemId, n, ali, desc, w, price, **kwargs)
		self.condition = kwargs.get("condition", 100)
		self.durability = kwargs.get("durability", 90)
		self.actions.remove("załóż")
		self.actions.append("dobądź")

class Clothes(Item):
	def __init__(self, itemId, n, ali, desc, w, price, **kwargs):
		super(Clothes, self).__init__(itemId, n, ali, desc, w, price)
		self.actions.append("ubierz")
		self.body_part = kwargs.get("body_part", 5)
		self.cold_protection = kwargs.get("cold_protection", 30)
		self.water_protection = kwargs.get("water_protection", 5)

class Tool(Item):
	def __init__(self, itemId, n, ali, desc, w, price, **kwargs):
		super(Tool, self).__init__(itemId, n, ali, desc, w, price)
		self.actions.append("dobądź")
		self.function = kwargs.get("function", None)

class Jewellery(Item):
	def __init__(self, itemId, n, ali, desc, w, price, **kwargs):
		super(Jewellery, self).__init__(itemId, n, ali, desc, w, price)
		self.actions.append("załóż")
		self.body_part = kwargs.get("body_part", 5) #finger, wrist, neck, forehead, hair

class Machine(Item):
	def __init__(self, itemId, n, ali, desc, w, price, **kwargs):
		super(Machine, self).__init__(itemId, n, ali, desc, w, price)
		self.actions.remove("podnieś")
		self.actions.append("użyj")
		self.liftable = False
		self.function = kwargs.get("function", None)

class Vehicle(Item):
	def __init__(self, itemId, n, ali, desc, w, price, **kwargs):
		super(Vehicle, self).__init__(itemId, n, ali, desc, w, price)
		self.actions.append("prowadź")
		self.actions.remove("podnieś")
		self.liftable = False
		self.strength_req = kwargs.get("strength_req", 5)
		#self.capacity = kwargs["capacity"]
		#self.stored = None
		self.speed_minus = kwargs.get("speed_minus", 20)

class Container(Item):
	def __init__(self, itemId, n, ali, desc, w, price, **kwargs):
		super(Container, self).__init__(itemId, n, ali, desc, w, price)
		self.capacity = kwargs.get("capacity", 5)
		self.liftable = False
		self.current_amount = 0
		self.for_liquids = kwargs.get("liquids",False)
		self.stored = None
	def fill(self, source, substance, quantity):
		if substance.type == "liquid" and self.for_liquids == False:
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
	def __init__(self, itemId, n, ali, desc, w, price, **kwargs):
		super(Furniture, self).__init__(itemId, n, ali, desc, w, price)
		self.actions.append("podejdź do")
		self.liftable = False
		self.openable = kwargs.get("open",False)
		self.function = kwargs.get("function", None) #table, bed
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
		if self.openable: print("Możesz otworzyć, żeby zajrzeć do środka")
	def open(self):
		if not self.openable:
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
	def __init__(self, itemId, n, ali, desc, w, price):
		super(Heap, self).__init__(itemId, n, ali, desc, w, price)
		self.actions.append("podejdź")
		self.liftable = False
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

class DeadBody(Item):
	def __init__(self, itemId, n, ali, desc, w, price):
		super(DeadBody, self).__init__(itemId, n, ali, desc, w, price)
		self.actions.append("sekcja")
