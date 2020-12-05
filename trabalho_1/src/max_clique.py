import math
from itertools import combinations
import time
import random
import matplotlib.pyplot as plt

def rec_maxclique(n_vertices:list,m_edges:list) -> list:
    global n_rec_calls
    if not n_vertices:
        return []
    for i in n_vertices:
        for j in n_vertices:
            if i!=j and not (i,j) in m_edges and not (j,i) in m_edges:
                values = []
                for k in n_vertices:
                    values.append(rec_maxclique(list(set(n_vertices) - set([k])),m_edges))
                    n_rec_calls+=1   
                return max(values,key=len)
    return n_vertices            

def random_graph(n,e):
    #assert number of edges not over max possible
    nodes = range(1,n+1)
    edges=[]
    while len(edges)<e:
        i = random.randrange(1,len(nodes)+1)
        j=random.randrange(1,len(nodes)+1)
        while i==j:
            j=random.randrange(1,len(nodes)+1)
        if (i,j) in edges or (j,i) in edges:
            continue
        else:
            edges.append((i,j))
    return n,edges

def compcalc(n):
    total=0
    for i in range(2,n+1):
        c =(math.factorial(n)/(math.factorial(n-i)*math.factorial(i)))
        total+=c*(math.factorial(i)/(math.factorial(i-2)*math.factorial(2)))
    return total


def max_clique(n_vertices: int,m_edges: list)->list:
    start=time.time()
    n_configurations=0
    n_innermost_inst=0
    max = 0
    sols = {}
    for i in range(1,n_vertices+1):
        comb = list(combinations(range(1,n_vertices+1),i))
        sols[i]=[]
        for c in comb:
            c=list(c)
            n_configurations+=1
            flag=True
            for a in range(len(c)):
                
                for j in range(1,len(c)-a):
                    n_innermost_inst+=1
                    if  not ((c[a],c[a+j]) in m_edges or (c[a+j],c[a]) in m_edges): #flag and
                        flag=False
            
            if flag and len(c)>=max:
                max=len(c)
                sols[i].append(c)
    end = time.time()
    return sols[max],n_innermost_inst,n_configurations,end-start


def basic_op_increasing_n(beg,end):
    x=[]
    basic_operations=[]
    for n in range(beg,end+1):
        graph=(n,[])
        results = list(max_clique(*graph))
        x.append(n)
        basic_operations.append(results[1])

    plt.plot(x,basic_operations)
    plt.xticks(x)
    plt.title("Number of basic operations for input size n")
    plt.xlabel("n")
    plt.ylabel("# basic operations")
    plt.show()
    
def exec_time_increasing_n(beg,end):
    x=[]
    times=[]
    for n in range(beg,end+1):
        graph=(n,[])
        results = list(max_clique(*graph))
        x.append(n)
        times.append(results[3])

    plt.plot(x,times)
    plt.title("Execution time for input size n")
    plt.xlabel("n")
    plt.xticks(x)
    plt.ylabel("time (s)")
    plt.show()

def sol_config_ratio_increasing_n(beg,end):
    x=[]
    sol_config_ratio=[]
    for n in range(beg,end+1):
        graph=(n,[])
        results = list(max_clique(*graph))
        x.append(n)
        sol_config_ratio.append(len(results[0])/results[2])

    plt.plot(x,sol_config_ratio)
    plt.title("Solutions/Configurations for input size n")
    plt.xlabel("n")
    plt.xticks(x)
    plt.ylabel("%")
    plt.show()

def increasing_m(n,beg,end):
    print(compcalc(n))
    for m in range(beg,end+1):
        graph=random_graph(n,m)
        results = max_clique(*graph)
        print(graph)
        print(results)
        print()

#basic_op_increasing_n(1,20)
#exec_time_increasing_n(1,20)
sol_config_ratio_increasing_n(1,20)
#increasing_m(5,0,10)