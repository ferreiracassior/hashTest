import threading
from bit import Key
import random
import os
import time
from threading import Thread
import __main__
from datetime import datetime 
import pathlib

def formatNumber(n):
    return f"{n:,}"

#------> parametros
start_rangeHex = '0000000000000000000000000000000000000000000000020000000000000000'
end_rangeHex = '000000000000000000000000000000000000000000000003ffffffffffffffff'
solution = '13zb1hQbWVsc2S7ZTZnP2G4undNNpdh5so'

start_rangeDec = int(start_rangeHex, 16)
end_rangeDec = int(end_rangeHex, 16)
total_range_distance = end_rangeDec - start_rangeDec

pathAtual = str(pathlib.Path(__file__).parent.resolve())

continuar = int(input('continuar anterior: 0/1: '))
divisoes = 0
count = 0
countReal = 0
ultimoCountReal = 0
saveFile = ""

if continuar == 0:
	divisoes = int(input('sao ' + formatNumber(total_range_distance) + ' possibilidades, digite quantas divisoes de busca: '))
	file = open(pathAtual + '\\' + 'hashMiner' + saveFile + 'mb.cfg',"w+")
	file.write(str(divisoes) + """
""" + str(count))
	file.close()
else:
	saveFile = input("digite a qtd memoria a usar em mb 10/73/405: ")
	file = open(pathAtual + '\\' + 'hashMiner' + saveFile + 'mb.cfg')
	content = file.readlines()
	file.close()
	divisoes = int(content[0])
	count = int(content[1])
	countReal = divisoes * count
	ultimoCountReal = count
 
start_time = datetime.now() 

porcaoDivisao = total_range_distance / divisoes

sArrayDivisoes = []
fArrayDivisoes = []

print('gerando array divisoes...')
for i in range(divisoes):
	if i == 0:
		sArrayDivisoes.append(start_rangeDec)
		fArrayDivisoes.append(round(porcaoDivisao) + start_rangeDec)
	else:
		sArrayDivisoes.append((round(porcaoDivisao) * i-1) + start_rangeDec)
		fArrayDivisoes.append((round(porcaoDivisao) * i) + start_rangeDec)


print('processando...')

def generate_random_number(start, end):
    return random.randint(start, end)

def printStatus(possibilidades, tentativas, progresso, hashesPorSegundo, divisoes):
	os.system('cls')
	print('processando com ' + formatNumber(divisoes) + ' divisoes...')
	print('possibilidades: ' + formatNumber(possibilidades))
	print('possibilidades restantes: ' + formatNumber(possibilidades-tentativas))
	print('tentativas feitas: ' + formatNumber(tentativas))
	print('progresso:' + str(progresso) + '%')
	print('hashes por segundo:' + formatNumber(hashesPorSegundo))
	return 0

class ImpressaoACadaSegundo(Thread):
	cont = True
	def run(self):
		self.run = True
		while threading.main_thread().is_alive() and self.cont == True:
			printStatus(total_range_distance, countReal, round(((countReal/total_range_distance)*100),16), (countReal - ultimoCountReal)*2, divisoes)
			__main__.ultimoCountReal = countReal
			time.sleep(.5)

	def stop(self):
		self.cont = False

impressora = ImpressaoACadaSegundo()
impressora.start()

while 1:
	for ad in sArrayDivisoes:
		countReal = countReal+1
		dec = ad + count
		key = Key.from_int(dec)

		if key.address == solution:
			impressora.stop()
			printStatus(total_range_distance, countReal, round(((countReal/total_range_distance)*100),16), countReal - ultimoCountReal, divisoes)
			print('pk decimal: ' + str(dec))
			print('address:' + str(key.address))
			print('wif:' + key.to_wif())
			count = 0
			countReal = 0
			ultimoCountReal = 0
			numerosTentados = []
			end = time.time()
			time_elapsed = datetime.now() - start_time 
			print('Tempo total: {}'.format(time_elapsed))
			input(' ')
			input(' ')
			file = open(pathAtual + '\\' + 'solution.txt',"w+")
			file.write('pk: decimal: ' + str(dec) + '//address: ' + str(key.address) + '//wif:' + key.to_wif())
			file.close()

	count = count +1
	file = open(pathAtual + '\\' + 'hashMiner' + saveFile + 'mb.cfg',"w+")
	file.write(str(divisoes) + """
""" + str(count))
	file.close()

#python e:\desktop\t3.py
	
	