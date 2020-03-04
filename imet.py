import copy
import os as osy
import subprocess as sub
import random as rand
import anopoi as apo
import genclasses as gec
import xml.dom.minidom as xm
import math

def State(G, task):
    for k in G.Tree.keys():
        if k in G.get_task(task).anomal:
            G.get_task(k).exac = apo.get_time_p_A(G.get_task(k))
        else:
            G.get_task(k).exac = G.get_task(k).timeinterval[1]
    return G
    
def NOD(a,b):
    while b:
        a, b = b, a % b
    return a

def ocr(dig):
    a = "" +'"'
    a += str(dig)
    return a + '"'

def create_sys(G,name):
    f = open(name,'w')
    f.write("<system>\n")
    start = 0
    stop = 2000000
    task = G.get_task(0)
    stop = task.maj_fr
    for i in range(len(G.Cores)):
        f.write('\t<module major_frame='+ocr(stop)+' name="Module'+str(i)+'">\n')
        f.write('\t\t<partition id="0" name="m0_part0"  scheduler="FPPS">\n')
        for j in G.get_tasks_proc(i):
            task = G.get_task(j)
            f.write('\t\t\t<task id='+ocr(task.index)+' name="task'+str(task.index)+'" wcet='+ocr(task.exac)+' prio='+ocr(task.priority)+' offset="0" period='+ocr(task.per)+' deadline='+ocr(task.deadline)+'/>\n')
        f.write("\t\t</partition>\n")
        f.write('\t\t<window start='+ocr(start)+' stop='+ocr(stop)+' partition="0"/>\n')
        f.write("\t</module>\n")
    for j in G.mass:
        f.write('\t<link src='+ocr(j.src)+' dst='+ocr(j.dst)+' delay='+ocr(j.dly)+'/>\n')
    f.write("</system>\n")
    f.close()
    return None

def use(name1,name2):
    sub.call("./compute.sh")
    return None

#Help(Others)
def wcrtH(G,name,task1,dom):
    tasks = dom.getElementsByTagName("task")
    WCRT = 0
    number = 0
    for t in tasks:
        task = int(t.getAttribute("id"))
        if task != task1:
            period = G.get_task(task).per
            for child in t.getElementsByTagName("job"):
                beg = child.getElementsByTagName("event")[0]
                end = child.getElementsByTagName("event")[-1]
                if end.getAttribute("type") != "finished":
                    print("Others, No finish task: ",task," job:",number+1)
                    #input()
                    return 0
                if not beg:
                    print("Others, there's no task: ",task," job:",number)
                    #input()
                    return 0
                start = number*period
                stop = int(end.getAttribute("time"))
                tmp = stop - start
                if tmp == 0:
                    print("Others, WCRT ZERRO task: ",task," job:",number)
                    #input()
                    return 0
                if tmp == period:
                    flag = False
                    sh = 0
                    summa = 0
                    for s in child.getElementsByTagName("event"):
                        if s.getAttribute("type") == "exec" and not flag:
                            sh = int(s.getAttribute("time"))
                            flag = True
                        elif s.getAttribute("type") == "exec" and flag:
                            print("s.getAttribute(type) == exec and not flag. Task ",task, " summa: ",summa," exec: ",G.get_task(task).exac," job: ",number+1)
                            #input()
                            return 0
                        if (s.getAttribute("type") == "preempt" or s.getAttribute("type") == "finished") and flag:
                            sh = int(s.getAttribute("time")) - sh
                            summa += sh
                            flag = False
                        elif (s.getAttribute("type") == "preempt" or s.getAttribute("type") == "finished") and not flag:
                            print("s.getAttribute(type) != exec and not flag. Task ",task, " summa: ",summa," exec: ",G.get_task(task).exac," job: ",number+1)
                            #input()
                            return 0
                    if summa != G.get_task(task).exac:
                        print("WCRT == period, but exec' summa != task.exec. Task: ", task, " summa: ",summa," exec: ",G.get_task(task).exac," job: ",number+1)
                        #input()
                        return 0
                if tmp > WCRT:
                    WCRT = tmp
                number += 1
            break
    if number == 0:
        print(" the number of jobs == 0 ! in the main cycle task: ",task)
    return WCRT
    
