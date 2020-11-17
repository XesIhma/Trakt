from square import Square
import json

class Location:
	def __init__(self, file_path):
		self.name = "Nigdzie"
		self.x = 0
		self.y = 0
		self.size_x = 1
		self.size_y = 1
		self.size_z = 1
		self.ground_level = 0
		self.s = None

		with open(file_path, "r", encoding='utf-8') as f:
			data = json.loads(f.read())
			self.name = data['name']
			self.x = data['x']
			self.y = data['y']
			self.size_x = data['size_x']
			self.size_y = data['size_y']
			self.size_z = data['size_z']
			self.ground_level = data['ground_level']
			square_list = data['square']
			self.s = []
			for x in range(self.size_x):
				column = []
				for y in range(self.size_y):
					row = []
					for z in range(self.size_z):
						sq = Square(x, y, z, 1, "Pustka", "Nic tu nie ma", n=1,ne=1,e=1,se=1,s=1,sw=1,w=1,nw=1,u=1,d=1)
						for s in range(len(square_list)):
							if square_list[s]["coord"]["x"] == x and square_list[s]["coord"]["y"] == y and square_list[s]["coord"]["z"] == z:
								sq = Square(x, y, z, square_list[s]["surface"], square_list[s]["name"], square_list[s]["description"], 
											n=bool(square_list[s]["exit"][0]), ne=bool(square_list[s]["exit"][1]), 
											e=bool(square_list[s]["exit"][2]), se=bool(square_list[s]["exit"][3]), 
											s=bool(square_list[s]["exit"][4]), sw=bool(square_list[s]["exit"][5]), 
											w=bool(square_list[s]["exit"][6]), nw=bool(square_list[s]["exit"][7]), 
											u=bool(square_list[s]["exit"][8]), d=bool(square_list[s]["exit"][9]))
						row.append(sq)
					column.append(row)
				self.s.append(column)
	def test(self):
		licznik = 0
		for z in range(self.size_z):
			for y in range(self.size_y):
				for x in range(self.size_x):
					print(licznik)
					licznik+=1
					print("X: {}, Y: {}, Z: {}".format(x, y, z))
					print(self.s[x][y][z].show_content())
	def show_location(self, x, y, z):
		self.s[x][y][z].show_content(self)
