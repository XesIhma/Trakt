def spawn(self):
		keywords = {
			"hp" : 20, 
			"hp_max" : 20,
			"st" : 50,
			"st_av" : 50,
			"st_max" : 100,
			"mn" : 5,
			"mn_max" : 10,
			"nou" : 30,
			"nou_max" : 50,
			"str" : 3,
			"agl" : 60,
			"spd" : 5,
			"def" : 10,
			"per" : 20,
			"vis" : 20,
			"sword" : 5,
			"axe" : 5,
			"spear" : 5,
			"cudgel" : 5,
			"bow" : 2}
		kurwik = Humanoid(-1, 3, 0, 0, "Mały kurwik", ["kurwik", "maly kurwik"], "kurwik", "Mały włochaty, lekko przygarbiony kurwik", 5, [], **keywords)
		kwargs = {}
		kwargs['w_type'] = "spear"
		kwargs["dm"] = 5
		kwargs["str_r"] = 5
		kwargs["agl_r"] = 5
		kwargs["skill_r"] = 5
		kwargs["though"] = 20
		kwargs["cut"] = 0
		kwargs["stab"] = 80
		kwargs["crush"] = 10
		kwargs['block'] = 0
		kij = CloseRange("Kij", ["kij"], "Zwykły leśny patyk, zaostrzony na końcu", -1, 2, 0, **kwargs)
		kurwik.right_hand = kij
		kurwik.currentLocation = self.world.location[-1]
		self.world.location[-1].mobs.append(kurwik)

    def populate(self):
		keywords = {
			"hp" : 60, 
			"hp_max" : 70,
			"st" : 50,
			"st_av" : 90,
			"st_max" : 100,
			"mn" : 5,
			"mn_max" : 10,
			"nou" : 30,
			"nou_max" : 50,
			"str" : 10,
			"agl" : 50,
			"spd" : 5,
			"def" : 10,
			"per" : 20,
			"vis" : 20,
			"sword" : 5,
			"axe" : 5,
			"spear" : 5,
			"cudgel" : 5,
			"bow" : 2}
		self.hero = Hero(0, 9,7,2, "Erlod", ["erlod"], "To tylko ty", "Human", 70, [], **keywords)
		keywords["hp"] = 20
		keywords["hp_max"] = 20
		keywords["str"] = 5
		keywords["agl"] = 10
		kukla1 = Humanoid(-1, 15, 1, 2, "Zwykła kukła", ["kukla", "kukła"], "kukła", "Zwykła obrotowa kukła", 0, [], **keywords)
		keywords["hp"] = 10
		kukla2 = Humanoid(-1, 15, 1, 2, "Zniszczona kukła", ["kukla", "zniszczona kukla"], "Ta kukła ma za sobą wiele pojedynków", "kukła", 0, [], **keywords)
		keywords["str"] = 20
		keywords["agl"] = 5
		keywords["hp"] = 100
		keywords["hp_max"] = 100
		ogr = Humanoid(-1, 16, 1, 2, "Ogr Igor", ["ogr", "igor"], "Gigantyczny ogr, sapie strasznie", "ogr", 0, [], **keywords)
		kwargs = {}
		kwargs['w_type'] = "xudgel"
		kwargs["dm"] = 50
		kwargs["str_r"] = 50
		kwargs["agl_r"] = 10
		kwargs["skill_r"] = 10
		kwargs["though"] = 50
		kwargs["cut"] = 0
		kwargs["stab"] = 0
		kwargs["crush"] = 100
		kwargs['block'] = 50
		maczuga = CloseRange("Maczuga", ["maczuga"], "Wielki kawał drewna ponabijany kamieniami", -1, 20, 0, **kwargs)
		ogr.right_hand = maczuga
		self.hero.currentLocation = self.world.location[0]
		kukla1.currentLocation = self.world.location[0]
		kukla2.currentLocation = self.world.location[0]
		ogr.currentLocation = self.world.location[0]
		self.hero.currentLocation.mobs.append(kukla1)
		self.hero.currentLocation.mobs.append(kukla2)
		self.hero.currentLocation.mobs.append(ogr)		

  	eliskir = Elixir("Eliksir walki", ["eliksir", "eliksir walki"], "description", 32, 1, 20, 24, str=20, agl=1)
		pot1 = Elixir("Potion", ["potion", "pot1"], "description", -1, 1, 1, 0, hp_sup=30)
		pot2 = Elixir("Potion", ["potion", "pot2"], "description", -1, 1, 1, 0,hp_sup=40)
		pot3 = Elixir("Potion", ["potion", "pot3"], "description", -1, 1, 1, 0,hp_sup=50)
		pot4 = Elixir("Redbul", ["redbul"], "description", -1, 1, 1, 0,st_sup=50)
		pot5 = Elixir("Redbul", ["redbul"], "description", -1, 1, 1, 0,st_sup=50)
		ban1 = Heals("Bandaż", ["bandaz", "bandaz1"], "description", -1, 1, 1, hp_sup=50)
		ban2 = Heals("Bandaż", ["bandaz", "bandaz2"], "description", -1, 1, 1, hp_sup=50)
		ban3 = Heals("Bandaż", ["bandaz", "bandaz3"], "description", -1, 1, 1, hp_sup=50)
		sword= CloseRange("Miecz światłości", ["miecz", "miecz swiatlosci"], "Piękny miecz", -1, 6, 500, w_type="sword", dm=30, str_r=5, agl_r=5, skill_r=0, though=5, cut=5, stab=5, crush=5, block=5)
		self.hero.equip.append(eliskir)
		self.hero.equip.append(pot1)
		self.hero.equip.append(pot2)
		self.hero.equip.append(pot3)
		self.hero.equip.append(pot4)
		self.hero.equip.append(pot5)
		self.hero.equip.append(ban1)
		self.hero.equip.append(ban2)
		self.hero.equip.append(ban3)
		self.hero.equip.append(sword)