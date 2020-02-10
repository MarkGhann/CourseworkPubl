import random as rn
import anoclasses as cl

class probabil:
	def __init__(self,i,p):
		self.time = i
		self.P = p

def get_time_p_A(task):
	a = task.timeinterval[0]
	b = task.timeinterval[1]
	b = int(b)
	y = int(a)
	if a > y:
		y += 1
	a = y
	#c = b-a
	#P = 1/c
	N = rn.randrange(a,b,1)
	return N #probabil(N,P)
	
def get_time_p_B(task):
	a = task.timeinterval[0]
	b = task.timeinterval[1]
	N = rn.randrange(0,1,1)
	if N == 0:
		y = int(a)
		if a > y:
			y += 1
		a = y
		return probabil(a,0.5)
	else:
		return probabil(int(b),0.5)

def points_A(G,num):
	Points = {k:probabil(G[k].timeinterval[1],1) for k in sorted(G.keys())}
	task = G[num]
	for T in task.anomal:
		Points[T] = get_time_p_A(G[T])
	return Points

def points_B(G,num):
	Points = {k:probabil(G[k].timeinterval[1],1) for k in sorted(G.keys())}
	task = G[num]
	for T in task.anomal:
		Points[T] = get_time_p_B(G[T])
	return Points
