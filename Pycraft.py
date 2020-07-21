import pygame
import time
import random
import math
import numpy
from noise import pnoise2
import socket
import json
import pygame_menu
import os
import threading
pygame.init()

width, height = 480, 480
blocks = [math.floor(math.floor(width / 48) / 2), math.floor(math.floor(height / 48) / 2)]

nick = 'Player' + str(random.randint(1, 9))

aMap = []
aMapBack = []

clock = pygame.time.Clock()

locker = threading.Lock()

################### DEVELOPER MODE #####################
iDeveloper = 0
########################################################
#tMoveInterval # Timer ruchu
tMouseInterval = None # Timer kopania
io1 = 6
io2 = -io1 # Skok offsetu
b_Map = 0 # Mapa (ziemia/jaskinia
aTrees = [] # Tablica drzew (mechanizm rozrostu)
################### STRUCTY
oDig = {'Dig' : -1, 'X' : -1, 'Y' : -1}
ItemBar = []
itemSelector = 0 # Selektor paska
oPlayer = {}
players = []
oOffset = {'X' : 0, 'Y' : 0, 'Direction' : 0}
#########################################################
def BlockAdd(iID, bTrans, bMine, iDigTime):
	aBlockInfo.append({'ID' : iID, 'Trans' : bTrans, 'bMine' : bMine, 'iDigTime' : iDigTime})
################### BLOCKS INFO ########################
aBlockInfo = [] #ID, Trans, Mineable, DigTime
BlockAdd(0, 0, 0, 0) #Bedrock
BlockAdd(1, 1, 0 , 0) #Dirt (Background)
BlockAdd(2, 0, 1, 150) #Dirt (Minable)
BlockAdd(3, 0, 1, 0) #Water
BlockAdd(4, 0, 1, 250) #Tree
BlockAdd(5, 1, 1, 100) #Leaves
BlockAdd(6, 0, 1, 250) #Log (Tree)
BlockAdd(7, 1, 1, 0) #Plant (Tree)
BlockAdd(8, 0, 0, 0) #Water
BlockAdd(9, 1, 0, 0) #Sand
BlockAdd(10, 0, 1, 150) #Sand (Mineable)
BlockAdd(11, 1, 0, 0) #Stone
BlockAdd(12, 0, 1, 500) #Stone (Mineable)
BlockAdd(13, 0, 1, 150) #Cactus
########################################################
################### BLOCKS TEXTURES LOAD ###############
txt_id = []
txt_id.append(pygame.image.load("./Data/Blocks/bedrock.png")) #Bedrock, ID 0
txt_id.append(pygame.image.load("./Data/Blocks/dirt_b.png")) #Dirt (background), ID 1
txt_id.append(pygame.image.load("./Data/Blocks/dirt.png")) #Dirt, ID 2
txt_id.append(pygame.image.load("./Data/Blocks/water.png")) #Woda, ID 3
txt_id.append(pygame.image.load("./Data/Blocks/tree.png")) #Drzewo, ID 4
txt_id.append(pygame.image.load("./Data/Blocks/leaves.png")) #Liście, ID 5
txt_id.append(pygame.image.load("./Data/Blocks/log.png")) #LOG, ID 6
txt_id.append(pygame.image.load("./Data/Blocks/plant.png")) #Plant (Tree), ID 7
txt_id.append(pygame.image.load("./Data/Blocks/water.png")) #Water, ID 8
txt_id.append(pygame.image.load("./Data/Blocks/sand_b.png")) #Sand (background), ID 9
txt_id.append(pygame.image.load("./Data/Blocks/sand.png")) #Sand (Mineable), ID 10
txt_id.append(pygame.image.load("./Data/Blocks/stone_b.png")) #Stone (background, ID 11
txt_id.append(pygame.image.load("./Data/Blocks/stone.png")) #Stone (Mineable), ID 12
txt_id.append(pygame.image.load("./Data/Blocks/cactus.png")) #Cactus, ID 13
txt_black = pygame.image.load("./Data/Blocks/black.png")
txt_m_stage = [0 for x in range(4)]
txt_m_stage[1] = pygame.image.load("./Data/Blocks/m_stage_1.png") #Mine stage :1
txt_m_stage[2] = pygame.image.load("./Data/Blocks/m_stage_2.png") #Mine stage :2
txt_m_stage[3] = pygame.image.load("./Data/Blocks/m_stage_3.png") #Mine stage :3
txt_itembar = pygame.image.load("./Data/Blocks/itembar.png") #Itembar
txt_itemselector = pygame.image.load("./Data/Blocks/itemselector.png") #ItemSelector
########################################################
################## PLAYER TEXTURES #####################
txt_player = [0 for x in range(4)]
txt_player[0] = pygame.image.load("./Data/Player/up.png")
txt_player[1] = pygame.image.load("./Data/Player/right.png")
txt_player[2] = pygame.image.load("./Data/Player/down.png")
txt_player[3] = pygame.image.load("./Data/Player/left.png")
########################################################
################### LIGHT TEXTURES LOAD ################
txt_light = [0 for x in range(6)]
txt_light[0] = pygame.image.load("./Data/Light/0.png")# 0%
txt_light[2] = pygame.image.load("./Data/Light/20.png")# 20%
txt_light[3] = pygame.image.load("./Data/Light/30.png")# 30%
txt_light[4] = pygame.image.load("./Data/Light/40.png")# 40%
txt_light[5] = pygame.image.load("./Data/Light/50.png")# 50%
########################################################
################### FONTS LOAD #########################
#Font_red = _FontCreate(@ScriptDir & "Data/Font/", 0, -100, -100)
#Font_white = _FontCreate(@ScriptDir & "Data/Font/")
#Ekran ładowania
#AdlibRegister("loading_screen", 50)
#Oświetlenie
light_c, light_v, light_val = 0, 0, 0
#AdlibRegister("light", 10000) ;10s

