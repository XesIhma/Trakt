from konsola import Konsola

class Square:
	def __init__(self, x, y, z, surf, name, desc, ids, **kwargs):
		self.x = x
		self.y = y
		self.z = z
		self.surface = surf
		#self.surfColor = self.surfColor(self.surface)
		self.name = name
		self.description = desc
		self.north = kwargs['n']
		self.northeast = kwargs['ne']
		self.east = kwargs['e']
		self.southeast = kwargs['se'] 
		self.south = kwargs['s']
		self.southwest = kwargs['sw']
		self.west = kwargs['w']
		self.northwest = kwargs['nw']
		self.up = kwargs['u']
		self.down = kwargs['d']
		self.doorN = None
		self.doorE = None
		self.doorS = None
		self.doorW = None
		self.doorU = None
		self.doorD = None
		self.itemIds = []
		self.itemIds = ids
		self.items = []
	def checkExit(self, direction):
		exits = {
			0: self.down,
			1: self.southwest,
			2: self.south,
			3: self.southeast,
			4: self.west,
			5: self.up,
			6: self.east,
			7: self.northwest,
			8: self.north,
			9: self.northeast
		}
		doors = {
			0: True,
			1: True,
			2: True,
			3: True,
			4: True,
			5: True,
			6: True,
			7: True,
			8: True,
			9: True
		}
		try: doors[0] = self.doorD.open
		except: pass
		try: doors[2] = self.doorS.open
		except: pass
		try: doors[4] = self.doorW.open
		except: pass
		try: doors[5] = self.doorU.open
		except: pass
		try: doors[6] = self.doorE.open
		except: pass
		try: doors[8] = self.doorN.open
		except: pass
			
		if direction in exits: 
			if exits[direction] == False:
				print("Nie da się tam przejść")
			elif exits[direction] and doors[direction] == False:
				komunikat = ["Drzwi nie dają się otworzyć", "Drzwi ani drgną", "Drzwi są zamknięte"]
				Konsola.printRandom(komunikat)
			return exits[direction]*doors[direction] #zwraca true w przypadku gdy oba są true, w pozostałych zwraca false
		else: 
			print("Nie da się tam przejść")
			return False
	def showSquare(self, world, mob):
		Konsola.print(self.name, "lyellow")
		Konsola.wrap(self.description, "lwhite")
		Konsola.compas(self, world, mob)
		for i in self.items:
			Konsola.print(i.name, "lcyan")
		for m in mob.currentLocation.mobs:
			if m.x == mob.x and m.y == mob.y and m.z == mob.z and m.id != 0:
				print("  ", end="")
				Konsola.print(m.name, "lmagenta")
	def addItem(self, item):
		self.items.append(item)
		self.itemIds.append(item.id)
	def removeItem(self, item):
		self.itemIds.remove(item.id)
		self.items.remove(item)