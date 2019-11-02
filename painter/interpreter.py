class Interpreter():

	def __init__(self,fname,colors,instructions,nrows=30,ncols=30):
		self.filename = fname
		self.mapping = {}
		for color,instruction in zip(colors,instructions):
			self.mapping[color] = instruction
		print(self.mapping)
		self.instructions = []
		self.nrows = nrows
		self.ncols = ncols

	def readGrid(self):
		with open(self.filename,"r") as f:
			dims = f.readline().rstrip().split(" ")
			rows = int(dims[0])
			num = 0
			lastColor = (-1,-1,-1)
			for line in f:
				if "." in line:
					break
				line = line.rstrip()
				if num%self.nrows == 0:
					self.instructions.append([])
				color = line.split(",")
				color = tuple([int(x) for x in color])
				if color != lastColor:
					if (num//self.nrows)%2 == 0:
						self.instructions[num//self.nrows].append(self.mapping[color])
					else:
						self.instructions[num//self.nrows].insert(0,self.mapping[color])
				num += 1
				lastColor = color

realColors = [(255,0,0),(255,128,0),(204,204,255),(200,50,200),(0,153,153),(255,204,153),(255,255,0),(30,100,100),(0,255,0),(0,255,255),(70,70,70),(0,128,255),(127,0,255),(255,0,255),(229,255,204),(153,0,76),(255,0,127),(128,128,128),(50,90,160),(255,255,255)]
instructions = ["Save R1","Save R2","Save R3","Load R1","Load R2","Load R3","Add","Subtract","Multiply","Divide","Mod","Exit","CastToChar","CastToInt","CastToFloat","Print","Pass","Pass","Pass","Pass"]
a = Interpreter("thing.txt",realColors,instructions)
a.readGrid()
print(a.instructions)


