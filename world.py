from location import Location
from square import Square

class World:
	def __init__(self, maps):
		self.x = 0
		self.y = 0
		self.location = []
		self.size_x = 1
		self.size_y = 1
		self.size_z = 1
		self.ground_level = 0
		length = len(maps)
		for i in range(length):
			temp_location = Location(maps[i])
			self.location.append(temp_location)
		for loc in self.location:
			if loc.ground_level > self.ground_level:
				self.ground_level = loc.ground_level
			if (loc.x + loc.size_x) > self.size_x:
				self.size_x = loc.x + loc.size_x
			if (loc.y + loc.size_y) > self.size_y:
				self.size_y = loc.y + loc.size_y
			if (loc.size_z - loc.ground_level) > self.size_z:
				self.size_z = loc.size_z - loc.ground_level + self.ground_level
		self.s = [[[Square(i, j, k, 1, "Pustka", "Nic tu nie ma", n=1,ne=1,e=1,se=1,s=1,sw=1,w=1,nw=1,u=1,d=1) for k in range(self.size_z)] for j in range(self.size_y)] for i in range(self.size_x)]
		for loc in self.location:
			for x in range(loc.size_x):
				for y in range(loc.size_y):
					for z in range(loc.size_z):
						self.s[loc.x+x][loc.y+y][self.ground_level-loc.ground_level+z] = loc.s[x][y][z]
	
	def show_location(self, x, y, z):
		self.s[x][y][z].show_content(self)
