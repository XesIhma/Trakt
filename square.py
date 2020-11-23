from colorama import Fore, Back, Style
import sys 
import time


class Square:
	def __init__(self, x, y, z, surf, name, desc, **kwargs):
		self.x = x
		self.y = y
		self.z = z
		self.surface = surf
		self.surf_color = self.surf_color(self.surface)
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
		
	def show_content(self, location):
		print(Fore.LIGHTYELLOW_EX + self.name + Style.RESET_ALL)
		print(Fore.LIGHTWHITE_EX, end='')
		#for char in self.description:
			#sys.stdout.write(char)
			#time.sleep(0.005)
		#data = self.description.split()
		#for w in data:
			#sys.stdout.write('%s\r' % pad)
			#sys.stdout.write("%s " % w)
			#time.sleep(0.03)
		print(self.description)
		print(Style.RESET_ALL, end='')
		#nw n ne up
		#w    e	down
		#sw s se
		try: 
			print(location.s[self.x-1][self.y-1][self.z].surf_color, end="") if self.northwest else print(Fore.BLACK + Style.BRIGHT, end="")
			print("nw" + Style.RESET_ALL, end="")
			print(location.s[self.x][self.y-1][self.z].surf_color, end="") if self.north else print(Fore.BLACK + Style.BRIGHT, end="")
			print(" n " + Style.RESET_ALL, end="")
			print(location.s[self.x+1][self.y-1][self.z].surf_color, end="") if self.northeast else print(Fore.BLACK + Style.BRIGHT, end="")
			print("ne" + Style.RESET_ALL, end="")
			print(" ", end="")
			print(location.s[self.x][self.y][self.z+1].surf_color, end="") if self.up else print(Fore.BLACK + Style.BRIGHT, end="")
			print("up" + Style.RESET_ALL)
			print(location.s[self.x-1][self.y][self.z].surf_color, end="") if self.west else print(Fore.BLACK + Style.BRIGHT, end="")
			print("w " + Style.RESET_ALL, end="")
			print("   ", end="")
			print(location.s[self.x+1][self.y][self.z].surf_color, end="") if self.east else print(Fore.BLACK + Style.BRIGHT, end="")
			print(" e" + Style.RESET_ALL, end="")
			print(" ", end="")
			print(location.s[self.x][self.y][self.z-1].surf_color, end="") if self.down else print(Fore.BLACK + Style.BRIGHT, end="")
			print("down" + Style.RESET_ALL)
			print(location.s[self.x-1][self.y+1][self.z].surf_color, end="") if self.southwest else print(Fore.BLACK + Style.BRIGHT, end="")
			print("sw" + Style.RESET_ALL, end="")
			print(location.s[self.x][self.y+1][self.z].surf_color, end="") if self.south else print(Fore.BLACK + Style.BRIGHT, end="")
			print(" s " + Style.RESET_ALL, end="")
			print(location.s[self.x+1][self.y+1][self.z].surf_color, end="") if self.southeast else print(Fore.BLACK + Style.BRIGHT, end="")
			print("sw" + Style.RESET_ALL)
		except IndexError:
			print("")
	def check_exit(self, direction):
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
		if direction in exits: 
			if exits[direction] == False:
				print("Nie da się tam przejść")
			return exits[direction]
		else: 
			print("Nie da się tam przejść")
			return False
	def surf_color(self, surf):
		# 1 droga
		# 2 budynek
		# 3 łąka
		# 4 las
		# 5 góry
		# 6 bagna
		if surf == 1:
			return  Back.YELLOW + Fore.BLACK
		elif surf == 2:
			return Back.RED + Style.BRIGHT
		elif surf == 3:
			return Back.GREEN + Fore.BLACK
		elif surf == 4:
			return Back.GREEN + Style.BRIGHT
		elif surf == 5:
			return Back.BLACK + Style.BRIGHT
		elif surf == 6:
			return Back.CYAN + Style.BRIGHT