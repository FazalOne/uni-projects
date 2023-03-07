import math
import numpy as np
import sympy as sm
from tabulate import *

def f(x):
    f = sm.simplify(fx).subs({"x":x})
    return sm.N(f)

def integral(eq,x,a,b): #for evaluating integral with limits
    x=sm.symbols(x)
    return sm.N(sm.integrate(eq,(x, a, b)))

def g(eq,x,a, i): # for evaluating ith derivative
    x=sm.symbols(x)
    gx = sm.diff(eq, x, i)
    g = sm.simplify(gx).subs({"x":a})
    return sm.N(g)

def Trapezoidal(start, end, n):
    S = 0 
    h = (end - start ) /n
    x = np.linspace(start,end, n+1)
    y = []
    for i in range(len(x)):
        y.append(f(x[i]))
    for i in range(n-1):
        S = S +2*y[i+1]
    S = (h/2)*(S+y[0]+y[n])
    return S

def approxErrorTrapezoidal(h, eq, x):
    D2 = []
    for i in range(len(x)):
        D2.append(g(eq, "x", x[i], 2))
    return abs(h**3*max(D2) / 12)

def approxErrorSimpson(h, eq, x):
    D4 = []
    for i in range(len(x)):
        D4.append(g(eq, "x", x[i], 4))
    return abs((3/80)*(h**5)*max(D4))
    
def q22():
    print("Q22")
    print("We are not provided with any equation, rather data points are given.")
    x = [0, 6, 12, 18, 24, 30, 36, 42, 48, 54, 60, 66, 72, 78, 84] # time (independent)
    y = [124, 134, 148, 156, 147, 133, 121, 109, 99, 85, 78, 89, 104, 116, 123] # speed (dependent)
    h = 6
    n = len(x) - 1
    # our functions were generic for data based on equations so we extracted the logic and tried it below
    t_Sum = 0
    for i in range(n-1):
        t_Sum = t_Sum +2*y[i+1]
    dist = (h/2)*(t_Sum+y[0]+y[n])
    print("Distance using Trapezium rule: ", dist)
    
    S1 = 0
    S2 = 0
    for i in range(int(n/2)):
        S1 = S1 + 4*y[2*i + 1]
        if i == (n/2) - 1:
            break
        S2 = S2+2*y[2*i + 2]
    dist2 = h * (y[0]+S1+S2+y[n]) / 3
    print("Distance using Simpsons rule: ", dist2)
    
def Simpsons(start, end, n):
    S1 = 0
    S2 = 0
    h = (end - start ) /n
    x = np.linspace(start,end, n+1)
    y = []
    for i in range(len(x)):
        y.append(f(x[i]))
    for i in range(int(n/2)):
        S1 = S1 + 4*y[2*i + 1]
        if i == (n/2) - 1:
            break
        S2 = S2+2*y[2*i + 2]
    return h * (y[0]+S1+S2+y[n]) / 3
    
def given5n():
    global fx
    dec = str(input("The equation to integrate is sin(x^2): (y/N)"))
    if (dec == "y"):
        fx = "sin(x^2)"
    else:
        fx = str(input("Please input f(x) in format accepted by sympy package: "))
    start = int(input("Enter interval start: "))
    end = int(input("Enter interval end: "))
    ndata = input("Enter values of n in the format 'n n n n n' :").split()
    print()
    Method = ["Method / Error"]
    for item in ndata:
        Method.append("n=" +str(item))
    ResultsTable = [Method,["Trapezoidal"],["Simpsons"],["Trapezoidal Approx Error"],["Simpsons Approx Error"]]
    ndata = list(map(int, ndata))
    for n in ndata:
        h = (end - start) / n
        x = np.linspace(start, end, n)
        ResultsTable[1].append(Trapezoidal(start, end, n))
        ResultsTable[2].append(Simpsons(start, end, n))
        ResultsTable[3].append(approxErrorTrapezoidal(h, fx, x))
        ResultsTable[4].append(approxErrorSimpson(h, fx, x))
        
    Table = tabulate(ResultsTable, headers='firstrow')
    print(Table)
    print("\'True\' value of integral: ", integral(fx,"x",start,end))

def exact():
    global fx
    print("The equation to integrate is √(x + 1)")
    fx = "(x+1)^(1/2)"
    start = 0.0
    end = 0.1
    print("Interval start: ",start)
    print("Interval end: ", end)
    ndata = input("Enter values of n or different in the format 'n n n n n' :").split()
    print()
    Method = ["Methods / Errors"]
    for item in ndata:
        Method.append("n=" +str(item))
    ResultsTable = [Method,["Trapezoidal"],["Simpsons"],["Trapezoidal True Error"],["Simpsons True Error"],["Trapezoidal Approx Error"],["Simpsons Approx Error"] ]
    ndata = list(map(int, ndata))
    truth = integral(fx,"x",start,end)
    for n in ndata:
        t = Trapezoidal(start, end, n)
        s = Simpsons(start, end, n)
        h = (end - start) / n
        x = np.linspace(start, end, n)
        ResultsTable[1].append(t)
        ResultsTable[2].append(s)
        ResultsTable[3].append(abs(truth-t))
        ResultsTable[4].append(abs(truth-s))
        ResultsTable[5].append(approxErrorTrapezoidal(h, fx, x))
        ResultsTable[6].append(approxErrorSimpson(h, fx, x))

    Table = tabulate(ResultsTable, headers='firstrow')
    print(Table)
    print("True value of integral: ", truth)

def main():
    decision = (input("Perform integral of sin(x^2)? OR compare exact value of integral? OR q22? enter (sin/exact/q22): "))
    if decision == "sin":
        given5n()
        return
    elif decision == "exact":
        exact()
        return
    elif decision == "q22":
        q22()
        return
    else:
        print("Choose a valid option next time")
        
    
if __name__ == "__main__":
    main()
    