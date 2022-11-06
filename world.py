from location import Location

class World:
	def __init__(self, maps):
		self.x = 0
		self.y = 0
		self.location = []
		self.sizeX= 1
		self.sizeY = 1
		self.sizeZ = 1
		self.groundLevel = 0
		self.sSurf = []
		for i in range(len(maps)):
			temp_location = Location(maps[i])
			self.location.append(temp_location)
		for loc in self.location:
			if (loc.x + loc.sizeX) > self.sizeX:
				self.sizeX= loc.x + loc.sizeX
			if (loc.y + loc.sizeY) > self.sizeY:
				self.sizeY = loc.y + loc.sizeY
			if (self.sizeZ + loc.sizeZ - loc.groundLevel - 1) > self.sizeZ:
				self.sizeZ = self.sizeZ + loc.sizeZ - loc.groundLevel - 1 #kiedy nowa kratka wystaje w górę
			if loc.groundLevel > self.groundLevel:
				self.sizeZ += loc.groundLevel - self.groundLevel #kiedy nowa kratka wystaje w dół
				self.groundLevel = loc.groundLevel
		self.sSurf = [[[5 for k in range(self.sizeZ)] for j in range(self.sizeY)] for i in range(self.sizeX)]
		for loc in self.location:
			for x in range(loc.sizeX):
				for y in range(loc.sizeY):
					for z in range(loc.sizeZ):
						self.sSurf[loc.x+x][loc.y+y][self.groundLevel-loc.groundLevel+z] = loc.s[x][y][z].surface
						