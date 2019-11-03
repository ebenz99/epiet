start,end,vals = 0,0,[]
nstart,nend,nvals = 0,0,[]

with open("eclec.txt","r") as f:
	start = f.readline()
	for line in f:
		vals.append(tuple(line.rstrip().split(",")))
	end = vals[-1]
	vals = vals[:-1]


with open("filler.txt","r") as f:
	nstart = f.readline
	for line in f:
		nvals.append(tuple(line.rstrip().split(",")))
	nend = nvals[-1]
	nvals = nvals[:-1]
