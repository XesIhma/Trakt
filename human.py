from being import Being

class Character(Being):
    def __init__(self):
        super().__init__()
        self.right_hand = None
        self.left_hand = None
        self.head = None
        self.torso1 = None
        self.torso2 = None
        self.hands = None
        self.legs = None
        self.boots = None
        self.finger1 = None
        self.finger2 = None
        self.neck = None


class Human(Character):
    def __init__(self):
        super().__init__()
        self.species = "Człowiek"
        self.equipment = []
    #def pick_up(self, item):
        #print(item.occupier)
        #print(self.equipment)
        #item.occupier = self
        #self.equipment.append(item)
        #print("Podniosłeś: {}".format(item.name))
    #def drop(self, item):
        #item.occupier = None
        #self.equipment.remove(item)
        #item.x = self.x
        #item.y = self.y
        #item.z = self.z