# -*- coding: utf-8 -*-
"""
Created on Thu Sep 10 11:52:46 2020

@author: tabla
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Sep 10 10:26:02 2020

@author: Eltablawy
"""

import sympy as sym
import math
from gekko import GEKKO
from pycpa import model
from pycpa import analysis
from pycpa import schedulers
from pycpa import graph
from pycpa import options
from tkinter import *
import tkinter as tk

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
        tasks.append(r1.bind_task(model.Task("T"+str(i+1)  , wcet=x[i], bcet=x[i], scheduling_parameter=T[i])))
        
        


    
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
            

#########################################    GUI    #####################################
def close_window():
    x2 = entry2.get()
    No_Of_Tasks.append(int(float(x2)))
    root1.destroy()
    
def addtothematrix ():
    
    x1 = entry1.get()
    e=int(float(x1))
    x.append(e)
    root.destroy()
def close_window1():
    if int(float(e1.get()))==int(float(e2.get())):
        print("Wrong input")
    else:
        p1.append(int(float(e1.get())))
        p2.append(int(float(e2.get())))
        m[0]=0
    master.destroy()
    
def Prec():
    if int(float(e1.get()))==int(float(e2.get())):
        print("Wrong input")
    else:
        p1.append(int(float(e1.get())))
        p2.append(int(float(e2.get())))
    master.destroy()

    
x=[]  
No_Of_Tasks=[]
m=[1]
p1=[]
p2=[]
root1= tk.Tk()
                
canvas2 = tk.Canvas(root1, width = 400, height = 300,  relief = 'raised')
canvas2.pack()
#No of Tasks input                
label1 = tk.Label(root1, text='Total Number of Tasks')
label1.config(font=('helvetica', 14))
canvas2.create_window(200, 100, window=label1)             
entry2 = tk.Entry (root1) 
canvas2.create_window(200, 140, window=entry2)
#button
button2 = tk.Button(text='Next', command=close_window, bg='brown', fg='white', font=('helvetica', 9, 'bold'))
canvas2.create_window(200, 180, window=button2)
root1.mainloop() 
###################################################Upper bound
root1= tk.Tk()               
canvas2 = tk.Canvas(root1, width = 400, height = 300,  relief = 'raised')
canvas2.pack()                
label1 = tk.Label(root1, text='Upper bound')
label1.config(font=('helvetica', 14))
canvas2.create_window(200, 100, window=label1)                          
entry2 = tk.Entry (root1) 
canvas2.create_window(200, 140, window=entry2)
button2 = tk.Button(text='Next', command=close_window, bg='brown', fg='white', font=('helvetica', 9, 'bold'))
canvas2.create_window(200, 180, window=button2)               
root1.mainloop() 
#####################################################Lower bound
root1= tk.Tk()               
canvas2 = tk.Canvas(root1, width = 400, height = 300,  relief = 'raised')
canvas2.pack()                
label1 = tk.Label(root1, text='Lower bound')
label1.config(font=('helvetica', 14))
canvas2.create_window(200, 100, window=label1)                          
entry2 = tk.Entry (root1) 
canvas2.create_window(200, 140, window=entry2)
button2 = tk.Button(text='Next', command=close_window, bg='brown', fg='white', font=('helvetica', 9, 'bold'))
canvas2.create_window(200, 180, window=button2)               
root1.mainloop() 
############################################
while(m[0]==1):
    print(m)
    master = tk.Tk()
    tk.Label(master, 
             text="The Task No").grid(row=0)
    tk.Label(master, 
             text="depends on the Task No").grid(row=1)
    
    e1 = tk.Entry(master)
    e2 = tk.Entry(master)
    
    e1.grid(row=0, column=1)
    e2.grid(row=1, column=1)
    
    tk.Button(master, 
              text='Next', 
              command=Prec).grid(row=3, 
                                        column=0, 
                                        sticky=tk.W, 
                                        pady=4)
    tk.Button(master, 
              text='No more precedance', command=close_window1).grid(row=3, 
                                                           column=1, 
                                                           sticky=tk.W, 
                                                           pady=4)
    
    tk.mainloop()




####################################################################################

   
    

for i in range(No_Of_Tasks[0]):
        root= tk.Tk()
        
        canvas1 = tk.Canvas(root, width = 400, height = 300,  relief = 'raised')
        canvas1.pack()
        
        label1 = tk.Label(root, text='Calculate the Square Root')
        label1.config(font=('helvetica', 14))
         
        e=str(i+1)
        label2 = tk.Label(root, text="WCET of Task Nubmer " + e)
        label2.config(font=('helvetica', 10))
        canvas1.create_window(200, 100, window=label2)
        
        entry1 = tk.Entry (root) 
        
        canvas1.create_window(200, 140, window=entry1)
        button1 = tk.Button(text='Next', command=addtothematrix, bg='brown', fg='white', font=('helvetica', 9, 'bold'))
        canvas1.create_window(200, 180, window=button1)
        
        root.mainloop()
################################################          Ends of GUI     #################################################
if __name__ == "__main__":
    
    print(x)
    m = GEKKO() # Initialize gekko
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
                        'minlp_branch_method 2', \
                        # maximum deviation from whole number
                        'minlp_integer_tol 0.0005', \
                        # covergence tolerance
                        'minlp_gap_tol 0.0001']
    
    # Initialize variables
    Variable=[]
    print(round(math.log2(No_Of_Tasks[1]/10)))
    print(round(math.log2(No_Of_Tasks[2]/10)))
    for i in range(len(x)): 
        Variable.append(m.Var(value=1,lb=round(math.log2(No_Of_Tasks[2]/10)),ub=round(math.log2(No_Of_Tasks[1]/10)),integer=True))
    
    #initializing the equation
    y=x[0]/(10*2**Variable[0])
    for i in range(len(x)-1): 
        y+=x[i+1]/(10*2**Variable[i+1])
    
    # Equations
    m.Equation(y<1)
    for i in range(len(p1)):
        print("i=",i)
        m.Equation(Variable[p2[i]-1]<Variable[p1[i]-1]-1)
    # Objective
    m.Obj(-(y)) 
    
    # Solve
    m.solve(disp=False) 
    
    period=[]
    print('Results')
    for i in range(len(x)):
         print('T', i+1 , ': ' + str(10*2**Variable[i].value[0]))
         period.append(int(10*2**Variable[i].value[0])+0.1)
         
         
    print('Objective: ' + str(-1*m.options.objfcnval))
    spp_test(x,period)
    print("--- %s seconds ---" % (time.time() - start_time))
