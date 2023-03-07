import numpy as np
import matplotlib.pyplot as plt
import math

def Lagrange(x): #evaluate Langrange at x
    y = 0
    for i in range(len(xdata)): #outer loop is Lagrange Approximation at x. sum of (data)*(nth Lagrange)
        dnmr = 1
        nmr = 1
        for j in range(len(ydata)): #inner loop is nth Lagrange Interpolating Polynomial
            if i == j:
                continue
            nmr = nmr*(x - xdata[j])
            dnmr = dnmr*(xdata[i]-xdata[j])
        y = y + (nmr / dnmr)*ydata[i]
    return y

def divDifference(): #coefficients of Polynomial
    DDTable = [ydata]
    for i in range(len(ydata) - 1):
        M = []
        for j in range(len(ydata) - 1 - i):
            nmr = DDTable[i][j+1] - DDTable[i][j]
            dnmr = xdata[j + 1 + i] - xdata[j]
            M.append(nmr/dnmr)
        DDTable.append(M)
    return DDTable
        
def DDPolynomial(x): #evaluate Polynomial at x
    y = DDTable[0][0]
    for i in range(len(ydata) - 1):
        P = 1
        for j in range(i+1):
            P = P * (x - xdata[j])
        y = y+P*DDTable[i+1][0]
    return y

def f(x): # for evaluating function values for generate()
    fx = "math.exp(x) + math.pow(2,-x) + 2*math.cos(x) - 6"
    val = eval(fx)
    return val

def generate(): #for given eq

    global xdata
    global ydata
    global LangrangeTable
    global DDTable
    global PolynomialTable
    global xdata100
    global ErrorTableLangrange
    global ErrorTablePoly

    n = int(input("Please input value of n: "))
    xdata = np.linspace(-2,2,n)
    ydata = []
    LangrangeTable = []
    DDTable = []
    PolynomialTable = []
    xdata100 = np.linspace(-2,2,100)
    ydata100 = [] 
    ErrorTableLangrange = []
    ErrorTablePoly = []

    for x in xdata:
        ydata.append(f(x)) #values of f(x)
    for x in xdata100:
        ydata100.append(f(x)) #values of f(x) with n =100
    for x in xdata100:
        LangrangeTable.append(Lagrange(x)) #values of Lagrange with n=100
    DDTable = divDifference()
    for x in xdata100:
        PolynomialTable.append(DDPolynomial(x)) #values of DD with n=100

    for x in range(len(LangrangeTable)):
        ErrorTableLangrange.append(abs(float(ydata100[x])-LangrangeTable[x])) #Langrange Error for n=100
    for x in range(len(PolynomialTable)):
        ErrorTablePoly.append(abs(float(ydata100[x])-PolynomialTable[x])) #DD Error for n=100
    
    print("X: ", xdata)
    print("Y: ", ydata)
    print("Langrange: ", LangrangeTable)
    print()
    print("DD Polynomial: ", PolynomialTable)
    print()
    print("Langrange Error: ", ErrorTableLangrange)
    print()
    print("Poly Error: ", ErrorTablePoly)
    print()
    print("DD Table: " )
    DDTablePrint()
    plt.subplot(2,1,1)
    plt.plot(xdata, ydata, label = "f(x) n=" + str(len(ydata)), color= 'Red')
    plt.plot(xdata100, LangrangeTable, label="Lagrange n=" + str(len(xdata100)), color='Green')
    plt.plot(xdata100, PolynomialTable, label="Divided Difference n=" + str(len(xdata100)), color='Blue')
    plt.title("Given EQ")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.legend()
    plt.subplot(2,1,2)
    plt.plot(xdata100, ErrorTableLangrange, label="Lagrange n=" + str(len(xdata100)), color='Green')
    plt.plot(xdata100, ErrorTablePoly, label="Divided Difference n=" + str(len(xdata100)), color='Blue')
    plt.xlabel("x")
    plt.ylabel("y")
    plt.legend()
    plt.tight_layout()
    plt.savefig('eq.png')
    plt.show()

