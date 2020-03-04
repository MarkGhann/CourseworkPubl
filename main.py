import sys as system
import subprocess as sub
import anomaltasks as ata
import genetics as ge
import time
import threading
import imet

start_time = time.time()

NAME1 = "data.xml"
NAME2 = "scenario.xml"

G = ata.anomal_tasks("input.xml")
G.Tree.pop(-1)
tasks = []
tasksBF = []
start_time1 = time.time()
Ind = None
count = 0
cc = -1
res_time = 0
WCRT1 = 0
nom = int(input("Task num: "))
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
	start_timega = time.time()
	if (count >= 0):
		input("what?")
		res_time, ind = imet.imitation(G,num,NAME1,NAME2)
		cc = 1
	end_timega = time.time() - start_timega
	if cc == -1 or count == -1 or cc1 == -1:
		print("Incorrect ! number:",num," WCRT base:",WCRT2," WCRT GA:",res_time, " Scenario:", ind, " count(iterations):", cc, " working time:",end_timega)
		break
	else:
		print("Correct ! number:",num," WCRT base:",WCRT2," WCRT GA:",res_time, " Scenario:", ind, " count(iterations):", cc, " working time:",end_timega)
	finf = open("file_inf",'w')
	finf.write(str(num)+" "+str(res_time)+" "+str(WCRT1)+" "+str(count)+" "+str(cc))
	finf.close()
print("--- %All time:  ---", (time.time() - start_time1))
if No_flag:
	print("In this system is no a task number",nom)
