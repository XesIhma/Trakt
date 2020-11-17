from human import Human
import math
from colorama import init, Fore, Back, Style

class Hero(Human):
	def __init__(self):
		super().__init__()
		self.name="Erlod"
		self.lift = 70
	def travel_show(self):
		#self.current_location.show_location(self.x, self.y, self.z)
		pass
	def parameters(self):
		print("HP:         "+Style.BRIGHT+str(self.param["hp"])+"/"+str(self.param["hp_max"])+Style.RESET_ALL)
		print("Stamina:    "+Style.BRIGHT+str(math.ceil(self.param["stamina"]))+"/"+str(math.ceil(self.param["stamina_aviable"]))+Style.RESET_ALL)
		print("Mana:       "+Style.BRIGHT+str(self.param["mana"])+"/"+str(self.param["mana_max"])+Style.RESET_ALL)
		print("Najedzenie: "+Style.BRIGHT+str(self.param["nourish"])+"/"+str(self.param["nourish_max"])+Style.RESET_ALL)
		print("")
		print("Siła: "+Style.BRIGHT+str(self.stat["strength"])+Style.RESET_ALL)
		print("Zręczność: "+Style.BRIGHT+str(self.stat["agility"])+Style.RESET_ALL)
		print("Szybkość: "+Style.BRIGHT+str(self.stat["speed"])+Style.RESET_ALL)
		print("Spostrzegawczość: "+Style.BRIGHT+str(self.stat["perceptivity"])+Style.RESET_ALL)
		print("Widoczność: "+Style.BRIGHT+str(self.stat["visibility"])+Style.RESET_ALL)

	
		