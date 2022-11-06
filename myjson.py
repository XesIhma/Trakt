import json

class MyJson:
	def __init__(self, maps):
		pass
	@classmethod
	def readJson(cls, path):
		with open(path, "r", encoding='utf-8') as f:
			data = json.loads(f.read())
			return data
	@classmethod
	def saveJson(cls, path, data):
		with open(path, 'w', encoding='utf-8') as outfile:
			json.dump(data, outfile, indent=2, ensure_ascii=False)