def recvall(sock):
	BUFF_SIZE = 4 # 4 KiB
	data = b''
	while True:
		part = sock.recv(BUFF_SIZE)
		data += part
		if len(part) < BUFF_SIZE:
			break
	return data

def data2bytes(data):
    return bytes(json.dumps({'data' : data}), encoding='utf8')
    
def bytes2data(bytes):
	return json.loads(bytes.decode('utf8'))
	
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
	
def TimerInit():
	return int(round(time.time() * 1000))
	
def TimerDiff(hTimer):
	return int(round(time.time() * 1000)) - hTimer
	
def BlockPlace(pX, pY, iID = -1): #Stawianie bloków
	if iID != -1:
		aMap[pX][pY] = aBlockInfo[iID]['ID']
	elif ItemBar[itemSelector][1] and not aBlockInfo[aMap[pX][pY]]['bMine'] and aBlockInfo[aMap[pX][pY]]['Trans']:
		if ItemBar[itemSelector][0] == 13 and aMap[pX][pY] != 9: return
		if iID == 7 and aMap[x][y] != 1: return
		if playing == 2:
			s.send(data2bytes('placeBlock,' + str(pX) + ',' + str(pY) + ',' + str(itemSelector)))
		else:
			iID = ItemBar[itemSelector][0]
			aMap[pX][pY] = iID
			ItemBar[itemSelector][1] -= 1
			#if iID == 7: AddTree(pX, pY)
			if not ItemBar[itemSelector][1]: ItemBar[itemSelector][0] = 0
	else:
		return
			
def MakePoint(pX, pY, iSize, iID):
	for iX in range(pX - iSize, pX + iSize + 1):
		for iY in range(pY - iSize, pY + iSize + 1):
			if aMap[iX][iY] != 0:
				BlockPlace(iX, iY, iID)
				
def PlantTree(pX, pY):
	MakePoint(pX, pY, 1, 5) # Leaves
	BlockPlace(pX, pY, 4) # Tree
#####################################################
def IDToTexture(iID, iX, iY, iW = 48, iH = 48, bEQ = 0): #Zamienia id na HANDLE textury
	if iID == 7: #Plant
		if not bEQ:
			window.blit(pygame.transform.scale(txt_id[1], (iW, iH)), (iX, iY))
		window.blit(pygame.transform.scale(txt_id[7], (iW, iH)), (iX, iY))
	elif iID == 5: #Leaves
		window.blit(pygame.transform.scale(txt_id[5], (iW, iH)), (iX, iY))
	elif iID == 13: #Cactus
		if not bEQ:
			window.blit(pygame.transform.scale(txt_id[9], (iW, iH)), (iX, iY))
		window.blit(pygame.transform.scale(txt_id[13], (iW, iH)), (iX, iY))
	else:
		window.blit(pygame.transform.scale(txt_id[iID], (iW, iH)), (iX, iY))
		'''
		Case 1
			;_DirectDraw($txt_dirt_b, $iX, $iY)
		Case 2
			_DirectDraw($txt_dirt, $iX, $iY)
		Case 3
			_DirectDraw($txt_water, $iX, $iY)
		Case 4
			_DirectDraw($txt_tree, $iX, $iY)
		Case 5
			_DirectDraw($txt_leaves, $iX, $iY)
		'''
		
