import requests
from os import system

class Invocador:
	def __init__(self, nickname, regiao):
		self.nickname = nickname
		self.region = regiao.lower()
		self.myKey = 'RGAPI-a351e1cf-d618-489a-9545-df3d85cf521d'
		dados = requests.get('https://{}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{}?api_key={}'. \
		format(self.region + str(1) if self.region not in ['kr', 'ru'] else self.region, self.nickname, self.myKey))
		self.dados = dados.json()

	def getSoloQueuePosition(self):
		elo = requests.get('https://br1.api.riotgames.com/lol/league/v4/positions/by-summoner/{}?api_key=RGAPI-a351e1cf-d618-489a-9545-df3d85cf521d'. \
		format(self.dados['id']))
		self.elo = elo.json()
		for x in self.elo:
			if x['queueType'].upper() == "RANKED_SOLO_5X5":
				print("\n{}: {} {} ({} PdL).\n".format(self.dados['name'], x['tier'], x['rank'], x['leaguePoints']))
				break
		return -1

	def printAllQueuePositions(self):
		elo = requests.get('https://br1.api.riotgames.com/lol/league/v4/positions/by-summoner/{}?api_key=RGAPI-a351e1cf-d618-489a-9545-df3d85cf521d'. \
		format(self.dados['id']))
		self.elo = elo.json()
		print("\n{}\n".format(self.dados['name']))
		for x in self.elo:
			if x['queueType'].upper() == "RANKED_SOLO_5X5":
				print("Solo:")
			if x['queueType'].upper() == "RANKED_FLEX_SR":
				print("Flex:")
			if x['queueType'].upper() == "RANKED_FLEX_3X3":
				print("3x3:")
			print("{}: {} {} ({} PdL).\n".format(x['leagueName'], x['tier'], x['rank'], x['leaguePoints']))
		return -1