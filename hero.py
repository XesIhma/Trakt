from humanoid import Humanoid
from konsola import Konsola

class Hero(Humanoid):
	def __init__(self, i, xx, yy, zz, n, a, d, sp, lft, itId,**kwargs):
		super(Hero, self).__init__(i, xx, yy, zz, n, a, d, sp, lft, itId, **kwargs)

	def parameters(self):
		Konsola.parameters(self)
	def outfit(self):
		anything = 0
		if self.bodyPart["right_hand"]:
			print("W prawej ręce     "+self.bodyPart["right_hand"].name)
			anything+=1
		if self.bodyPart["left_hand"]:
			print("W lewej ręce      "+self.bodyPart["left_hand"].name)
			anything+=1
		if anything>0:
			print("")
			anything=1

		if self.bodyPart["head"]:
			print("Na głowie         "+self.bodyPart["head"].name)
			anything+=1
		if self.bodyPart["torso1"]:
			print("Na torsie         "+self.bodyPart["torso1"].name)
			anything+=1
		if self.bodyPart["torso2"]:
			print("Na torsie         "+self.bodyPart["torso2"].name)
			anything+=1
		if self.bodyPart["hands"]:
			print("Na dłoniach       "+self.bodyPart["hands"].name)
			anything+=1
		if self.bodyPart["legs"]:
			print("Na nogach         "+self.bodyPart["legs"].name)
			anything+=1
		if self.bodyPart["boots"]:
			print("Buty              "+self.bodyPart["boots"].name)
			anything+=1
		if anything>1:
			print("")
			anything=2

		if self.bodyPart["finger1"] and self.bodyPart["finger2"]:
			print("Pierścienie       "+self.bodyPart["finger1"].name+" i "+self.bodyPart["finger1"].name)
			anything+=1
		elif self.bodyPart["finger1"]:
			print("Pierścień         "+self.bodyPart["finger1"].name)
			anything+=1
		elif self.bodyPart["finger2"]:
			print("Pierścień         "+self.bodyPart["finger2"].name)
			anything+=1
		if self.bodyPart["neck"]:
			print("Naszyjnik         "+self.bodyPart["neck"].name)
			anything+=1
		if anything == 0:
			print("Nie masz nic na sobie")
	def heal(self, hp):
		if self.param["hp"] + hp > self.param["hp_max"]:
			self.param["hp"] = self.param["hp_max"]
		else:
			self.param["hp"] += hp
	
	def rest(self, howLong):
		for x in range(howLong):
			self.weaking(-3, -15)
			self.heal(2)
			breakStatement = Konsola.prompt(self, False)
			if breakStatement: return 0
			Konsola.sleep(1)
			print("Minęła godzina")
	def sleep(self):
		long = self.param["stamina_max"] - self.param["stamina_aviable"]
		howLong = int(long / 10)
		for x in range(howLong):
			self.weaking(-11, -20)
			self.heal(5)
			breakStatement = Konsola.prompt(self, False)
			if breakStatement: return 0
			Konsola.sleep(1)
			print("Minęła godzina")
		print("Wyspałeś się")
		return howLong 