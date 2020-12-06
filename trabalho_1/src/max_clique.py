import math
from itertools import combinations
import time
import random
import matplotlib.pyplot as plt

class graph:
    """
    Class to represent a graph.
    """
    def __init__(self,n_vertices,edges):
        assert(n_vertices>=0),"invalid number of vertices"
        self.n_vertices=n_vertices
        assert (0<=len(edges)<=(n_vertices*(n_vertices-1))/2),"invalid number of edges"
        for i,j in edges:
            assert(i!=j and 1<=i<=n_vertices and 1<=j<=n_vertices),"invalid edge"
        self.edges=edges

    def __str__(self):
        s= str(self.n_vertices) +" nodes\n"
        for i,j in self.edges:
            s+=str(i) + "--" + str(j)+"\n"
        return s


    def add_node(self):
        self.n_vertices=self.n_vertices+1

def random_graph(n: int,e: int)->graph:
    """
    Create a random graph with n vertices and e edges.

    Args:
        n (int): Number of vertices.
        e (int): Number of edges.

    Returns:
        graph: Graph created with n vertices, and e random edges.
    """
    assert (n>=1),"invalid number of vertices"
    assert (0<=e<=(n*(n-1))/2),"invalid number of edges"
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
    return graph(n,edges)


def max_clique(graph: graph)->(list,int,int,float):
    """
    Get the max clique/s for a given graph.
    The main algorithm used for this assignment.

    Args:
        graph (graph): Graph to find max clique from

    Returns:
        list,int,int,float: list of solutions, number of occurrences of the innermost operation, number of configurations generated, executing time.
    """
    
    
    start=time.time()
    n_configurations=0
    n_innermost_inst=0
    max = 0
    sols = {}
    n_vertices=graph.n_vertices
    m_edges=graph.edges
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

def basic_op_increasing_n(beg: int,end: int)->None:
    """
    Plot the number of basic operations executed in max_clique for graphs with various #N (number of nodes).

    Args:
        beg (int): First #N to plot.
        end (int): Last #N to plot.
    """
    assert (0<=beg and 1<=end and beg<end),"invalid beg/end"
    x=[]
    basic_operations=[]
    g=graph(beg,[])
    for n in range(beg,end+1):
        results = list(max_clique(g))
        x.append(n)
        basic_operations.append(results[1])
        g.add_node()

    plt.plot(x,basic_operations)
    plt.xticks(x)
    plt.title("Number of basic operations for input size n")
    plt.xlabel("n")
    plt.ylabel("# basic operations")
    plt.show()
    
def exec_time_increasing_n(beg: int,end: int)->None:
    """
    Plot the executing times of max_clique for graphs with various #N (number of nodes).

    Args:   
        beg (int): First #N to plot.
        end (int): Last #N to plot.
    """
    assert (0<=beg and 1<=end and beg<end),"invalid beg/end"
    x=[]
    times=[]
    g=graph(beg,[])
    for n in range(beg,end+1):
        results = list(max_clique(g))
        x.append(n)
        times.append(results[3])
        g.add_node()

    plt.plot(x,times)
    plt.title("Execution time for input size n")
    plt.xlabel("n")
    plt.xticks(x)
    plt.ylabel("time (s)")
    plt.show()


def sol_config_ratio_increasing_n(beg: int,end: int,sample_size: int)->None:
    """
    Plot the ratios of solutions/configurations created in max_clique for graphs with various #N (number of nodes).

    Args:
        beg (int): First #N to plot.
        end (int): Last #N to plot.
        sample_size (int): Number of random graphs to create on each iteration to get an average of results.
    """
    
    assert (0<=beg and 1<=end and beg<end),"invalid beg/end"
    assert (sample_size>=0),"invalid sample_size"
    x=[]
    sol_config_ratio=[]
    graphs=[]
    max_edges=(beg*(beg-1))/2
    for i in range(sample_size):
        if max_edges>0:
            graphs.append(random_graph(beg,random.randrange(max_edges)))
        else:
            graphs.append(graph(beg,[]))
    for n in range(beg,end+1):
        mean=0
        for i in range(sample_size):
            results = list(max_clique(graphs[i]))
            mean+=len(results[0])/results[2]
            graphs[i].add_node()

        mean=mean/sample_size
        x.append(n)
        sol_config_ratio.append(mean)

    plt.plot(x,sol_config_ratio)
    plt.title("Solutions/Configurations for input size n")
    plt.xlabel("n")
    plt.xticks(x)
    plt.ylabel("%")
    plt.show()



def increasing_m(n: int,beg: int,end: int)->None:
    """
    Comparing the effect adding edges to a graph has on the number of basic operations.

    Args:
        n (int): Number of nodes to use on the test graph.
        beg (int): Number of edges to start plotting from. 
        end (int): Number of edges to end plotting at.
    """
    assert (n>=0),"invalid n"
    max_edges = (n*(n-1))/2
    assert (0<=beg<=max_edges-1 and 1<=end<=max_edges and beg<end),"invalid beg/end"
    for m in range(beg,end+1):
        g=random_graph(n,m)
        results = max_clique(g)
        
        print(results[1])
    

n_rec_calls=0
def rec_maxclique(n_vertices:list,m_edges:list) -> list:
    """
    Example of the max clique problem solved recursively.
    This function was made out of curiosity, it didn't serve any purpose for the report.

    Args:
        n_vertices (list): List of vertices in current subgraph.
        m_edges (list): List of edges.

    Returns:
        list: A max clique.
    """
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


#g=graph(3,[(1,2),(2,3)])
#g = random_graph(10,45)
print(g)
#print(max_clique(g))
#increasing_m(10,1,20)
#basic_op_increasing_n(1,20)
#exec_time_increasing_n(1,20)
#sol_config_ratio_increasing_n(1,15,5)
