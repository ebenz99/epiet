from tkinter import messagebox

class Interpreter():

	def __init__(self,fname,instructions,nrows=30,ncols=30):
		self.filename = fname
		self.mapping = {}
		colors = [
			(255,0,0),
			(0,153,153),
			(0,255,0),
			(127,0,255),
			(255,0,127),		#5
			(255,128,0),
			(255,204,153),
			(0,255,255),
			(255,0,255),
			(128,128,128),		#10
			(204,204,255),
			(255,255,0),
			(70,70,70),
			(229,255,204),
			(50,90,160),		#15
			(200,50,200),
			(30,100,100),
			(0,128,255),
			(153,0,76),
			(255,255,255)]
		for color,instruction in zip(colors,instructions):
			self.mapping[color] = instruction
		self.instructions = []
		self.nrows = nrows
		self.ncols = ncols

	def readGrid(self):
		with open(self.filename,"r") as f:
			dims = f.readline().rstrip().split(" ")
			rows = int(dims[0])
			num = 0
			lastColor = (-1,-1,-1)
			lastEndlineColor = (-1,-1,-1)
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
					#self.instructions[num//self.nrows].append(self.mapping[color])

				num += 1
				lastColor = color
		flatten_list = [j for sub in self.instructions for j in sub]
		i = 1
		while i < len(flatten_list):
			if flatten_list[i] == flatten_list[i-1]:
				del flatten_list[i]
			else:
				i+=1
		self.instructions = flatten_list

	def execute(self):
		r1 = 1
		r2 = 1
		r3 = 1
		acc = 0
		strReg = ""
		for instruction in self.instructions:
			if instruction == "Save R1":
				r1 = acc
			elif instruction == "Save R2":
				r2 = acc
			elif instruction == "Save R3":
				r3 = acc
			elif instruction == "Load R1":
				acc = r1
			elif instruction == "Load R2":
				acc = r2
			elif instruction == "Load R3":
				acc = r3
			elif instruction == "Add":
				acc = acc + r3
			elif instruction == "Subtract":
				acc = acc - r3
			elif instruction == "Multiply":
				acc = acc * r3
			elif instruction == "Divide":
				acc = acc // r3
			elif instruction == "Mod":
				acc = acc % r3
			elif instruction == "CastToChar":
				acc = chr(acc)
			elif instruction == "CastToInt":
				acc = ord(acc)
			elif instruction == "CastToFloat":
				try:
					acc = float(acc)
				except:
					pass
			elif instruction == "Print":
				messagebox.showinfo("output",str(acc))
			elif instruction == "Exit":
				break
			elif instruction == "strPrint":
				messagebox.showinfo("output",str(strReg))
			elif instruction == "strAppend":
				strReg += acc
			elif instruction == "strClear":
				strReg = ""
			else:
				pass
		return None
