from location import Location

class World:
	def __init__(self, maps):
		self.x = 0
		self.y = 0
		self.location = []
		length = len(maps)
		for i in range(length):
			temp_location = Location(maps[i])
			self.location.append(temp_location)
