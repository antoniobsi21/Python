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

	# def getSummonerStats(self):
	# 	dados = requests.get('https://{}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{}?api_key={}'. \
	# 	format(self.region + str(1) if self.region not in ['kr', 'ru'] else self.region, self.nickname, self.myKey))
	# 	self.dados = dados.json()
	# 	return self.dados

	def getSoloQueueElo(self):
		elo = requests.get('https://br1.api.riotgames.com/lol/league/v4/positions/by-summoner/{}?api_key=RGAPI-a351e1cf-d618-489a-9545-df3d85cf521d'. \
		format(self.dados['id']))
		self.elo = elo.json()[0]
		return "{}: {} {}.".format(self.nickname, self.elo['tier'], self.elo['rank'])