import sys as system
import subprocess as sub
import anomaltasks as ata
import bruteforce as ge
import time
import threading

def turn(vals,f,G):
    l = len(vals)
    end = False
    j = 0
    for i in sorted(vals.keys()):
        ll = G.get_task(i).timeinterval[1] - G.get_task(i).timeinterval[0] + 1
        if f[j] >= ll:
            if j == l-1:
                end = True
                break
            f[j+1] += 1
            f[j] = 0
        vals[i] = G.get_task(i).timeinterval[0] + f[j]
        #print(G.get_task(i).timeinterval[0])
        if j == 0:
            f[j] += 1
        j += 1
    return vals,f,end

def BF(G,task,nameinp,nameout,anomal):
    vals = vm =dict()
    if not anomal:
        print("No anomals")
        return 0,0
    f = [0 for k in range(len(anomal))]
    for i in anomal:
        vals[i] = 0
    WCRT = -1
    end = False
    count = 0
    co = 0
    while not end:
        count += 1
        vals,f,end = turn(vals,f,G)
        tmp,co = ge.ifitness(vals,G,task,nameinp,nameout,co)
        if tmp > WCRT:
            vm = vals
            WCRT = tmp
    return WCRT, count, vm

vm = dict()
system.setrecursionlimit(100000)

start_time = time.time()

NAME1 = "data.xml"
NAME2 = "scenario.xml"
"""
if system.args[1] == 1:
	pass
else:
	pass
sub.call(system.args[2],"input.xml")
"""
G = ata.anomal_tasks("input.xml")
G.Tree.pop(-1)
tasks = []
tasksBF = []
start_time1 = time.time()
#input()
Ind = None
count = 0
cc = -1
res_time = 0
WCRT1 = 0
nom = int(system.argv[1])
No_flag = True
for num in G.num:
	if num < 0:
		continue
	if num != nom:
		continue
	else:
		No_flag = False
	if len(G.get_task(num).anomal) == 0:
		print("This task has no anomal tasks")
		break
	else:
		print("This task has",len(G.get_task(num).anomal),"anomal tasks")
		ovj = 1
		for ta in G.get_task(num).anomal:
			ovj *= G.get_task(ta).timeinterval[1] - G.get_task(ta).timeinterval[0] + 1
		print(" Number of possible solutions: ",ovj)
	for i in G.Tree.keys():
		G.Tree[i].exac = G.get_task(i).timeinterval[1]
	WCRT2,cc1 = ge.ifitness(dict(),G,num,NAME1,NAME2,cc)
	for i in G.Tree.keys():
		G.Tree[i].exac = G.get_task(i).timeinterval[1]
	start_timebf = time.time()
	WCRT1, count, vm = BF(G,num,NAME1,NAME2,G.Tree[num].anomal)
	end_timebf = time.time() - start_timebf
	if count == -1 or cc1 == -1:
		print("Incorrect ! number:",num," WCRT base:",WCRT2," WCRT GA:",WCRT1, " Scenario:", 'empty', " count(iterations):", cc, " working time:",end_timebf)
		#input()
		#continue
		break
	else:
		print("Correct ! number:",num," WCRT base:", WCRT2," WCRT GA:", WCRT1, " Scenario:", vm, " count(iterations):", cc, " working time:",end_timebf)
		#input()
	finf = open("output.xml",'w')
	finf.write("WCRT BF: " + str(WCRT1)+"\nTime: "+str(end_timebf) + "\nTask number: " + str(num) + "\nWCRT BS: " + str(WCRT2))
	finf.close()
	#tasks += [(num,res_time,cc,WCRT1,WCRT2,end_timebf,end_timega)]
#for i in range(len(tasks)):
#	print(" ",i," ",tasks[i][0]," ",tasks[i][1]," ",tasks[i][2]," ",tasks[i][3]," ",tasks[i][4]," ",tasks[i][5]," ",tasks[i][6])
print("--- %All time:  ---", (time.time() - start_time1))
if No_flag:
	print("In this system is no a task number",nom)
