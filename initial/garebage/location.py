from square import Square
import json

def coord_conv(letter):
	if letter == "Y":
		return 0
	elif letter == "Z":
		return 1
	elif letter == "A":
		return 2
	elif letter == "B":
		return 3
	elif letter == "C":
		return 4
	elif letter == "D":
		return 5
	else:
		return 10

class Location:
	def __init__(self, file_path):
		self.name = "Nigdzie"
		self.x = 0
		self.y = 0
		self.size_x = 1
		self.size_y = 1
		self.size_z = 1
		self.s = None

		loc_file = open(file_path, encoding='utf-8')
		loc_square = []
		for line in loc_file.readlines():
			loc_square.append(line.rstrip())
		loc_file.close()
		nr_linii = 1
		temp_sq_name = []
		temp_sq_desc = []
		temp_sq_x = []
		temp_sq_y = []
		temp_sq_z = []
		temp_sq_surf = []
		temp_sq_exits = []
		for r in loc_square:
			if nr_linii == 1:
				self.name = r
				nr_linii += 1
			elif nr_linii == 2:
				self.x = int(r)
				nr_linii += 1
			elif nr_linii == 3:
				self.y = int(r)
				nr_linii += 1
			elif nr_linii == 4:
				self.size_x = int(r)
				nr_linii += 1
			elif nr_linii == 5:
				self.size_y = int(r)
				nr_linii += 1
			elif nr_linii == 6:
				self.size_z = int(r)
				nr_linii += 1
			elif nr_linii == 7:
				temp_sq_z.append(coord_conv(r))
				nr_linii += 1
			elif nr_linii == 8:
				temp_sq_x.append(int(r))
				nr_linii += 1
			elif nr_linii == 9:
				temp_sq_y.append(int(r))
				nr_linii += 1
			elif nr_linii == 10:
				temp_sq_surf.append(int(r))
				nr_linii += 1
			elif nr_linii == 11:
				temp_sq_name.append(r)
				nr_linii += 1
			elif nr_linii == 12:
				temp_sq_desc.append(r)
				nr_linii += 1
			elif nr_linii == 13:
				temp_sq_exits.append(r)
				nr_linii = 7
		
		self.s = []
		for x in range(self.size_x):
			column = []
			for y in range(self.size_y):
				row = []
				for z in range(self.size_z):
					sq = Square(x, y, z, 1, "Pustka", "Nic tu nie ma", n=1,ne=1,e=1,se=1,s=1,sw=1,w=1,nw=1,u=1,d=1)
					for s in range(len(temp_sq_name)):
						#print("Z: {}, z: {}, Y: {}, y: {}, X: {}, x: {}".format(z+1, temp_sq_z[s], y+1, temp_sq_y[s], x+1, temp_sq_x[s]))
						if temp_sq_x[s] == x and temp_sq_y[s] == y and temp_sq_z[s] == z:
							sq = Square(x, y, z, int(temp_sq_surf[s]), temp_sq_name[s], temp_sq_desc[s], 
										n=bool(int(temp_sq_exits[s][0])), ne=bool(int(temp_sq_exits[s][1])), 
										e=bool(int(temp_sq_exits[s][2])), se=bool(int(temp_sq_exits[s][3])), 
										s=bool(int(temp_sq_exits[s][4])), sw=bool(int(temp_sq_exits[s][5])), 
										w=bool(int(temp_sq_exits[s][6])), nw=bool(int(temp_sq_exits[s][7])), 
										u=bool(int(temp_sq_exits[s][8])), d=bool(int(temp_sq_exits[s][9])))
						#else:
							#sq = Square(x, y, z, 1, "", "beng", n=1,ne=1,e=1,se=1,s=1,sw=1,w=1,nw=1,u=1,d=1)
							#row.append(sq)
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
