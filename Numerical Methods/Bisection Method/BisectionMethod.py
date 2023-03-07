import math

def f(x):
    val = float(eval(eq)) #eval(fx) returns expression (that is, our function f) in terms of x. x is parameter, so x becomes the input for f. 
    return val


def root(a,b): #testing for Intermediate Value Theorem
    if(f(a)>0 and f(b)<0): 
        return True
    elif(f(a)<0 and f(b)>0):
        return True
    else:
        return False
    
    
def bisection_method(a, b, tolerance):
    if(root(a,b) == False):
        print('Root does not exist in interval',f'[{a},{b}]')
        return
    mid_list = [0,0] #mid of interval
    f_list = [0,0] #f of mid of interval
    Interval_list = [[0,0],[0,0]]
    i = 1
    mid = (a+b)/2
    f_mid = f(mid) #Pn
    mid_list[i] = mid
    f_list[i] = f_mid
    Interval_list[i] = [a,b]

    if (f_mid != 0): #condition for when root is found on 1st iteration
        if(f_mid >0):
            b = mid
            Interval_list.append([a,b])
        elif(f_mid <0):
            a = mid
            Interval_list.append([a,b])
        mid = (a+b)/2
        i+=1
        f_mid = f(mid) #Pn-1
            
        mid_list.append(mid)
        f_list.append(f_mid)

        while((abs(f_mid-f_list[i-1])/abs(f_mid)>tolerance) and (abs(f_mid)>tolerance)):  #Testing for Relative Error AND Bounds
            ##print(abs(f_mid-f_list[i-1])/abs(f_mid))
            if(f_mid >0):
                b = mid
                Interval_list.append([a,b])
            elif(f_mid <0):
                a = mid
                Interval_list.append([a,b])
            
            mid = (a+b)/2
            i+=1
            f_mid = f(mid)

            mid_list.append(mid)
            f_list.append(f_mid)

            if(f_mid == 0):
                break
                
            
        
    print('Root of the function:',mid)
    print('Number of iterations:',i)
    order = asym_ord_of_conv(mid_list)
    file_write(i,mid_list,f_list, mid, order, Interval_list)
#asymtotic and rate of convergence
def asym_ord_of_conv(mid_list):
    order = []
    for i in range(len(mid_list) - 2):
        order.append(abs(mid_list[i+2] - mid_list[i+1]) / abs(mid_list[i+1] - mid_list[i]))
    print('Asymtotic order of convergence: ', order[-1])
    if(math.floor(order[-1] / order[-2]) == 1):
        print("Linear order of convergence")
    return order
    
def file_write(i,list1,list2, mid, order, Interval_List):
    file = open('DATA.txt','w')
    file.write(f'{eq}\n')
    file.write("{:<5}{:<30}{:<30}{:<30}{:<15}".format('i','a','b','m','f(m)'))
    file.write('\n')
    for k in range(1,i):
        file.write("{:<5}{:<30}{:<30}{:<30}{:<15}\n".format(k,Interval_List[k][0],Interval_List[k][1],list1[k],list2[k]))
    
    file.write('Root of the function: {} \n'.format(mid))
    file.write('Number of iterations: {} \n'.format(i))
    file.write('Asymtotic order of convergence: {}\n'.format( order[-1]))
    file.write('order \n')
    for index in range(len(order) -1):
        file.write("{} \n".format(order[index]))
    file.write("Order of convergence is linear for bisection as asymptotic revolves around 0.5.")
    file.close()
    
    
def main():
    global eq
    eq = str(input("Enter function in terms of x: "))
    a = (eval(input("Enter interval a: ")))
    b = (eval(input("Enter interval b: ")))
    tol = float(input("Enter tolerance: "))
    bisection_method(a,b,tol)

if __name__ == "__main__":
    main()