def DrawMap():#Funkcja rysowania mapy
	'''
	if b_Map == 0: #Ziemia
		print("")#window.blit(txt_id[1], (-48 + oOffset['X'], -48 + oOffset['Y']))
	elif b_Map == 1: # Jaskinia
		print("")
	'''
	leaves = []
	for iX in range(oPlayer['X'] - blocks[0] - 1, oPlayer['X'] + blocks[0] + 2):
		for iY in range(oPlayer['Y'] - blocks[0] - 1, oPlayer['Y'] + blocks[1] + 2):
			if iX < 0 or iX > iMapSize -1 or iY < 0 or iY > iMapSize - 1:
				IDToTexture(0, #Txt bloku z mapy
				((iX - (oPlayer['X'] - blocks[0])) * 48) + oOffset['X'], #pozycja X rysowania w oknie
				((iY - (oPlayer['Y'] - blocks[1])) * 48) + oOffset['Y']) #pozycja Y rysowania w oknie
			elif aMap[iX][iY] == 5:
				IDToTexture(1, #rysowanie ziemi
				((iX - (oPlayer['X'] - blocks[0])) * 48) + oOffset['X'], #pozycja X rysowania w oknie
				((iY - (oPlayer['Y'] - blocks[1])) * 48) + oOffset['Y']) #pozycja Y rysowania w oknie
				leaves.append((iX, iY))
			else:
				IDToTexture(aMap[iX][iY], #Txt bloku z mapy
				((iX - (oPlayer['X'] - blocks[0])) * 48) + oOffset['X'], #pozycja X rysowania w oknie
				((iY - (oPlayer['Y'] - blocks[1])) * 48) + oOffset['Y']) #pozycja Y rysowania w oknie
	if playing == 2:
		for iX in range(oPlayer['X'] - blocks[0], oPlayer['X'] + blocks[0] + 1):
			for iY in range(oPlayer['Y'] - blocks[0], oPlayer['Y'] + blocks[1] + 1):
				for player in players:
					if player['X'] == iX and player['Y'] == iY:
						window.blit(txt_player[player['Direction']], ((iX - oPlayer['X'] + blocks[0]) * 48 + oOffset['X'], (iY - oPlayer['Y'] + blocks[1]) * 48 + oOffset['Y'])) #postać
	window.blit(txt_player[oPlayer['Direction']], (blocks[0] * 48, blocks[1] * 48)) #postać
	if len(leaves):
		for leaf in leaves:
			IDToTexture(5, #Rysowanie liści
			((leaf[0] - (oPlayer['X'] - blocks[0])) * 48) + oOffset['X'], #pozycja X rysowania w oknie
			((leaf[1] - (oPlayer['Y'] - blocks[1])) * 48) + oOffset['Y']) #pozycja Y rysowania w oknie
	window.blit(pygame.transform.scale(txt_light[int(light_val / 10)], (528, 528)), (0, 0))
	if oDig['Dig'] != -1:
		window.blit(txt_m_stage[oDig['Dig']],
		((oDig['X'] - oPlayer['X'] + blocks[0]) * 48,
		(oDig['Y'] - oPlayer['Y'] + blocks[1]) * 48))
	DrawItembar()

def MapOffset(oX = 0, oY = 0):
	if aMap[oPlayer['X'] + oX][oPlayer['Y'] + oY] == 0: return 0
	if iDeveloper: return 1
	return aBlockInfo[aMap[oPlayer['X'] + oX][oPlayer['Y'] + oY]]['Trans']

