from pygame import image

class Blocks():
	class Block():
		def __init__(self, name, mineable, placeable, walkable, digtime, stack, texture):
			self.name = name
			self.mineable = mineable
			self.placeable = placeable
			self.walkable = walkable
			self.digtime = digtime
			self.texture = texture
			self.stack = stack
			
	def __init__(self):
		self.blocks = []
		
	def addBlock(self, name, mineable, placeable, walkable, digtime, stack, filepath):
		self.blocks.append(self.Block(name, mineable, placeable, walkable, digtime, stack, image.load(filepath)))
	
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
		
	def getStack(self, id):
		return self.blocks[id].stack

BLOCKS = './Assets/Blocks/'
blocks = Blocks()

################ Name				Mineable	Placeable	Walkable	Digtime		Max stack	Texture					ID
blocks.addBlock('Bedrock',			False,		True,		False,		0,			64,			BLOCKS + 'bedrock.png') #0
blocks.addBlock('Dirt background',	False,		False,		True,		0,			0,			BLOCKS + 'dirt_b.png') 	#1
blocks.addBlock('Dirt',				True,		True,		False,		150,		64,			BLOCKS + 'dirt.png') 	#2
blocks.addBlock('Wooden planks',	True,		True,		False,		250,		64,			BLOCKS + 'wood.png')	#3
blocks.addBlock('Tree',				True,		True,		False,		250,		0,			BLOCKS + 'log.png')		#4
blocks.addBlock('Leaves',			True,		True,		True,		100,		0,			BLOCKS + 'leaves.png')	#5
blocks.addBlock('Log',				True,		True,		False,		250,		64,			BLOCKS + 'log.png')		#6
blocks.addBlock('Tree sapling',		True,		True,		True,		0,			64,			BLOCKS + 'sapling.png')	#7
blocks.addBlock('Water',			False,		True,		False,		0,			0,			BLOCKS + 'water.png')	#8
blocks.addBlock('Sand background',	False,		False,		True,		0,			0,			BLOCKS + 'sand_b.png')	#9
blocks.addBlock('Sand',				True,		True,		False,		150,		64,			BLOCKS + 'sand.png')	#10
blocks.addBlock('Stone background',	False,		False,		True,		0,			0,			BLOCKS + 'stone_b.png')	#11
blocks.addBlock('Stone',			True,		True,		False,		500,		64,			BLOCKS + 'stone.png')	#12
blocks.addBlock('Cactus',			True,		True,		False,		150,		64,			BLOCKS + 'cactus.png')	#13
blocks.addBlock('Stick',			False,		False,		False,		0,			64,			BLOCKS + 'stick.png')	#14
blocks.addBlock('Wooden pickaxe',	False,		False,		False,		0,			1,			BLOCKS + 'wooden_pickaxe.png')	#15
blocks.addBlock('Stone pickaxe',	False,		False,		False,		0,			1,			BLOCKS + 'stone_pickaxe.png')	#16
blocks.addBlock('Iron pickaxe',		False,		False,		False,		0,			1,			BLOCKS + 'iron_pickaxe.png')	#17
blocks.addBlock('Gold pickaxe',		False,		False,		False,		0,			1,			BLOCKS + 'golden_pickaxe.png')	#18
blocks.addBlock('Diamond pickaxe',	False,		False,		False,		0,			1,			BLOCKS + 'diamond_pickaxe.png')	#19
blocks.addBlock('Cobblestone',		True,		True,		False,		500,			64,			BLOCKS + 'cobblestone.png')	#20
blocks.addBlock('Crafting table',		True,		True,		False,		250,			64,			BLOCKS + 'crafting_table.png')	#21