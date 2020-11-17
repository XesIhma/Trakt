class Collection:
    id = 0
    @classmethod
    def increment_ID(cls):
        cls.id += 1 
        return cls.id
    def __init__(t, o):
        self.id=Item.increment_ID()
        self.type = t
        self.capacity = 10
        self.owner = o
        self.content = []

    def add_item(self, it):
        self.content.append(it)