def PlayerMove(key = None):
	global itemSelector
	if key and key >= 49 and key <= 57:
		itemSelector = key - 49
		return
	#Wyliczanie offsetu dla bloków (Płynne przesuwanie)
	if oOffset['X'] or oOffset['Y']:
		if not iDeveloper:
			if oOffset['X']: oOffset['X'] += oOffset['Direction']
			if oOffset['Y']: oOffset['Y'] += oOffset['Direction']
		if abs(oOffset['X']) == 48 or abs(oOffset['Y']) == 48:
			if oOffset['Y'] == 48: oPlayer['Y'] -= 1
			if oOffset['Y'] == -48: oPlayer['Y'] += 1
			if oOffset['X'] == 48: oPlayer['X'] -= 1
			if oOffset['X'] == -48: oPlayer['X'] += 1
			if playing == 2:
				with locker:
					s.send(data2bytes('movePlayer,' + str(oPlayer['X']) + ',' + str(oPlayer['Y']) + ',' + str(oPlayer['Direction'])))
			oOffset['X'] = 0
			oOffset['Y'] = 0
			oOffset['Direction'] = 0
		return
	#Ograniczenie szybkości ruchu
	#if TimerGet(tMoveInterval) < 250 and not iDeveloper and cKey > 0 and cKey < 10: Return
	#Switch cKey ;kbCode (KB hook)
	if key and not oOffset['Direction']:
		if key == pygame.K_w:
			if MapOffset(0, -1):
				oOffset['Y'] = io1 if not iDeveloper else 48
				oOffset['Direction'] = io1
			oPlayer['Direction'] = 0
		elif key == pygame.K_s:
			if MapOffset(0, 1):
				oOffset['Y'] = io2 if not iDeveloper else -48
				oOffset['Direction'] = io2
			oPlayer['Direction'] = 2
		elif key == pygame.K_a:
			if MapOffset(-1, 0):
				oOffset['X'] = io1 if not iDeveloper else 48
				oOffset['Direction'] = io1
			oPlayer['Direction'] = 3
		elif key == pygame.K_d:
			if MapOffset(1, 0):
				oOffset['X'] = io2 if not iDeveloper else -48
				oOffset['Direction'] = io2
			oPlayer['Direction'] = 1
def _Mouse():
	tMouse = {'X' : 0, 'Y' : 0, 'Button' : 0}
	tMouse['X'], tMouse['Y'] = pygame.mouse.get_pos()
	b1, b2, b3 = pygame.mouse.get_pressed()
	if b1:
		tMouse['Button'] = 1
	elif b3:
		tMouse['Button'] = 2
	return tMouse

def MouseToBlock():
	tMouse = _Mouse()
	tMouse['X'] = math.floor(tMouse['X'] / 48) + oPlayer['X'] - blocks[0]
	tMouse['Y'] = math.floor(tMouse['Y'] / 48) + oPlayer['Y'] - blocks[1]
	return tMouse
	
def BlockDig(pX, pY): #Kopanie bloków
	global tMouseInterval
	if aBlockInfo[aMap[pX][pY]]['bMine']:
		#Pre switch dla kilofów

		if iDeveloper: oDig['Dig'] = 4
		if oDig['Dig'] == -1:
			tMouseInterval = TimerInit()
			oDig['Dig'] = 1
			oDig['X'] = pX
			oDig['Y'] = pY
			return
		else:
			if pX == oDig['X'] and pY == oDig['Y'] and not iDeveloper:
				if TimerDiff(tMouseInterval) >= aBlockInfo[aMap[pX][pY]]['iDigTime']:
					tMouseInterval = TimerInit()
					oDig['Dig'] += 1
			else:
				if not iDeveloper: oDig['Dig'] = -1
		if oDig['Dig'] == 4:
			oDig['Dig'] = -1
			if playing == 2:
				with locker:
					s.send(data2bytes('delBlock,' + str(pX) + ',' + str(pY)))
			else:
				BlockAddEq(aMap[pX][pY], pX, pY) #Dodawanie do eq
				aMap[pX][pY] = aMapBack[pX][pY]
	elif oDig['Dig'] != -1:
		oDig['Dig'] = -1

def BlockAddEq(iID, pX, pY): #Dodawanie bloku do ekwipunku
	iSelector, iCount, sID = -1, 1, iID
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
	if iCount == 0: return 1
	for iC in range(0, 8):
		if ItemBar[iC][0] == sID:
			iSelector = iC
			break
	if iSelector == -1:
		for iC in range(0, 8):
			if ItemBar[iC][0] == 0:
				iSelector = iC
				break
	if iSelector != -1:
		ItemBar[iSelector][0] = sID
		ItemBar[iSelector][1] += iCount
		return 1
	return 0
	
def MouseControl():
	oMouse = MouseToBlock()
	if oMouse['Button'] == 1:
		BlockDig(oMouse['X'], oMouse['Y'])
	elif oMouse['Button'] == 2:
		BlockPlace(oMouse['X'], oMouse['Y'])
	else:
		if oDig['Dig'] != -1:
			oDig['Dig'] = -1

