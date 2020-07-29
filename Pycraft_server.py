import socket
import json
import threading
import keyboard
import time
import random
from noise import pnoise2
from blocks import *
from net import *

HOST = '0.0.0.0'
PORT = 65432

MAX_PLAYERS = 4

players = []
conns = []
updates = {}
iMapSize = 128

locker = threading.Lock()

aMap = [[0 for x in range(iMapSize)] for y in range(iMapSize)]
aMapBack = [[0 for x in range(iMapSize)] for y in range(iMapSize)]

def perlin_array(shape, scale=100, octaves = 6,  persistence = 0.5,  lacunarity = 2.0,  seed = None):
	if not seed:
		seed = random.randint(0, 100)
		arr = [[0 for a in range(shape[0])] for b in range(shape[1])]
	for i in range(shape[0]):
		for j in range(shape[1]):
			arr[i][j] = pnoise2(i / scale, j / scale, octaves=octaves, persistence=persistence, lacunarity=lacunarity, repeatx=1024, repeaty=1024, base=seed)
	max_arr = max(map(max, arr))
	min_arr = min(map(min, arr))
	for i in range(shape[0]):
		for j in range(shape[1]):
			arr[i][j] = (arr[i][j] - min_arr) / (max_arr - min_arr)
	return arr

################## MAP GENERATOR ###################
for iX in range(1, iMapSize - 1):#dirt loop
	for iY in range(1, iMapSize - 1):
		aMap[iX][iY] = 1
#generating terrain
perlin = perlin_array((iMapSize, iMapSize))
perlin2 = perlin_array((iMapSize, iMapSize))
for y in range(1, iMapSize - 1):
	for x in range(1, iMapSize - 1):
		if perlin[x][y] >= 0 and perlin[x][y] <= 0.25:
			aMap[x][y] = 8 #Water
		elif perlin[x][y] >0.25 and perlin[x][y] <= 0.5:
			if perlin2[x][y] > 0.75:
				aMap[x][y] = 10 # Mineable sand
			else:
				aMap[x][y] = 9 #Sand
			aMapBack[x][y] = 9
		elif perlin[x][y] > 0.5 and perlin[x][y] <= 0.75:
			if perlin2[x][y] > 0.75:
				aMap[x][y] = 2
			else:
				aMap[x][y] = 1
			aMapBack[x][y] = 1
		elif perlin[x][y] > 0.75 and perlin[x][y] <= 1:
			aMap[x][y] = 12 #Stone
			aMapBack[x][y] = 11
for y in range(1, iMapSize - 1): #Cactus loop
	for x in range(1, iMapSize - 1):
		if aMap[x][y] == 9:
			if random.randint(1, 20) == 10:
				aMap[x][y] = 13
for iSteps in range(int(iMapSize ** 2 / 24)):#tree loop
	iRandX = random.randint(2, iMapSize - 2)
	iRandY = random.randint(2, iMapSize - 2)
	for iX in range(iRandX - 1, iRandX + 2):
		for iY in range(iRandY - 1, iRandY + 2):
			if aMap[iX][iY] == 9 or aMap[iX][iY] == 10:
				iSteps -= 1
				continue
	if aMap[iRandX][iRandY] == 1:
		for iX in range(iRandX - 1, iRandX + 2):
			for iY in range(iRandY - 1, iRandY + 2):
				if aMap[iX][iY] != 0:
					aMap[iX][iY] = 5
		aMap[iRandX][iRandY] = 4
	else:
		iSteps -= 1

def BlockAddEq(nick, iID, pX, pY): #Dodawanie bloku do ekwipunku
	aEq, iSelector, iCount, sID = -1, -1, 1, iID
	for player in players:
		if player['nick'] == nick:
			aEq = player['eq']
	if aEq == -1: return
	#Pre switch dla ID
	if iID == 4: #Tree > Log
		sID = 6
		iCount = random.randint(1, 3)
	elif iID == 5: #Leaves > Plants
		sID = 7
		iCount = random.randint(0, 1)
	elif iID == 7:
		sId = 7
		iCount = 1
		#TreeDelete(pX, pY)
	if iCount == 0: return
	for iC2 in [3, 0, 1, 2]:
		for iC in range(9):
			if aEq[iC][iC2][0] == 0 or aEq[iC][iC2][0] == sID:
				iSelector = [iC, iC2]
				break
		else:
			continue
		break
	if iSelector[0] != -1 and iSelector[1] != -1:
		with locker:
			updates[nick].append(['eqAdd', iSelector[0], iSelector[1], sID, iCount])
		for player in range(len(players)):
			if players[player]['nick'] == nick:
				players[player]['eq'][iSelector[0]][iSelector[1]][0] = sID
				players[player]['eq'][iSelector[0]][iSelector[1]][1] += iCount

