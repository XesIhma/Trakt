from konsola import Konsola
from mob import Mob
from item import Weapon, CloseRange, Ranged, Armor, Shield, Clothes, Tool, Jewellery, Machine, Vehicle, Container, Furniture, Heap

class Humanoid(Mob):
	def __init__(self, i, xx, yy, zz, n, a, d, sp, lft, itId, **kwargs):
		super(Humanoid, self).__init__(i, xx, yy, zz, n, a, d, sp, lft, itId, **kwargs)
		self.bodyPart = {
		"right_hand" : None,
		"left_hand" : None,
		"head" : None,
		"torso1" : None,
		"torso2" : None,
		"hands" : None,
		"legs" : None,
		"boots" : None,
		"finger1" : None,
		"finger2" : None,
		"neck" : None
		}
	def pickUp(self, item, info=False):
		if item.liftable:
			if item.weight + self.equipWeight() <= self.lift:
				self.equip.append(item)
				self.currentLocation.s[self.x][self.y][self.z].removeItem(item)
				if "upuść" not in item.actions: 
					item.actions.append("upuść")
				if "podnieś" in item.actions: 
					item.actions.remove("podnieś")
				self.weaking(0.2*item.weight, 0.4*item.weight)
				print(item.weight)
				if info: print("Podniosłeś "+ item.name) 
			elif item.weight > self.lift:
				if info: print("To jest dla ciebie za ciężkie") 
			else:
				if info: print("Twój ekwipunek waży za dużo. Wyrzuć coś innego aby to podnieść") 
		else:
			if info: print("Nie da się tego podnieść") 
	def drop(self, itemName, info=False):
		searchedItem = self.isInEq(itemName)
		if searchedItem:
			searchedItem.actions.append("podnieś")
			searchedItem.actions.remove("upuść")
			if info: print("Upuściłeś "+ searchedItem.name)
			self.equip.remove(searchedItem)
			self.currentLocation.s[self.x][self.y][self.z].addItem(searchedItem)
	def isInEq(self, itemName, info=False):
		hit = []
		for i in self.equip:
			for a in i.alias:
				if itemName == a:
					hit.append(i) 
		if len(hit) == 1:
			return hit[0]
		elif len(hit) > 1:
			if info: 
				Konsola.print("O którą rzecz Ci dokładnie chodzi?", "lred")
				return self.choseHit(hit)
			else:
				return hit[-1]
		else:
			if info: Konsola.print("Nie masz takiej rzeczy", "lred")
			return 0
	def showEquip(self):
		if len(self.equip) > 1:
			i = 0
			weight = 0
			for item in self.equip:
				item.display(i)
				weight += item.weight
				i+=1
			print("Waga ekwipunku: " + str(weight) + " funtów")
		elif len(self.equip) == 1:
			self.equip[0].display(0)
		else: 
			print("Ekwipunek jest pusty!")
	def travel(self, direction):
		if self.currentLocation.s[self.x][self.y][self.z].checkExit(direction):
			self.move(direction)
			factor = 1 + (self.equipWeight()/self.lift)
			self.weaking(0.1*factor)
			return True
	def equipWeight(self):
		equip_weight = 0
		for x in self.equip:
			equip_weight += x.weight
		return equip_weight
	def draw(self, thatItem, info=False):
		if isinstance(thatItem, Weapon):
			self.bodyPart["right_hand"] = thatItem
			if info: print("Wziąłeś do ręki "+thatItem.name)
		elif isinstance(thatItem, Shield):
			self.bodyPart["left_hand"] = thatItem
			if info: print("Wziąłeś do ręki "+thatItem.name)
		else:
			if info: print("To nie jest broń ani tarcza")
	def stow(self, thatItem, info=False):
		if self.bodyPart["right_hand"] == thatItem:
			self.bodyPart["right_hand"] = None
			if info: print("Schowałeś "+thatItem.name)
		elif self.bodyPart["left_hand"] == thatItem:
			self.bodyPart["left_hand"] = None
			if info: print("Schowałeś "+thatItem.name)
		else: 
			if info: print("Nie masz broni w ręce")
	def putOn(self, thatItem, info=False):
		if isinstance(thatItem, Armor):
			if thatItem.body_part == "head":
				self.bodyPart["head"] = thatItem
				if info: print("Założyłeś "+thatItem.name)
			elif thatItem.body_part == "hands":
				self.bodyPart["hands"] = thatItem
				if info: print("Założyłeś "+thatItem.name)
			elif thatItem.body_part == "torso1":
				self.bodyPart["torso1"] = thatItem
				if info: print("Założyłeś "+thatItem.name)
			elif thatItem.body_part == "torso2":
				self.bodyPart["torso2"] = thatItem
				if info: print("Założyłeś "+thatItem.name)
			elif thatItem.body_part == "legs":
				self.bodyPart["legs"] = thatItem
				if info: print("Założyłeś "+thatItem.name)
			elif thatItem.body_part == "boots":
				self.bodyPart["boots"] = thatItem
				if info: print("Założyłeś "+thatItem.name)
		elif isinstance(thatItem, Jewellery):
			if thatItem.body_part == "finger":
				if self.bodyPart["finger1"] is not None:
					if self.bodyPart["finger2"] is not None:
						if info: print("Masz już maksymalną liczbę pierścieni, zdjemij jeden")
					else:
						self.bodyPart["finger2"] = thatItem
						if info: print("Założyłeś "+thatItem.name)
				else: 
					self.bodyPart["finger1"] = thatItem
					if info: print("Założyłeś "+thatItem.name)
			elif thatItem.body_part == "neck":
				self.bodyPart["neck"] = thatItem
				if info: print("Założyłeś "+thatItem.name)
		else:
			if info: print("To nie jest pancerz ani biżuteria")

	def takeOff(self, thatItem, info=False):
		if self.bodyPart["right_hand"] == thatItem:
			self.bodyPart["right_hand"] = None
			if info: print("Schowałeś "+thatItem.name)
		elif self.bodyPart["head"] == thatItem:
			self.bodyPart["head"] = None
			if info: print("Zdjąłeś "+thatItem.name)
		elif self.bodyPart["torso1"] == thatItem:
			self.bodyPart["torso1"] = None
			if info: print("Zdjąłeś "+thatItem.name)
		elif self.bodyPart["torso2"] == thatItem:
			self.bodyPart["torso2"] = None
			if info: print("Zdjąłeś "+thatItem.name)
		elif self.bodyPart["hands"] == thatItem:
			self.bodyPart["hands"] = None
			if info: print("Zdjąłeś "+thatItem.name)
		elif self.bodyPart["legs"] == thatItem:
			self.bodyPart["legs"] = None
			if info: print("Zdjąłeś "+thatItem.name)
		elif self.bodyPart["boots"] == thatItem:
			self.bodyPart["boots"] = None
			if info: print("Zdjąłeś "+thatItem.name)
		elif self.bodyPart["finger1"] == thatItem:
			self.bodyPart["finger1"] = None
			if info: print("Zdjąłeś "+thatItem.name)
		elif self.bodyPart["finger2"] == thatItem:
			self.bodyPart["finger2"] = None
			if info: print("Zdjąłeś "+thatItem.name)
		elif self.bodyPart["neck"] == thatItem:
			self.bodyPart["neck"] = None
			if info: print("Zdjąłeś "+thatItem.name)
		else:
			if info: print("Nie masz tego na sobie")
	def dress(self, thatItem, info=False):
		if isinstance(thatItem, Clothes):
			if thatItem.body_part == "head":
				self.bodyPart["head"] = thatItem
				print("Ubrałeś "+thatItem.name)
			elif thatItem.body_part == "torso1":
				self.bodyPart["torso1"] = thatItem
				print("Ubrałeś "+thatItem.name)
			elif thatItem.body_part == "torso2":
				self.bodyPart["torso2"] = thatItem
				print("Ubrałeś "+thatItem.name)
			elif thatItem.body_part == "hands":
				self.bodyPart["hands"] = thatItem
				print("Ubrałeś "+thatItem.name)
			elif thatItem.body_part == "legs":
				self.bodyPart["legs"] = thatItem
				print("Ubrałeś "+thatItem.name)
			elif thatItem.body_part == "boots":
				self.bodyPart["boots"] = thatItem
				print("Ubrałeś "+thatItem.name)
			else:
				print("Nie masz czegoś takiego")
		else:
			print("To nie jest ubranie ani buty")
			
	def grab(self, thatItem, info=False):
		if isinstance(thatItem, Tool):
			self.bodyPart["right_hand"] = thatItem
			if info: print("Wziąłeś do ręki "+thatItem.name)
		else:
			print("To nie jest narzędzie")
		
	def drive(self, thatItem, info=False):
		if isinstance(thatItem, Vehicle):
			self.bodyPart["right_hand"] = thatItem
			self.bodyPart["left_hand"] = thatItem
			self.currentLocation.s[self.x][self.y][self.z].removeItem(thatItem)
			if info: print("Prowadzisz teraz "+thatItem.name)
		else:
			print("To nie jest pojazd")
	def leave(self, itemName, info=False):
		try:
			for a in self.bodyPart["right_hand"].alias:
				if itemName == a:
					thatItem = self.bodyPart["right_hand"]
					if isinstance(thatItem, Vehicle) and self.bodyPart["right_hand"] == thatItem:
						self.bodyPart["right_hand"] = None
						self.bodyPart["left_hand"] = None
						self.currentLocation.s[self.x][self.y][self.z].addItem(thatItem)
						if info: print("Zostawiłeś "+thatItem.name)
					else:
						print("To nie jest pojazd")
		except: print("Nie jeździsz czymś takim")
		