from os import system
from invocador import Invocador

# sem 1 :"KR", "RU", ex kr.api.riotgames.com
regioes = ["BR", "EUNE", "EUW", "JP", "KR", "LAN", "LAS", "NA", "OCE", "TR", "RU", "PBE"]

def getRegiao():
	regiao = input(">> ").lower()
	if regiao.upper() not in regioes:
		print("Região inválida, por favor insira novamente.")
		return getRegiao()
	else:
		return regiao

def getNickName():
	nickname = input(">> ")
	for x in nickname:
		if not x.isalnum() and not " ":
			print("Nickname inválido, por favor insira novamente.")
			return getNickName()
	return nickname.replace(" ", "%20")

def main():
	print("Região:\n")
	for x in regioes:
		print(x)
	regiao = getRegiao()
	print("Nome de invocador:")
	nickname = getNickName()

	invocador = Invocador(nickname, regiao)
	# print(invocador.dados)
	print("ID: \'{}\'.".format(invocador.dados['id']))
	# invocador.getSoloQueuePosition()
	invocador.printAllQueuePositions()

main()