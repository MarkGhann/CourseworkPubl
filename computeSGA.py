filename = "output"
postfix = ".xml"
maxW = 0
maxT = 0
W = []
T = []
for filenumber in range(0, 100):
	sfile = open(filename + str(filenumber) + postfix)
	wcrt, time = int(sfile.readline().split(' ')[2]), float(sfile.readline().split(' ')[1])
	maxW += wcrt
	W += [wcrt]
	maxT += time
	T += [time]
	sfile.close()

aveW = maxW/100
aveT = maxT/100
f = open("ave.txt", "w")
f.write("ave: " + str(aveW) + "\n" + "time: " + str(aveT))
f.close()

S = 0
Sw = 0
St = 0

for i in range(0, 100):
	Sw += W[i] - aveW
	St += T[i] - aveT

Sw = (1/99) * Sw
St = (1/99) * St

f = open("SGA.txt", "w")
f.write(str(Sw) + " " + str(aveW) + "\n" + str(St) + " " + str(aveT) )
f.close()



