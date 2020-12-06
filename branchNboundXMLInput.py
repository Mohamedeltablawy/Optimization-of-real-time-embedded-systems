# -*- coding: utf-8 -*-
"""
Created on Sun Nov 22 19:22:27 2020

@author: tabla
"""

import xml.etree.ElementTree as ET
import sympy as sym
import math
from gekko import GEKKO
from pycpa import model
from pycpa import analysis
from pycpa import schedulers
from pycpa import graph
from pycpa import options

########################################################WCRT analysis
def spp_test(EX,T):
    # init pycpa and trigger command line parsing
    options.init_pycpa()

    # generate an new system
    s = model.System()

    # add two resources (CPUs) to the system
    # and register the static priority preemptive scheduler
    r1 = s.bind_resource(model.Resource("R1", schedulers.SPPScheduler()))


    # create and bind tasks to r1
    tasks=[]
    for i in range(len(EX)): 
        tasks.append(r1.bind_task(model.Task("T"+str(i+1)  , wcet=WCET[i], bcet=WCET[i], scheduling_parameter=T[i])))
        
        


    
    # register a periodic with jitter event model for T11 and T12
    for i in range(len(EX)):
        tasks[i].in_event_model = model.PJdEventModel(P=T[i], J=0)
    
    

    # perform the analysis
    print("Performing analysis")
    task_results = analysis.analyze_system(s)

    # print the worst case response times (WCRTs)
    print("Result:")
    for r in sorted(s.resources, key=str):
        for t in sorted(r.tasks, key=str):
            print("%s: wcrt=%d" % (t.name, task_results[t].wcrt))
            print("    b_wcrt=%s" % (task_results[t].b_wcrt_str()))
            
###################################################################
#######################################reading XML file
app=ET.parse('test.xml')
App=app.getroot()
Complexity={}
p1=[]
p2=[]
Complexity={}
x={}
ID_Ass={}


for i in App[0]:
    for t in range(len(App[0][1])):

        if i[t].tag=='Name':
            name=i[t].text
            print(i[t].text)
        elif i[t].tag=='weight':
            weight=i[t].text
            print(i[t].text)
    d={name :weight}
    Complexity.update(d)

         
for i in App[1]:
    if i.tag=='Ub':
        ub=int(i.text)
    elif i.tag=='Lb':
         lb=int(i.text)
print(ub,lb)

n=1
for c in range(len(App)-2):
    print(c)
    for i in App[c+2]:
        if i.tag=='Name':
            name=i.text
        elif i.tag=='WCET':
            WCET=i.text 
        elif i.tag=='precedence':
            Prec=i.text 

    ID_ass={name:n}
    ID_Ass.update(ID_ass)    
    d={name :[WCET,Prec]}
    x.update(d)
    n=n+1
        
WCET=[]
for i in x:
    sum=0
    t=x[i]
    t=t[0]
    res = t.replace(',',' ') 
    res = res.split() 
    for t in res:
       
        sum= sum +float(Complexity[t])
      
    WCET.append(sum)
n=1
for i in x:

    t=x[i]
    t=t[1]
    if t!=None:
        res = t.replace(',',' ') 
        res = res.split() 
        print(res)
        for t in res: 
            p1.append(n)
            p2.append(ID_Ass[t])
       
    n=n+1
#########################################

if __name__ == "__main__":
    print('Lower bound',lb)
    print('Upper bound',ub)
    print('WCET=',WCET)
    m = GEKKO(remote=False) # Initialize gekko
    m.options.SOLVER=1  # APOPT is an MINLP solver
    import time
    start_time = time.time()
    # optional solver settings with APOPT
    m.solver_options = ['minlp_maximum_iterations 5000', \
                        # minlp iterations with integer solution
                        'minlp_max_iter_with_int_sol 100', \
                        # treat minlp as nlp
                        'minlp_as_nlp 0', \
                        # nlp sub-problem max iterations
                        'nlp_maximum_iterations 50', \
                        # 1 = depth first, 2 = breadth first
                        'minlp_branch_method 3', \
                        # maximum deviation from whole number
                        'minlp_integer_tol 0.0005', \
                        # covergence tolerance
                        'minlp_gap_tol 0.0001']
    
    # Initialize variables
    Variable=[]
    
    for i in range(len(WCET)): 
        Variable.append(m.Var(value=1,lb=math.floor(math.log2(lb/10)),ub=math.floor(math.log2(ub /10)),integer=True))
    print(math.floor(math.log2(lb/10)),math.floor(math.log2(ub/10)))
    #initializing the equation
    y=WCET[0]/(10*2**Variable[0])
    for i in range(len(WCET)-1): 
        y+=WCET[i+1]/(10*2**Variable[i+1])
    
    # Equations
    m.Equation(y<0.99)
    #precdance
    for i in range(len(p1)):
        m.Equation(Variable[p2[i]-1]<Variable[p1[i]-1]-1)
    # Objective
    m.Obj(-(y)) 
    
    # Solve
    print('start')
    m.solve(disp=False)
    print('done')
    
    period=[]
    print('Results')
    for i in range(len(WCET)):
         print('T', i+1 , ': ' + str(10*2**Variable[i].value[0]))
         period.append(int(10*2**Variable[i].value[0]))
         
         
    print('Objective: ' + str(-1*m.options.objfcnval))
    spp_test(x,period)
    print("--- %s seconds ---" % (time.time() - start_time))
        
