import socket
import json
import threading
import keyboard
import time
import numpy
import random
from noise import pnoise2

HOST = '0.0.0.0'
PORT = 65432

MAX_PLAYERS = 4

players = []
conns = []
updates = {}
iMapSize = 64

locker = threading.Lock()

aMap = [[0 for x in range(iMapSize)] for y in range(iMapSize)]

def perlin_array(shape, scale=100, octaves = 6,  persistence = 0.5,  lacunarity = 2.0,  seed = None):
	if not seed:
		seed = numpy.random.randint(0, 100)
		arr = numpy.zeros(shape)
	for i in range(shape[0]):
		for j in range(shape[1]):
			arr[i][j] = pnoise2(i / scale, j / scale, octaves=octaves, persistence=persistence, lacunarity=lacunarity, repeatx=1024, repeaty=1024, base=seed)
	max_arr = numpy.max(arr)
	min_arr = numpy.min(arr)
	norm_me = lambda x: (x-min_arr)/(max_arr - min_arr)
	norm_me = numpy.vectorize(norm_me)
	arr = norm_me(arr)
	return arr
	
################## MAP GENERATOR ###################
for iX in range(1, iMapSize - 1):#dirt loop
	for iY in range(1, iMapSize - 1):
		aMap[iX][iY] = 1
#generating terrain
'''
perlin = perlin_array((iMapSize, iMapSize))
for y in range(1, iMapSize - 1):
	for x in range(1, iMapSize - 1):
		if perlin[x][y] >= 0 and perlin[x][y] <= 0.4:
			aMap[x][y] = 8 #Water
		elif perlin[x][y] >0.4 and perlin[x][y] <= 0.55:
			aMap[x][y] = 9 #Sand
		elif perlin[x][y] > 0.55 and perlin[x][y] <= 0.70:
			aMap[x][y] = 1
		elif perlin[x][y] > 0.70 and perlin[x][y] <= 1:
			aMap[x][y] = 2
'''
for iSteps in range(int(iMapSize ** 2 / 24)):#tree loop
	iRandX = random.randint(2, iMapSize - 2)
	iRandY = random.randint(2, iMapSize - 2)
	for iX in range(iRandX - 1, iRandX + 2):
		for iY in range(iRandY - 1, iRandY + 2):
			if aMap[iX][iY] != 0:
				aMap[iX][iY] = 5
	aMap[iRandX][iRandY] = 4

def data2bytes(data):
    return bytes(json.dumps({'data' : data}), encoding='utf8')
    
def bytes2data(bytes):
    return json.loads(bytes.decode('utf8'))

def TimerInit():
	return int(round(time.time() * 1000))
	
def TimerDiff(hTimer):
	return int(round(time.time() * 1000)) - hTimer	

def playerDisconnect(conn, nick):
	print(nick, 'disconnected')
	print(conns)
	conns.remove(conn)
	for player in players:
		if player['nick'] == nick:
			players.remove(player)
	for player in players:
		with locker:
			updates[player['nick']].append('removePlayer,' + nick)

def playerThread(conn):
	nick = None
	if len(players) == MAX_PLAYERS:
		conn.send(data2bytes(-1)) #No free slot available
	else:
		conn.send(data2bytes('getName'))
		while True:
			data = conn.recv(1024)
			if data:
				data = bytes2data(data)
				print('Logging in as', data['data'])
				for player in players:
					if player['nick'] == data['data']:
						print('This player is online')
						conn.send(data2bytes(-2)) #Player is online
						return
				conn.send(data2bytes('OK'))
				break
		nick = data['data']
		data = {'nick' : data['data'], 'X' : random.randint(1, iMapSize), 'Y' : random.randint(1, iMapSize), 'Direction' : 2, 'eq' : [[0 for x in range(2)] for y in range(9)]}
		updates[nick] = []
		if len(players):
			for player in players:
				updates[player['nick']].append('addPlayer,' + data['nick'] + ',' + str(data['X']) + ',' + str(data['Y']) + ',' + str(data['Direction']))
		conns.append(conn)
		players.append(data)
	timer = TimerInit()
	while True:
		'''
		if TimerDiff(timer) >= 5000:
			try:
				conn.send(data2bytes('PING'))
				timer = TimerInit()
			except:
				playerDisconnect(conn, nick)
				return
		'''
		try:
			data = conn.recv(1024)
		except:
			playerDisconnect(conn, nick)
			return
		if data:
			data = bytes2data(data)
			data = data['data'].split(',')
			#try:
			if data[0] == 'getUpdates':
				print(updates)
				with locker:
					try:
						if nick in updates:
							conn.send(data2bytes(updates[nick]))
						else:
							conn.send(data2bytes([]))
					except:
						playerDisconnect(conn, nick)
				updates[nick] = []
			#elif data[0] == 'disconnect':
			#	playerDisconnect(conn, nick)
			elif data[0] == 'getInit':
				print(nick, 'requested initial data')
				data = {'map' : aMap, 'players' : players}
				conn.send(data2bytes(data))
			elif data[0] == 'delBlock':
				aMap[int(data[1])][int(data[2])] == 1
				for player in players:
					with locker:
						updates[player['nick']].append('delBlock,' + data[1] + ',' + data[2])
			elif data[0] == 'movePlayer':
				for player in range(len(players)):
					if players[player]['nick'] == nick:
						players[player]['X'] == data[1]
						players[player]['Y'] == data[2]
						players[player]['Direction'] == data[3]
				for player in players:
					with locker:
						updates[player['nick']].append('movePlayer,' + nick + ',' + str(data[1]) + ',' + str(data[2]) + ',' + str(data[3]))
			#except:
			#	playerDisconnect(conn, nick)
			#	return
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
	s.bind((HOST, PORT))
	s.listen()
	print('Server started on', HOST, 'port', PORT)
	while True: #keyboard.read_key() != 'q':
		conn, addr = s.accept()
		if conn:
			print('Client connected:', addr)
			threading.Thread(target=playerThread, args=(conn, )).start()