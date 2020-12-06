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
import matplotlib.pyplot as plt
import numpy as np

############################################1 depth first
p1=[]
p2=[]
e=0
t=150 #Number of iteration
lb=20
ub=10000000
TR=0
Error1=0
runningTime1=[]
No_Tasks1=[]
ut_t1=[]
for i in range(5,t):
    print('i=',i)
    x=[]
    if __name__ == "__main__":
        for r in range(i):
            x.append(10)
        print('Lower bound',lb)
        print('Upper bound',ub)
        print('WCET=',x)
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
                            'minlp_branch_method 1', \
                            # maximum deviation from whole number
                            'minlp_integer_tol 0.0005', \
                            # covergence tolerance
                            'minlp_gap_tol 0.0001']
        
        # Initialize variables
        Variable=[]
        
        for i in range(len(x)): 
            Variable.append(m.Var(value=1,lb=math.floor(math.log2(lb/10)),ub=math.floor(math.log2(ub/10)),integer=True))
        
        #initializing the equation
        y=x[0]/(10*2**Variable[0])
        for i in range(len(x)-1): 
            y+=x[i+1]/(10*2**Variable[i+1])
        
        # Equations
        m.Equation(y<1)
        #precdance
        for i in range(len(p1)):
            m.Equation(Variable[p2[i]-1]<Variable[p1[i]-1]-1)
        # Objective
        m.Obj(-(y)) 
        
        # Solve
        try: 
            m.solve(disp=False)
            period=[]
            print('Results')
            for i in range(len(x)):
                 print('T', i+1 , ': ' + str(10*2**Variable[i].value[0]))
                 period.append(int(10*2**Variable[i].value[0])+0.1)
                 
                 
            print('Objective: ' + str(-1*m.options.objfcnval))
            #spp_test(x,period)
            l=(time.time() - start_time)
            print("--- %s seconds ---" % l)
            runningTime1.append(l)
            TR=TR+l
            No_Tasks1.append(i)
            ut_t1.append((-1*m.options.objfcnval))
            if (-1*m.options.objfcnval)>1:
                e=e+1
        except:
            Error1=Error1+1
            
        
        
plt.plot(No_Tasks1, runningTime1)
plt.ylabel('Running Time')
plt.xlabel('Number of Tasks')
plt.show()
plt.plot(No_Tasks1, ut_t1)
plt.ylabel('Utilization factor')
plt.xlabel('Number of Tasks')
plt.show()
print(No_Tasks1)
print(runningTime1)
print('Total running time=',TR)
######################################################

#############################################################3 lowest objective leaf
p1=[]
p2=[]
t=150
lb=20
ub=1000000
TR=0
Error3=0
runningTime3=[]
No_Tasks3=[]
ut_t3=[]
for i in range(5,t):
    print('i=',i)
    x=[]
    if __name__ == "__main__":
        for r in range(i):
            x.append(10)
        print('Lower bound',lb)
        print('Upper bound',ub)
        print('WCET=',x)
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
        
        for i in range(len(x)): 
            Variable.append(m.Var(value=1,lb=math.floor(math.log2(lb/10)),ub=math.floor(math.log2(ub/10)),integer=True))
        
        #initializing the equation
        y=x[0]/(10*2**Variable[0])
        for i in range(len(x)-1): 
            y+=x[i+1]/(10*2**Variable[i+1])
        
        # Equations
        m.Equation(y<1)
        #precdance
        for i in range(len(p1)):
            m.Equation(Variable[p2[i]-1]<Variable[p1[i]-1]-1)
        # Objective
        m.Obj(-(y)) 
        
        # Solve
        try: 
            m.solve(disp=False)
            period=[]
            print('Results')
            for i in range(len(x)):
                 print('T', i+1 , ': ' + str(10*2**Variable[i].value[0]))
                 period.append(int(10*2**Variable[i].value[0])+0.1)
                 
                 
            print('Objective: ' + str(-1*m.options.objfcnval))
            #spp_test(x,period)
            l=(time.time() - start_time)
            print("--- %s seconds ---" % l)
            runningTime3.append(l)
            TR=TR+l
            No_Tasks3.append(i)
            ut_t3.append((-1*m.options.objfcnval))
            if (-1*m.options.objfcnval)>1:
                e=e+1
        except:
            Error3=Error3+1
            


plt.plot(No_Tasks3, runningTime3, label="lowest objective leaf")
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
plt.ylabel('Running Time')
plt.xlabel('Number of Tasks')
plt.show()


plt.plot(No_Tasks3, ut_t3,label="lowest objective leaf")
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
plt.ylabel('Utilization factor')
plt.xlabel('Number of Tasks')
plt.show()       

plt.plot(No_Tasks1, runningTime1, label="depth first")

plt.plot(No_Tasks3, runningTime3, label="lowest objective leaf")
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
plt.ylabel('Running Time')
plt.xlabel('Number of Tasks')
plt.show()
plt.plot(No_Tasks1, ut_t1,label="depth first")

plt.plot(No_Tasks3, ut_t3,label="lowest objective leaf")
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
plt.ylabel('Utilization factor')
plt.xlabel('Number of Tasks')
plt.show()
print(No_Tasks3)
print(runningTime3)

print('Total running time=',TR)
print('Error1=',Error1)

print('Error3=',Error3)
print('e',e)
#%%

from sklearn.linear_model import LinearRegression
model = LinearRegression(fit_intercept=True)
x=np.asarray(No_Tasks1)
model.fit(x[:, np.newaxis], np.asarray(runningTime1))

xfit1 = np.linspace(0, 400, 10000)
yfit1 = model.predict(xfit1[:, np.newaxis])


plt.plot(xfit1, yfit1);

model = LinearRegression(fit_intercept=True)
x=np.asarray(No_Tasks3)
model.fit(x[:, np.newaxis], np.asarray(runningTime3))

xfit2 = np.linspace(0, 400, 10000)
yfit2 = model.predict(xfit2[:, np.newaxis])


plt.plot(xfit2, yfit2);