def DrawString(text, x, y, size = 50, color = (255, 255, 255)):
	text = str(text)
	font = pygame.font.Font("freesansbold.ttf", size)
	text = font.render(text, True, color)
	window.blit(text, (x, y))
			
def DrawItembar():
	window.blit(txt_itembar, (0, height - 48))
	window.blit(txt_itemselector, (itemSelector * 43 + itemSelector - 1, height - 48))
	for iC in range(0, 8):
		if ItemBar[iC][0] > 1:
			IDToTexture(ItemBar[iC][0], 12 + (iC * 43 + iC) - 1, height - 36, 24, 24, 1)
			#_DirectDraw($txt_id_2, 12 + ($iC * 43 + $iC) - 1, 528 - 36, 24, 24)
			DrawString(ItemBar[iC][1], 12 + (iC * 43 + iC) - 1, height - 16, 12)
#Main game loop

key = None
active_menu = 0
playing = False
paused = False

def switch_menu(menu):
	global active_menu
	active_menu = menu

def generate_map(iMapSize):
	global aMap, aMapBack
	aMap = [[0 for x in range(iMapSize)] for y in range(iMapSize)]
	aMapBack = [[0 for x in range(iMapSize)] for y in range(iMapSize)]
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
					aMapBack[x][y] = 2
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

def start_game():
	name = world_selector.get_value()
	if name[1] == -1: return
	global playing, aMap, ItemBar, oPlayer, iMapSize
	file = open('./worlds/' + name[0], 'r')
	data = json.loads(file.read())
	aMap = data['map']
	aMapBack = data['mapBack']
	iMapSize = len(aMap[0])
	ItemBar = data['eq']
	oPlayer = data['player']
	playing = True

s = None

def Client():
	while playing:
		with locker:
			s.send(data2bytes('getUpdates'))
		while True:
			data = s.recv(1024)
			if data:
				data = bytes2data(data)
				for update in data['data']:
					data = update.split(',')
					if data[0] == 'delBlock':
						aMap[int(data[1])][int(data[2])] = int(data[3])
					elif data[0] == 'movePlayer' and data[1] != nick:
						for player in range(len(players)):
							players[player]['X'] = int(data[2])
							players[player]['Y'] = int(data[3])
							players[player]['Direction'] = int(data[4])
					elif data[0] == 'addPlayer':
						players.append({'nick' : data[1], 'X' : int(data[2]), 'Y' : int(data[3]), 'Direction' : int(data[4])})
					elif data[0] == 'removePlayer':
						for player in players:
							if player['nick'] == data[1]:
								players.remove(player)
					elif data[0] == 'placeBlock':
						BlockPlace(int(data[1]), int(data[2]), int(data[3]))
					elif data[0] == 'eqRemove':
						ItemBar[int(data[1])][1] -= 1
						if not ItemBar[int(data[1])][1]: ItemBar[int(data[1])][0] = 0
					elif data[0] == 'eqAdd':
						ItemBar[int(data[1])][0] = int(data[2])
						ItemBar[int(data[1])][1] += int(data[3])
				break

def start_game_multi():
	global playing, aMap, iMapSize, nick, players, oPlayer, ItemBar, s
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	HOST, PORT = server_address.get_value().split(':', 1)
	s.connect((HOST, int(PORT)))
	while True:
		data = s.recv(1024)
		if data:
			data = bytes2data(data)
			if data['data'] == 'getName':
				s.send(data2bytes(nick))
				while True:
					data = s.recv(1024)
					if data:
						data = bytes2data(data)
						if data['data'] == 'OK':
							print('Logged in')
							s.send(data2bytes('getInit'))
							while True:
								data = recvall(s)
								if data:
									print('Map received')
									data = bytes2data(data)
									aMap = data['data']['map']
									iMapSize = len(aMap[0])
									players = data['data']['players']
									for player in players:
										if player['nick'] == nick:
											oPlayer = player
											ItemBar = player['eq']
											players.remove(player)
									playing = 2
									threading.Thread(target=Client).start()
									break
						if data['data'] == -2:
							print('Player is online')
						break
			elif data['data'] == -1:
				print('Server is full')
			break
		
def delete_world():
	name = world_selector.get_value()[0]
	os.remove('./worlds/' + name)
	world_selector.update_elements(worlds_list())

