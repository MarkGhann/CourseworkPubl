class Task:
    def __init__(self,index=0,priority=0,timeinterval=[0,1],proc=0,maj_fr = 10000, deadline = 1, per = 100, Dep = set(), Inf = set(),anomal = set()):
        self.priority = priority
        self.timeinterval = timeinterval
        self.proc = proc
        self.Dep = Dep
        self.index = index
        self.Inf = Inf
        self.level = int(0)
        self.anomal = anomal
        self.chek = False
        self.maj_fr = maj_fr
        self.per = per
        self.deadline = deadline
    def printt(self):
        print(self.priority, self.timeinterval, self.proc, self.Dep, self.index, self.Inf)

class Mass:
    def __init__(self,src,dst,dly):
        self.src = src
        self.dst = dst
        self.dly = dly
    def printt(self):
        print(self.scr, self.dst, self.dly)

class Core:
    def __init__(self,hw = 0,TaskSet = set()):
        self.hw = hw
        self.tasks = TaskSet
        self.stop = 0
    def add_task(self,task):
        (self.tasks).add(task)

class Level:
	def __init__(self,tasks = set(),dep = 0):
		self.tasks = tasks
		self.dep = dep

class Graph:
    def __init__(self,TaskSet,CoreSet, mass, state = "nulldep"):
        self.mass = mass
        self.Tree = dict()
        self.path = dict()
        self.Cores = CoreSet
        self.roots = {-1}
        self.graphroot = Task(-1,-1,[0,0],-1)
        for task in TaskSet:
            self.Tree[task.index] = task
        self.num = self.Tree.keys()
        self.Tree[-1] = self.graphroot
        for i in self.Tree:
            if i == -1:
                continue
            if len(self.Tree[i].Dep) == 0:
                self.graphroot.Inf.add(i)
                self.Tree[i].Dep = {-1}

    def paths(self):
        self.path[0] = [-1]
        self.prepaths(-1,0) 
        return self.path  
     
    def prepaths(self,key = 0, fathpos = -1): # all paths 
        leng = len(self.Tree[key].Inf)
        s = 1
        for i in self.Tree[key].Inf:
            if s == leng and fathpos != -1:
                n = fathpos
            elif fathpos != -1:
                n = self.copypath(fathpos)
            self.path[n] += [i]
            self.prepaths(i,n)
            s += 1
        return None

    def get_task(self,key=0):
        return self.Tree[key]

    def get_tasks_proc(self,HW):
        return self.Cores[HW]

    def task_in_path(self,task,path): # is this task in the path? 
        for i in path:
            if task.index == i:
                return True
        return False

    def copypath(self, pos):
        P = []
        for i in self.path[pos]:
            P += [i]
        n = len(self.path)
        self.path[n] = P
        return n

    def get_proc(self,ind):
        return self.Tree[ind].proc

    def get_prior(self,ind):
        return self.Tree[ind].priority

    def inheritance(self,Paths_to_Tk):
        AnomalSet = set()
        for path in Paths_to_Tk.values():
            for j in path:
            	AnomalSet.update(self.get_anomal(j))
        return AnomalSet

    def above_above(self,Above_to_Tm,AnomalSet,Gr,period):
        DummySet = set()
        for i in Above_to_Tm:
            if Gr.get_task(i).per != period:
                continue
            if Gr.get_task(i).chek:
                continue
            Gr.get_task(i).chek = True
            DummySet.add(i)
            DummySet.update(self.dummy(i,Gr,period)) 
        AnomalSet.update(DummySet)
        return AnomalSet

    def under_above(self,Above_to_Tk,Above_to_Tm,AnomalSet):
        f = False
        for i in Above_to_Tm:
            for j in Above_to_Tk:
                if  i == j or i in self.Tree[j].Inf:
                    f = True
                    break		
        return f

    def above_under(self,Above_to_Tk,Above_to_Tm,AnomalSet):
        f = False
        for i in Above_to_Tm:
            for j in Above_to_Tk:
                if  i == j or i in self.Tree[j].Dep:
                    f = True
                    break		
        return f

    def dummy(self,i,Gr,period):
        if i == -1:
            return set()
        DummySet = set()
        ProcTaskSet = (self.get_tasks_proc(self.get_proc(i))).copy()
        for a in ProcTaskSet:
            if Gr.get_task(i).per != period:
                continue
            if self.get_prior(a) <= self.get_prior(i):
                continue
            if Gr.get_task(i).chek:
                continue
            Gr.get_task(i).chek = True
            DummySet.add(a)
            DummySet.update(self.dummion(a,Gr,period))
        return DummySet

    def dummion(self,i,Gr,period):
        if i == -1:
            return set()
        DummionSet = set()
        task = self.get_task(i)
        ProcTaskSet = (self.get_tasks_proc(self.get_proc(i))).copy()
        Del = set()
        for a in ProcTaskSet:
            if Gr.get_task(i).per != period:
                Del.add(a)
            if self.get_prior(a) <= self.get_prior(i):
                Del.add(a)
            if Gr.get_task(a).chek:
                Del.add(a)
            Gr.get_task(a).chek = True
        ProcTaskSet.difference_update(Del)
        for a in task.Dep:
            if Gr.get_task(i).per != period:
                continue
            if Gr.get_task(a).chek:
                continue
            Gr.get_task(a).chek = True
            ProcTaskSet.add(a)
        DummionSet.update(ProcTaskSet)
        for a in ProcTaskSet:
            DummionSet.update(self.dummion(a,Gr,period))
        return DummionSet

    def get_anomal(self,j):
        return self.Tree[j].anomal

    def set_anomal(self,Anomal,j):
        Anomal.discard(self.graphroot.index)
        self.Tree[j].anomal = Anomal
        return None

    def get_above_paths(self,j):
        above_paths = dict()
        n = 0
        for k in self.path:
            path = self.path[k]
            if len(self.Tree[path[-1]].Inf) != 0:
                continue
            if not self.task_in_path(self.get_task(j),path):
                continue
            above = []
            for i in path:
                if i == j:
                    break
                above += [i]
            above_paths[n] = above
            n += 1
        return above_paths

    def get_under_paths(self,j):
        under_paths = dict()
        n = 0
        for k in self.path:
            path = self.path[k]
            if len(self.Tree[path[-1]].Inf) != 0:
                continue
            flag = False
            under = []
            for i in path:
                if i == j:
                    flag = True
                if flag:
                    under += [i]
            if flag:
                under_paths[n] = under
                n += 1
        return under_paths

    def levels(self,paths):
        all_levels = dict()
        max_size = 0
        for path in paths.values():
            if len(path)>max_size:
                max_size = len(path)
        for path in paths.values():
            spec = path[-1]
            if (self.Tree[spec].Inf) == 0:
                continue
            n = 0
            for task in path:
                if self.Tree[task].level < n:
                    self.Tree[task].level = n
                n += 1
        for size in range(1,max_size):
            tasks = set()
            for ki in self.Tree.keys():
                if self.Tree[ki].level == size:
                    tasks.add(ki)
            all_levels[size] = Level(tasks,size)
        return all_levels

    def dischek(self):
        for k in self.Tree:
            T = self.Tree[k]
            if T.chek:
                T.chek = False
		
	
