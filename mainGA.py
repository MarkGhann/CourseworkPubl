import sys as system
import subprocess as sub
import anomaltasks as ata
import genetics as ge
import time
import threading


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
	#input("press any key to continue")
	for i in G.Tree.keys():
		G.Tree[i].exac = G.get_task(i).timeinterval[1]
	WCRT2,cc1 = ge.ifitness(dict(),G,num,NAME1,NAME2,cc)
	for i in G.Tree.keys():
		G.Tree[i].exac = G.get_task(i).timeinterval[1]
	start_timega = time.time()
	if (count >= 0):
		res_time, ind, cc = ge.genetic(G,num,NAME1,NAME2)
	end_timega = time.time() - start_timega
	if cc == -1 or count == -1 or cc1 == -1:
		print("Incorrect ! number:",num," WCRT base:",WCRT2," WCRT GA:",res_time, " Scenario:", ind, " count(iterations):", cc, " working time:",end_timega)
		#input()
		#continue
		#break
	else:
		print("Correct ! number:",num," WCRT base:",WCRT2," WCRT GA:",res_time, " Scenario:", ind, " count(iterations):", cc, " working time:",end_timega)
	finf = open("output.xml",'w')
	finf.write("WCRT GA: " + str(res_time)+"\nTime: "+str(end_timega)+"\nsolution: " + str(ind) + "\nTask number: " + str(num) + "\nWCRT BS: " + str(WCRT2))
	finf.close()
	#tasks += [(num,res_time,cc,WCRT1,WCRT2,end_timebf,end_timega)]
#for i in range(len(tasks)):
#	print(" ",i," ",tasks[i][0]," ",tasks[i][1]," ",tasks[i][2]," ",tasks[i][3]," ",tasks[i][4]," ",tasks[i][5]," ",tasks[i][6])
print("--- %All time:  ---", (time.time() - start_time1))
if No_flag:
	print("In this system is no a task number",nom)
