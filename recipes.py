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
			for pY in range(len(self.pattern[0])):
				for pX in range(len(self.pattern)):
					if self.pattern[pX][pY] != 0:
						self.ingredients +=1
		
	def __init__(self):
		self.recipes = []
		
	def addRecipe(self, pattern_row1, pattern_row2, pattern_row3, result, amount):
		self.recipes.append(self.Recipe(pattern_row1, pattern_row2, pattern_row3, result, amount))
	
	def Match(self, compare):
		size = 2
		for i in range(6, 8):
			if compare[i][0]: size = 3
		for recipe in self.recipes:
			for iX in range(size // recipe.size[0]):
				for iY in range(size // recipe.size[1]):
					match = 0
					for pY in range(recipe.size[1]):
						for pX in range(recipe.size[0]):
							if compare[2 * (pY + iY) + pX + iX][0] == recipe.pattern[pX][pY]:
								match += 1
					empty = sum(x.count(0) for x in compare) // 2
					if size == 2:
						empty -= 5
					if match == recipe.ingredients and empty == size ** 2 - recipe.ingredients:
						return (recipe.result, recipe.amount)
		return (0, 0)		
							
recipes = Recipes()

################# Row 1		Row 2		Row 3		Result	Amount		#Recipe
recipes.addRecipe([6], 		False, 		False, 		3,		4)			#Log -> 4 Wooden planks
recipes.addRecipe([3], 		[3], 		False, 		14,		4)			#2 Wooden planks -> 4 Sticks
			