def worlds_list():
	worlds = []
	if os.path.isdir('./worlds'):
		for item in os.listdir('./worlds/'):
			if os.path.isfile('./worlds/' + item):
				worlds.append((item, ))
	return worlds if len(worlds) else [('No worlds', -1)]

def pause():
	global paused
	paused = not paused

def create_world():
	size = int(world_size.get_value()[0])
	name = world_name.get_value()
	global aMap, active_menu, aMapBack
	if not os.path.isdir('./worlds'): os.mkdir("./worlds")
	if not name:
		name = 'world' + str(random.randint(0, 9999))
	generate_map(size)
	world = {'map' : aMap, 'mapBack' : aMapBack, 'eq' : [[0 for x in range(2)] for y in range(9)], 'player' : {'X' : random.randint(1, size - 1), 'Y' : random.randint(1, size - 1), 'Direction' : 2}}
	if os.path.isfile('./worlds/' + name):
		count = 1
		while os.path.isfile('./worlds/' + name + str(count)):
			count += 1
		name = name + str(count)
	file = open('./worlds/' + name, 'w')
	file.write(json.dumps(world))
	world_selector.update_elements(worlds_list())
	#world_selector.set_value(name)
	active_menu = 1
	
def save_game():
	global playing
	name = world_selector.get_value()[0]
	world = {'map' : aMap, 'mapBack' : aMapBack, 'eq' : ItemBar, 'player' : oPlayer}
	file = open('./worlds/' + name, 'w')
	file.write(json.dumps(world))
	playing = False
	switch_menu(0)
	pause()

def disconnect():
	global playing, s
	try:
		s.close()
	except:
		pass
	playing = False
	switch_menu(0)
	pause()
	

theme = pygame_menu.themes.THEME_DEFAULT
theme.menubar_close_button = False

window = pygame.display.set_mode((width, height))#, pygame.FULLSCREEN)

menus = []

menus.append(pygame_menu.Menu(height, width, 'Pycraft', theme=theme))
menus[0].add_button('Single player', switch_menu, 1)
menus[0].add_button('Multi player', switch_menu, 4)
menus[0].add_button('Settings', switch_menu, 0)
menus[0].add_button('Quit', switch_menu, -1)

menus.append(pygame_menu.Menu(height, width, 'Single player', theme=theme))
menus[1].add_label('Select world', font_size=18)
world_selector = menus[1].add_selector('', [('No worlds', -1)])
menus[1].add_button('Play', start_game)
menus[1].add_button('Delete', delete_world)
menus[1].add_button('Create', switch_menu, 2)
menus[1].add_button('Back', switch_menu, 0)
worlds = worlds_list()
if len(worlds): world_selector.update_elements(worlds)

menus.append(pygame_menu.Menu(height, width, 'Create world', theme=theme))
menus[2].add_label('Select world size', font_size=18)
world_size = menus[2].add_selector('', [('128',), ('256',), ('512',), ('1024', ), ('2048', )])
world_name = menus[2].add_text_input('World name: ', default='new world', maxchar=100, maxwidth=28, font_size=18)
menus[2].add_button('Create', create_world)
menus[2].add_button('Back', switch_menu, 1)

menus.append(pygame_menu.Menu(height, width, 'Game paused', theme=theme))
menus[3].add_button('Back to game', pause)
menus[3].add_button('Save and exit', save_game)

menus.append(pygame_menu.Menu(height, width, 'Multi player', theme=theme))
server_address = menus[4].add_text_input('Server address: ', maxchar=100, maxwidth=28, font_size=18)
menus[4].add_button('Connect', start_game_multi)
menus[4].add_button('Back', switch_menu, 0)

menus.append(pygame_menu.Menu(height, width, 'Multi player', theme=theme))
menus[5].add_button('Back to game', pause)
menus[5].add_button('Disconnect', disconnect)

#Main loop
while True:
	pygame_events = pygame.event.get()
	for event in pygame_events:
		if event.type == pygame.QUIT:
			if playing == 2: disconnect()
			pygame.quit()
			quit()
		if event.type == pygame.KEYUP:
			key = None
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				if playing == 2:
					active_menu = 5
				else:
					active_menu = 3
				pause()
			else:
				key = event.key
			
	window.fill((0, 0, 0))
	
	if playing and not paused:
		
		PlayerMove(key)
		MouseControl()
	
		DrawMap()
	elif active_menu == -1:
		break
	else:
		menus[active_menu].update(pygame_events)
		menus[active_menu].draw(window)
	
	pygame.display.update()
	clock.tick(60)