from os import system

class Invocador:
	def __init__(self, nickname, regiao):
		self.nickname = nickname
		self.region = regiao.lower()
		self.myKey = 'RGAPI-a351e1cf-d618-489a-9545-df3d85cf521d'

	def getSummonerStats(self):
		syntax = "curl --request GET 'https://{}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{}?api_key={}' --include". \
		format(self.region + str(1) if self.region not in ['kr', 'ru'] else self.region, self.nickname, self.myKey)
		resultado = system(syntax)
		return resultado

	def getRegion(self):
		return self.region

	def getNickName(self):
		return self.nickname

	def setNickName(self, newNick):
		self.nickname = newNick

	def setRegion(self, newRegion):
		self.region = newRegion