def TimerInit():
	return int(round(time.time() * 1000))
	
def TimerDiff(hTimer):
	return int(round(time.time() * 1000)) - hTimer	

def playerDisconnect(conn, nick):
	print(nick, 'disconnected')
	conns.remove(conn)
	for player in players:
		if player['nick'] == nick:
			players.remove(player)
			print(players)
	del updates[nick]
	for player in players:
		with locker:
			updates[player['nick']].append(['removePlayer', nick])

def playerThread(conn):
	nick = None
	if len(players) == MAX_PLAYERS:
		conn.send(data2bytes(-1)) #No free slot available
	else:
		conn.send(data2bytes('getName'))
		while True:
			data = conn.recv(1024)
			if data:
				data = bytes2data(data)[0]
				print('Logging in as', data['data'])
				for player in players:
					if player['nick'] == data['data']:
						print('This player is online')
						conn.send(data2bytes(-2)) #Player is online
						return
				conn.send(data2bytes('OK'))
				break
		nick = data['data']
		data = {'nick' : data['data'], 'X' : random.randint(1, iMapSize), 'Y' : random.randint(1, iMapSize), 'Direction' : 2, 'eq' : [[[0 for e in range(2)] for x in range(4)] for y in range(9)]}
		updates[nick] = []
		if len(players):
			for player in players:
				updates[player['nick']].append(['addPlayer', data['nick'], data['X'], data['Y'], data['Direction']])
		conn.settimeout(5)
		conns.append(conn)
		players.append(data)
		timer = TimerInit()
	while TimerDiff(timer) < 5000: #5 seconds timeout
		try:
			data = conn.recv(1024)
		except:
			break
		if len(data):
			timer = TimerInit()
			datas = bytes2data(data)
			for data in datas:
				data = data['data']
				#try:
				if data[0] == 'getUpdates':
					with locker:
						try:
							if nick in updates:
								conn.send(data2bytes(updates[nick]))
							else:
								conn.send(data2bytes([]))
						except:
							break
					updates[nick] = []
				elif data[0] == 'getInit':
					print(nick, 'requested initial data')
					data = {'map' : aMap, 'mapBack' : aMapBack, 'players' : players}
					conn.send(data2bytes(data))
				elif data[0] == 'delBlock':
					x = data[1]
					y = data[2]
					BlockAddEq(nick, aMap[x][y], x, y)
					aMap[x][y] = aMapBack[x][y]
					for player in players:
						with locker:
							updates[player['nick']].append(['delBlock', x, y, aMapBack[x][y]])
				elif data[0] == 'placeBlock':
					x = data[1]
					y = data[2]
					for player in players:
						if player['nick'] == nick:
							iID = player['eq'][data[3]][3][0]
					if iID and not blocks.isMineable(aMap[x][y]) and blocks.isWalkable(aMap[x][y]):
						if iID == 13 and aMap[x][y] != 9: return
						if iID == 7 and aMap[x][y] != 1: return
						aMap[data[1]][data[2]] = iID
						player['eq'][data[3]][3][1] -= 1
						#if iID == 7: AddTree(pX, pY)
						if not player['eq'][data[3]][3][1]: player['eq'][data[3]][3][0] = 0
						with locker:
							updates[nick].append(['eqRemove', data[3], 3])
							for player in players:
								updates[player['nick']].append(['placeBlock', data[1], data[2], iID])
				elif data[0] == 'movePlayer':
					for player in range(len(players)):
						if players[player]['nick'] == nick:
							players[player]['X'] = data[1]
							players[player]['Y'] = data[2]
							players[player]['Direction'] = data[3]
					with locker:
						for player in players:
							updates[player['nick']].append(['movePlayer', nick, data[1], data[2], data[3]])
	playerDisconnect(conn, nick)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
	s.bind((HOST, PORT))
	s.listen()
	print('Server started on', HOST, 'port', PORT)
	while True: #keyboard.read_key() != 'q':
		conn, addr = s.accept()
		if conn:
			print('Client connected:', addr)
			threading.Thread(target=playerThread, args=(conn, )).start()