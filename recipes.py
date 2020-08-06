import math

class Recipes():
	class Recipe():
		def __init__(self, pattern_row1, pattern_row2, pattern_row3, result, amount):
			self.pattern = [pattern_row1]
			if pattern_row2: self.pattern.append(pattern_row2)
			if pattern_row3: self.pattern.append(pattern_row3)
			self.size = (len(self.pattern), len(self.pattern[0]))
			self.result = result
			self.amount = amount
			self.ingredients = 0
			for pY in range(self.size[1]):
				for pX in range(self.size[0]):
					if self.pattern[pX][pY] != 0:
						self.ingredients +=1
		
	def __init__(self):
		self.recipes = []
		
	def addRecipe(self, pattern_row1, pattern_row2, pattern_row3, result, amount):
		self.recipes.append(self.Recipe(pattern_row1, pattern_row2, pattern_row3, result, amount))
	
	def Match(self, compare):
		for recipe in self.recipes:
			for iX in range(math.ceil(3 / recipe.size[1])):
				for iY in range(math.ceil(3 / recipe.size[0])):
					match = 0
					for pY in range(recipe.size[0]):
						for pX in range(recipe.size[1]):
							if compare[pX + iX][pY + iY][0] and compare[pX + iX][pY + iY][0] == recipe.pattern[pY][pX]:
								match += 1
					empty = 0
					for pX in range(3):
						for pY in range(3):
							if compare[pX][pY][0] == 0:
								empty += 1
					if match == recipe.ingredients and empty == 3 ** 2 - recipe.ingredients:
						return [recipe.result, recipe.amount]
		return [0, 0]		
							
recipes = Recipes()

################# Row 1			Row 2			Row 3		Result	Amount		#Recipe
recipes.addRecipe([6], 			False, 			False, 		3,		4)			#4 Wooden planks
recipes.addRecipe([3], 			[3], 			False, 		14,		4)			#4 Sticks
recipes.addRecipe([3, 3], 		[3, 3], 		False, 		21,		1)			#Crafting table
recipes.addRecipe([3, 3, 3],	[0, 14, 0],		[0, 14, 0], 15,		1)			#Wooden pickaxe
recipes.addRecipe([20, 20, 20],	[0, 14, 0], 	[0, 14, 0], 16,		1)			#Stone pickaxe
recipes.addRecipe([3, 14, 3],	[3, 14, 3], 	False, 		22,		1)			#Fence
			