def wcrt(G,name,task):
    f = open(name,'r')
    dom = xm.parse(name)
    dom.normalize()
    tasks = dom.getElementsByTagName("task")
    WCRT = 0
    tmpH = wcrtH(G,name,task,dom)
    print("tmpH = ",tmpH)
    if tmpH == 0:
        return 0
    period = G.get_task(task).per
    number = 0 #the number of a job
    for t in tasks:
        if int(t.getAttribute("id")) == task:
            for child in t.getElementsByTagName("job"):
                beg = child.getElementsByTagName("event")[0]
                end = child.getElementsByTagName("event")[-1]
                if end.getAttribute("type") != "finished":
                    print("Main, No finish task: ",task," job:",number)
                    #input()
                    return 0
                if not beg:
                    print("Main, there's no task: ",task," job:",number)
                    #input()
                    return 0
                start = number*period
                stop = int(end.getAttribute("time"))
                tmp = stop - start
                if tmp == 0:
                    print("bad wcrt in the main cycle ",tmp)
                    return 0
                if tmp == period:
                    flag = False
                    sh = 0
                    summa = 0
                    for s in child.getElementsByTagName("event"):
                        if s.getAttribute("type") == "exec" and not flag:
                            sh = int(s.getAttribute("time"))
                            flag = True
                        elif s.getAttribute("type") == "exec" and flag:
                            print("s.getAttribute(type) == exec and not flag. Task ",task, " summa: ",summa," exec: ",G.get_task(task).exac," job: ",number+1)
                            #input()
                            return 0
                        if (s.getAttribute("type") == "preempt" or s.getAttribute("type") == "finished") and flag:
                            sh = int(s.getAttribute("time")) - sh
                            summa += sh
                            flag = False
                        elif (s.getAttribute("type") == "preempt" or s.getAttribute("type") == "finished") and not flag:
                            print("s.getAttribute(type) != exec and not flag. Task ",task, " summa: ",summa," exec: ",G.get_task(task).exac," job: ",number+1)
                            #input()
                            return 0
                    if summa != G.get_task(task).exac:
                        print("WCRT == period, but exec' summa != task.exec. Task: ", task, " summa: ",summa," exec: ",G.get_task(task).exac," job: ",number+1)
                        #input()
                        return 0
                if tmp > WCRT:
                    WCRT = tmp
                number += 1
            break
    if number == 0:
        print(" the enumber of jobs == 0 ! in the main cycle task: ",task)
    return WCRT

def comput_wcrt(F,task,name1,name2):
    create_sys(F,name1)
    use(name1,name2)
    fa = wcrt(F,name2,task)
    return fa
    
def initialState(G,task,nameinp,nameout):
    state = State(G, task)
    for k in state.Tree.values():
        k.exac = k.timeinterval[1]
    return state, 100

def getWCRT(G, task, nameinp,nameout):
    return comput_wcrt(G, task, nameinp, nameout)

def lowT(T):
    return T/1

def setState(T, WCRT, new_WCRT, new_state, state):
    E = new_WCRT - WCRT
    if E > 0:
        pass
    else:
        prob = math.exp(-E/T)
        r = rand.random()
        print("GOOD <-------------------------------------", r)
        if r <= prob:
            WCRT = new_WCRT
            state = new_state
        T = lowT(T)
    return state, WCRT, T
	
def getState(G, task):
    state = State(G, task)
    return state

def imitation(G,task,nameinp,nameout):
    count = 1
    state, T = initialState(G,task,nameinp,nameout)
    search_state = state
    maxWCRT = WCRT = getWCRT(state, task, nameinp, nameout)
    if not state:
        print("Sth is going wrong, the state is empty.")
        return 0, None
    while count < 10:
        new_state = getState(G, task)
        print("--------------------------------")
        for a in new_state.Tree.values():
            print(task, "---> ", a.index, "   ", a.exac, "   ", a.timeinterval)
        print("--------------------------------")
        new_WCRT = getWCRT(new_state, task, nameinp,nameout)
        print("new WCRT = ", new_WCRT)
        state, WCRT, T = setState(T, WCRT, new_WCRT, new_state, state)
        if maxWCRT < WCRT:
            count = 1
            maxWCRT = WCRT
            search_state = state
        else:
            count += 1
    return maxWCRT, state
