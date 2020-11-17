with open("items.json", "r", encoding='utf-8') as f:
			data = json.loads(f.read())
			for x in data:
				class_name = data['class']
				name = data['name']
				description = data['description']
				weight = data['weight']
				price = data['price']
				x = data['x']
				y = data['x']
				z = data['x']
				loc = castle
				item_id = data['id']
				if class_name == "Food":
					temp_item = Food(name, description, x, y, z, loc, weight, price, data['nourish'], data['stamina_suppl'])
					self.items.append(temp_item)
				elif class_name == "Drink":
					temp_item = Drink(name, description, x, y, z, loc, weight, price, data['nourish'], data['stamina_suppl'], data['alcohol'])
					self.items.append(temp_item)
				elif class_name == "Heals":
					temp_item = Heals(name, description, x, y, z, loc, weight, price, data['nourish'], data['hp_suppl'])
					self.items.append(temp_item)
				elif class_name == "Elixir":
					temp_item = Elixir(name, description, x, y, z, loc, weight, price, hp_sup=data["hp_sup"], st_av_sup=data["st_av_sup"], st_sup=data["st_sup"], mn_sup=data["mn_sup"], str=data["str"], agl=data["agl"], spd=data["spd"], dfc=data["dfc"], per=data["per"], stl=data["stl"], hp_b=data["hp_b"], mn_b=data["mn_b"])
					self.items.append(temp_item)
				elif class_name == "CloseRange":
					temp_item = CloseRange(name, description, x, y, z, loc, weight, price, type=data['type'], dm=data['damage'], str_r=data['strength_req'], agl_r=data['agility_req'], skill_r=0, though=data['thoughness'], cut=data['cut'], stab=data['stab'], crush=data['crush'], block=data['block'])
					self.items.append(temp_item)
				elif class_name == "Ranged":
					temp_item = Ranged(name, description, x, y, z, loc, weight, price, type=data['type'], dm=data['damage'], str_r=data['strength_req'], agl_r=data['agility_req'], skill_r=0, ammo_type=data['ammo_type'], range=data['range'])
					self.items.append(temp_item)   
				elif class_name == "Armor":
					temp_item = Armor(name, description, x, y, z, loc, weight, price, body=data['body_part'], material=data['material'], defe=data['defence'], str_r=data['strength_req'], agl_min=data['agility_minus'], spd_min=data['speed_minus'])
					self.items.append(temp_item)
				elif class_name == "Clothes":
					temp_item = Clothes(name, description, x, y, z, loc, weight, price, body=data['body_part'], cold=data['cold_protection'], water=data['water_protection'])
					self.items.append(temp_item)
				elif class_name == "Tool":
					temp_item = Tool(name, description, x, y, z, loc, weight, price)
					self.items.append(temp_item)
				elif class_name == "Jewellery":
					temp_item = Jewellery(name, description, x, y, z, loc, weight, price, body=data['body_part'])
					self.items.append(temp_item)
				elif class_name == "Machine":
					temp_item = Machine(name, description, x, y, z, loc, weight, price)
					self.items.append(temp_item)
				elif class_name == "Vehicle":
					temp_item = Vehicle(name, description, x, y, z, loc, weight, price, str_r=data['strength_req'], spd_min=data['speed_minus'])
					self.items.append(temp_item)
				elif class_name == "Container":
					temp_item = Container(name, description, x, y, z, loc, weight, price, capacity=data['capacity'], liquids=data['for_liquids'])
					self.items.append(temp_item)
				elif class_name == "Furniture":
					temp_item = Furniture(name, description, x, y, z, loc, weight, price, open=data['openable'])
					self.items.append(temp_item)
				elif class_name == "Heap":
					temp_item = Heap(name, description, x, y, z, loc, weight, price)
					self.items.append(temp_item)