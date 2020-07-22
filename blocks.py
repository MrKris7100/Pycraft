from pygame import image

class Blocks():
	class Block():
		def __init__(self, name, mineable, placeable, walkable, digtime, texture):
			self.name = name
			self.mineable = mineable
			self.placeable = placeable
			self.walkable = walkable
			self.digtime = digtime
			self.texture = texture
			
	def __init__(self):
		self.blocks = []
		
	def addBlock(self, name, mineable, placeable, walkable, digtime, filepath):
		self.blocks.append(self.Block(name, mineable, placeable, walkable, digtime, image.load(filepath)))
	
	def getName(self, id):
		return self.blocks[id].name
		
	def getDigtime(self, id):
		return self.blocks[id].digtime
		
	def getTexture(self, id):
		return self.blocks[id].texture
	
	def isMineable(self, id):
		return self.blocks[id].mineable
		
	def isPlaceable(self, id):
		return self.blocks[id].placeable
		
	def isWalkable(self, id):
		return self.blocks[id].walkable

BLOCKS = './Assets/Blocks/'
blocks = Blocks()

################ Name				Mineable	Placeable	Walkable	Digtime		Texture					ID
blocks.addBlock('Bedrock',			False,		True,		False,		0,			BLOCKS + 'bedrock.png') #0
blocks.addBlock('Dirt background',	False,		False,		True,		0,			BLOCKS + 'dirt_b.png') 	#1
blocks.addBlock('Dirt',				True,		True,		False,		150,		BLOCKS + 'dirt.png') 	#2
blocks.addBlock('Wooden planks',	True,		True,		False,		250,		BLOCKS + 'wood.png')	#3
blocks.addBlock('Tree',				True,		True,		False,		250,		BLOCKS + 'tree.png')	#4
blocks.addBlock('Leaves',			True,		True,		True,		100,		BLOCKS + 'leaves.png')	#5
blocks.addBlock('Log',				True,		True,		False,		250,		BLOCKS + 'log.png')		#6
blocks.addBlock('Tree sapling',		True,		True,		True,		0,			BLOCKS + 'sapling.png')	#7
blocks.addBlock('Water',			False,		True,		False,		0,			BLOCKS + 'water.png')	#8
blocks.addBlock('Sand background',	False,		False,		True,		0,			BLOCKS + 'sand_b.png')	#9
blocks.addBlock('Sand',				True,		True,		False,		150,		BLOCKS + 'sand.png')	#10
blocks.addBlock('Stone background',	False,		False,		True,		0,			BLOCKS + 'stone_b.png')	#11
blocks.addBlock('Stone',			True,		True,		False,		500,		BLOCKS + 'stone.png')	#12
blocks.addBlock('Cactus',			True,		True,		False,		150,		BLOCKS + 'cactus.png')	#13
