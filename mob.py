import random
from konsola import Konsola
from item import DeadBody

class Mob:
	id = 0
	@classmethod
	def increment_ID(cls):
		cls.id += 1 
		return cls.id
	def __init__(self, mobId, xx, yy, zz, n, a, d, sp, lft, itId, **kwargs):
		if mobId == -1:
			self.id=Mob.increment_ID()
		else:
			Mob.increment_ID()
			self.id = mobId
		self.currentLocation = None
		self.x = xx
		self.y = yy
		self.z = zz
		self.name = n
		self.deadBody = "Zwłoki " + self.name
		self.alias = a
		self.description = d
		self.species = sp
		self.param = {
			"hp" : kwargs.get("hp", 50),
			"hp_max" : kwargs.get("hp_max", 5),
			"stamina" : kwargs.get("st", 100),
			"stamina_aviable" : kwargs.get("st_av", 100),
			"stamina_max" : kwargs.get("st_max", 100),
			"mana" : kwargs.get("mn", 0),
			"mana_max" : kwargs.get("mn_max", 0),
			"nourish" : kwargs.get("nou", 50),
			"nourish_max" : kwargs.get("nou_max", 50),
		}
		self.stat = {
			"strength" : kwargs.get("str", 5),
			"agility" : kwargs.get("agl", 5),
			"speed" : kwargs.get("spd", 5),
			"defence" : kwargs.get("dfc", 5),
			"perceptivity" : kwargs.get("per", 5),
			"visibility" : kwargs.get("vis", 5)
		}
		self.weapons = {
			"sword" : kwargs.get("sword", 5),
			"axe" : kwargs.get("axe", 5),
			"spear" : kwargs.get("spear", 5),
			"cudgel" : kwargs.get("cudgel", 5),
			"bow" : kwargs.get("bow", 2)
		}
		self.defence = {
			"cut" : kwargs.get("dfc_cut", self.stat["defence"]),
			"stab" : kwargs.get("dfc_stab", self.stat["defence"]),
			"crush" : kwargs.get("dfc_crush", self.stat["defence"]),
			"fire" : kwargs.get("dfc_fire", self.stat["defence"]),
			"ice" : kwargs.get("dfc_ice", self.stat["defence"]),
			"magic" : kwargs.get("dfc_magic", 0)
		}
		self.activeBonus = []
		self.lift = lft
		self.itemIds = []
		self.itemIds = itId
		self.equip = []
		self.fainted = False
		self.dead = False

	# f(x) = (-1.375x + 100) / 100 daje 100% dla x = 0 i 30% dla x = 50
	def getStrength(self):
		strength = self.stat["strength"]
		try:
			for b in self.bodyPart:
				try: 
					if b.strength_req > self.stat["strength"]:
						strength -= b.strength_req - self.stat["strength"]
				except: pass
		except: pass
		return strength
	def getAgility(self):
		agility = self.stat["agility"]
		try:
			for b in self.bodyPart:
				try: agility -= b.agility_minus 
				except: pass
				try: 
					if b.agility_req > self.stat["agility"]:
						agility -= b.agility_req - self.stat["agility"]
				except: pass
		except: pass
		return agility
	def getSpeed(self):
		speed = self.stat["speed"]
		try:
			for b in self.bodyPart:
				try:
					speed -= b.speed_minus
				except: pass
		except: pass
		return speed
	def travel(self, direction):
		if self.currentLocation.s[self.x][self.y][self.z].checkExit(direction):
			self.move(direction)
			self.weaking(0.1, -0.05)
			return True
	def move(self, direction):
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
	def whereami(self):
		print("{} - X: {} Y: {} Z: {}".format(self.name, self.x, self.y, self.z))
		print(self.currentLocation.name)
	def whoami(self):
		print(self.name)
		print(self.description)
		print(self.species)
	def weaking(self, val1, val2=0, info=True):
		x=self.stat["strength"]
		cost1= val1 - val1*(1-((pow(2,-1*((0.1*x)-2))+2)/4))
		cost2= val2 - val2*(1-((pow(2,-1*((0.1*x)-2))+2)/4))
		self.param["stamina_aviable"]-=cost1
		self.param["stamina"]-=cost2
		if self.param["stamina_aviable"] > self.param["stamina_max"]:
			self.param["stamina_aviable"] = self.param["stamina_max"]
		if self.param["stamina"] > self.param["stamina_aviable"]:
			self.param["stamina"] = self.param["stamina_aviable"]
		if self.param["stamina"] <=0:
			if info:print("Straciłeś przytomność z wyczerpania")
			self.param["stamina"] = 0
			self.fainted = True
	def kill(self, mob):
		#sprawdzam w czym mob jest najlepszy i dobywa taką broń jeśli ma
		try: 
			weapons=list(mob.weapons.items())
			weapons=sorted(weapons, key = lambda x:x[1], reverse=True)#sortowanie po wartości
			for s in weapons:
				weapon = mob.isInEq(s[0])
				if weapon:
					mob.draw(weapon)
					komunikat = mob.name + " dobywa " + weapon.name
					Konsola.print(komunikat, "lyellow")
					break
		except: pass
		howLong = 0

		self.timeFactor = (-1.375*self.getSpeed() + 100) / 100
		mob.timeFactor = (-1.375*mob.getSpeed() + 100) / 100

		hit = 10
		block = 5
		crit = 20

		queue = {
			1 : self.hit,
			10 : mob.hit,
			20 : self.hit,
			30 : self.hit,
			35 : mob.hit
		}
		while self.param["hp"] > 0 and mob.param["hp"] > 0 and self.param["stamina"] > 0 and mob.param["stamina"] > 0:
			print("")
			Konsola.prompt(self, False)
			damage = self.hit(mob)
			if damage:
				print("Zadałeś "+mob.name.upper()+" "+str(damage)+" obrażeń")
			else:
				print("Chybiłeś")
			howLong+=20
			
			condition = int((mob.param["hp"] / mob.param["hp_max"])*100)
			if condition < 0: condition = 0
			text = "{ "+ str(condition)+" } "
			Konsola.print(text, "red", "reset", "")
			if mob.param["hp"] > 0 and mob.param["stamina"] > 0:
				damage = mob.hit(self)
				if damage:
					print(mob.name.upper()+" zadał Ci "+str(damage)+" obrażeń")
				else:
					print(mob.name.upper()+" Chybia")
			howLong+=20
			# iterator = 0
			# while True:
			# 	pass


		if self.param["hp"] > 0:
			print("Zabiłeś "+mob.name.upper())
			mob.die()
		if self.param["hp"] <= 0:
			self.param["hp"] = 0
			self.dead = True
			print("Zostałeś zabity przez "+mob.name.upper())
		return howLong
	def hit(self, mob):
		chance = random.randint(0, 100)
		chance += self.stat["agility"]
		if chance > 50:
			damageMultiplexer = random.randint(0, 100) / 100
			damage = damageMultiplexer * self.stat["strength"]
			try:
				damageMultiplexer = random.randint(0, 100) / 100
				damage += damageMultiplexer * self.bodyPart["right_hand"].damage
			except: pass

			damage = round(damage, 2)
			mob.param["hp"] -= damage
			self.weaking(2, 8, False)
			return damage
	def die(self):
		deadBody = DeadBody(self.deadBody, "Martwe ciało", ["truchło", "truchlo", "zwłoki", "zwloki", "ciało", "cialo"], self.description, self.param["hp_max"]/3, 0)
		self.currentLocation.s[self.x][self.y][self.z].addItem(deadBody)
		for i in self.equip:
			self.currentLocation.s[self.x][self.y][self.z].addItem(i)
		self.currentLocation.mobs.remove(self)

	def coordComp(self, that):
		if self.x == that.x and self.y == that.y and self.z == that.z and self.currentLocation == that.currentLocation:
			return 1
		else: return 0