def ExampleQs(): #for q19
    
    global xdata
    global ydata
    global LangrangeTable

    global xdatan

    xdata = [0,6,10,13,17,20,28]
    ydata = [6.67,17.33,42.67,37.33,30.10,29.31,28.74]
    LangrangeTable = []
    xdatan = np.linspace(0,28,28)

    for x in xdatan:
        LangrangeTable.append(Lagrange(x)) #values of Lagrange with n=28
    
    print("SAMPLE 1")
    print("X: ", xdata)
    print("Y: ", ydata)
    print("Langrange: ", LangrangeTable)
    print()
    print("Maximum Interpolated Weight: ", max(LangrangeTable))
    print()

    plt.clf()
    plt.plot(xdata, ydata, label = "f(x) n=" + str(len(ydata)), color= 'Red')
    plt.plot(xdatan, LangrangeTable, label="Lagrange n=" + str(len(xdatan)), color='Green')
    plt.title("SAMPLE 1")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.legend()
    plt.savefig("SAMPLE 1")
    plt.show()

    ydata = [6.67,16.11,18.89,15.00,10.56,9.44,8.89]
    LangrangeTable = []

    for x in xdatan:
        LangrangeTable.append(Lagrange(x)) #values of Lagrange with n=28

    print("SAMPLE 2")
    print("X: ", xdata)
    print("Y: ", ydata)
    print("Langrange: ", LangrangeTable)
    print()
    print("Maximum Interpolated Weight: ", max(LangrangeTable))
    print()

    plt.clf()
    plt.plot(xdata, ydata, label = "f(x) n=" + str(len(ydata)), color= 'Red')
    plt.plot(xdatan, LangrangeTable, label="Lagrange n=" + str(len(xdatan)), color='Green')
    plt.title("SAMPLE 2")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.legend()
    plt.savefig("SAMPLE 2")
    plt.show()

def interpolate(): #for general interpolation given n-data

    global xdata
    global ydata
    global LangrangeTable
    global DDTable
    global PolynomialTable
    global xdatan

    print("Enter x values in the format: x x x x x ...")
    data = input().split()
    xdata = list(map(float, data))

    print("Enter y values in the format: y y y y y ... ")
    data = input().split()
    ydata = list(map(float, data))

    LangrangeTable = []
    DDTable = []
    PolynomialTable = []
    n = int(input("Enter linspace size: "))
    xdatan = np.linspace(min(xdata),max(xdata),n)

    for x in xdatan:
        LangrangeTable.append(Lagrange(x)) #values of Lagrange with n=28
    DDTable = divDifference()
    for x in xdatan:
        PolynomialTable.append(DDPolynomial(x)) #values of DD with n=28
    
    print("Data:")
    print("X: ", xdata)
    print("Y: ", ydata)
    print("Langrange: ", LangrangeTable)
    print()
    print("DD Polynomial: ", PolynomialTable)
    print()
    print("DD Table: " )
    DDTablePrint()
    plotmygraph("data interpolation")

def plotmygraph(graphTitle): #general Plot

    plt.clf()
    plt.plot(xdata, ydata, label = "f(x) n=" + str(len(ydata)), color= 'Red')
    plt.plot(xdatan, LangrangeTable, label="Lagrange n=" + str(len(xdatan)), color='Green')
    plt.plot(xdatan, PolynomialTable, label="Divided Difference n=" + str(len(xdatan)), color='Blue')
    plt.title(graphTitle)
    plt.xlabel("x")
    plt.ylabel("y")
    plt.legend()
    plt.savefig(graphTitle)
    plt.show()

def DDTablePrint(): #triangle DD print
    PrintTable = []
    max_num_length = 0;

    #whitespace between DD
    max_size = len(DDTable[0])
    for Diff in DDTable:
        
        size = max_size - len(Diff)
        newArr = []
        for num in Diff:
            num = '{:.4e}'.format(num) # 4sf to make cleaner table
            newArr.append(num)
            newArr.append(" ")
            max_num_length = max(max_num_length, len(str(num)))
            
        #whitespace before and after DD to center them
        newArr = [" "]*size + newArr + [" "]*(size-1)
        PrintTable.append(newArr)
        
    PrintTable[0].pop() #pop free space in first array

    #transposing the matrix
    PrintTable = np.transpose(PrintTable)

    for arr in PrintTable:
        for num in arr:
            print(num, end=" " *((max_num_length + 1) - len(num)))
        print("",end="\n")

def main():
    decision = (input("Interpolate given eq OR Interpolate q19 OR Interpolate using data? enter (eq/q19/data): "))
    if decision == "eq":
        generate()
        return
    elif decision == "q19":
        ExampleQs()
        return
    elif decision == "data":
        interpolate()
        return
    
if __name__ == "__main__":
    main()