import math
from itertools import combinations,permutations
import time
import random
import matplotlib.pyplot as plt

n_comparisons=0
n_configurations=0
n_rec_calls=0


def iter_maxclique(n_vertices_list:list,m_edges:list)->list:
    global n_comparisons,n_configurations
    n_vertices=len(n_vertices_list)
    max =0
    sols = {}
    for i in range(1,n_vertices+1):
        comb = combinations(range(1,n_vertices+1),i)
        #comb = permutations(range(1,n_vertices+1),i)
        sols[i]=[]
        for c in comb:
            n_configurations+=1
            flag=True
            c=list(c)
            for a in range(len(c)):
                
                for j in range(1,len(c)-a):
                    n_comparisons+=1
                    if  not ((c[a],c[a+j]) in m_edges or (c[a+j],c[a]) in m_edges): #flag and
                        flag=False
                
            if flag and len(c)>=max:
                max=len(c)
                sols[i].append(c)
    return sols[max]

def final_maxclique(n_vertices: int,m_edges: list)->list:
    global n_configurations, n_comparisons
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
                    n_comparisons+=1
                    if  not ((c[a],c[a+j]) in m_edges or (c[a+j],c[a]) in m_edges): #flag and
                        flag=False
            
            if flag and len(c)>=max:
                max=len(c)
                sols[i].append(c)

    return sols[max]


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

#edg=[(1,2),(1,5),(2,4),(2,6),(3,4),(3,6),(4,5),(4,6),(5,6)]
edgtest=[(1,2),(1,3),(1,7),(2,3),(2,7),(3,4),(3,5),(3,6),(4,5),(4,6),(5,6),(6,7)]
#print(final_maxclique(7,edgtest))
def compcalc(n):
    total=0
    for i in range(2,n+1):
        c =(math.factorial(n)/(math.factorial(n-i)*math.factorial(i)))
        total+=c*(math.factorial(i)/(math.factorial(i-2)*math.factorial(2)))
    return total


def max_clique(n_vertices: int,m_edges: list)->list:
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
                
    return sols[max],n_innermost_inst,n_configurations


def increasing_n(beg,end):
    for n in range(beg,end+1):
        graph = random_graph(n,2)
        results = maxclique(*graph)
        print(results)

def increasing_m(n,beg,end):
    print(compcalc(n))
    for m in range(beg,end+1):
        graph=random_graph(n,m)
        results = maxclique(*graph)
        print(graph)
        print(results)
        print()
"""
for i in range(1,10):
    n_comparisons=0
    n_configurations=0
    vert=[1,2,3,4,5,6]
    edg=[(1,2),(1,5),(2,4),(2,6),(3,4),(3,6),(4,5),(4,6),(5,6)]
    edg2=list(combinations(range(1,6),2))
    #n = int(input("n_vertices:\n"))
    #print("iterative")
    start=time.time()
    #x =iter_maxclique(vert,edg)
    x =final_maxclique(i,edgtest)
    end=time.time()
    print(x)  
    print(end-start, "seconds")
    print("vertices:",i,"\nedges:",len(edgtest))
    print("iterative comparisons:",n_comparisons)
    print("iterative configurations:",n_configurations)
    print(len(x)/n_configurations,"solutions/configurations")
    print("formula",compcalc(i))
"""
"""
print("\n\nrecursive")
start=time.time()
print(rec_maxclique(vert,edg))
print(time.time()-start,"seconds")
print(n_rec_calls, "recursive calls")
"""

"""
graph=random_graph(6,10)
print(graph)
print(maxclique(*graph))
"""
#increasing_n(3,15)
increasing_m(5,0,10)