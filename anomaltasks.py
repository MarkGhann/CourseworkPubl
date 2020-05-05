import anoclasses as cl
import xml.dom.minidom as xm


def MinData(name):
	tasks = set()
	cores = set()
	Cori = dict()
	mass = []
	dom = xm.parse(name)
	for task in dom.getElementsByTagName("task"):
		tid = int(task.getAttribute("index"))
		pr = int(task.getAttribute("prio"))
		wcet = int(task.getAttribute("wcet"))
		bcet = int(task.getAttribute("bcet"))
		proc = int(task.getAttribute("proc"))
		mf = int(task.getAttribute("maj_fr"))
		ddl = int(task.getAttribute("deadline"))
		period = int(task.getAttribute("period"))
		t = task.getAttribute("Dep").split(',')[0]
		dep = task.getAttribute("Dep").split(',')
		inf = task.getAttribute("Inf").split(',')
		Dep = set()
		Inf = set()
		for i in dep:
			if not i:
				continue
			Dep.add(int(i))
		for i in inf:
			if not i:
				continue
			Inf.add(int(i))
		task = cl.Task(tid,pr,[bcet,wcet],proc,mf,ddl,period,Dep,Inf)
		task.printt()
		tasks.add(task)
		cores.add(proc)
	for i in cores:
		Cori[i] = set()
	for i in tasks:
		#print("iwas")
		Cori[i.proc].add(i.index)
	for link in dom.getElementsByTagName("tlink"):
		#print("iwas")
		src = link.getAttribute("src")
		dst = link.getAttribute("dist")
		dly = link.getAttribute("delay")
		#print("HERE ",dst)
		mass += [cl.Mass(src,dst,dly)]
	return tasks, Cori, mass

def anomal_tasks(name):
	Anom_tasks = set()
	Dt = set()
	Taski, Cori, mass = MinData(name)
	#print(mass)
	Gr = cl.Graph(Taski,Cori,mass,"nulldep")
	#print(Gr.paths())
	All_Levels = Gr.levels(Gr.paths())
	#noneorto_cycletomik = len(Gr.mass) - len(Gr.Tree) + len(Gr.graphroot.Inf)
	#if noneorto_cycletomik != 0:
		#print("noneorto_cyclotomik != 0. It is ",noneorto_cycletomik)
		#print("Arcs: ",len(mass)," Nodes: ",len(Gr.Tree)," components: ",len(Gr.graphroot.Inf))
		#cycletomik = cycle(Gr)
	for FS in sorted(All_Levels.keys()):
		#print("here")
		FindSet = All_Levels[FS]
		for task in FindSet.tasks:
			#print(task)
			period = Gr.get_task(task).per
			#Gr.get_task(task).printt()
			if type(task) == list:
				print("WRONG list type. Please, contact the developer")
				task = task[0]
			Paths_to_Tk = Gr.get_above_paths(task)
			Paths_after_Tk = Gr.get_under_paths(task)
			Anomal = Gr.inheritance(Paths_to_Tk)
			ProcTaskSet = (Gr.get_tasks_proc(Gr.get_proc(task))).copy()
			for Tm in ProcTaskSet:
				j = False
				#if Gr.get_task(Tm).per != period:
				#	continue
				if Gr.get_prior(Tm) <= Gr.get_prior(task):
					continue
				AnomalSet = set()
				Paths_to_Tm = Gr.get_above_paths(Tm)
				Paths_after_Tm = Gr.get_under_paths(Tm)
				for key in Paths_after_Tk:
					Under_to_Tk = Paths_after_Tk[key]
					for k in Paths_to_Tm:
						Above_to_Tm = Paths_to_Tm[k]
						if j:
							break
						j = Gr.under_above(Under_to_Tk,Above_to_Tm,AnomalSet)
				for key in Paths_to_Tk:
					Above_to_Tk = Paths_to_Tk[key]
					for k in Paths_after_Tm:
						Under_to_Tm = Paths_after_Tm[k]
						if j:
							break
						j = Gr.above_under(Above_to_Tk,Under_to_Tm,AnomalSet)
				for key in Paths_to_Tk:
					Above_to_Tk = Paths_to_Tk[key]
					for k in Paths_to_Tm:
						Above_to_Tm = Paths_to_Tm[k]
						if j:
							break
						AnomalSet = Gr.above_above(Above_to_Tm,AnomalSet,Gr,period)
					for k in AnomalSet:
						Gr.get_task(k).chek = False
				if not j:
					Anomal.update(AnomalSet)
					Gr.dischek()
			if task in Anomal:
				Anomal.remove(task)
			Gr.set_anomal(Anomal,task)
			#print("Dep: ",FindSet.dep," task num: ",task," Anomal tasks: ",Gr.get_anomal(task))
	print(" \n \n \n")
	for i in sorted(Gr.Tree.keys()):
		if i != -1:
			j = Gr.Tree[i]
			print("Dep: ",j.level," task num: ",j.index," Anomal tasks: ",j.anomal)
	return Gr
