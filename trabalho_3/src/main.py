from random import choice
from math import floor, ceil
from tabulate import tabulate



class char_chain:
    """
    Class that represents the test chains of characters. 
    Contains attributes such as the source string, size, the generated chain and exact counters.
    """
    def __init__(self,source_string,chain_size, path):
        self.source_string=source_string
        self.chain_size=chain_size
        self.exact_count={}
        with open(path, "w", encoding="utf-8") as f:
            for _ in range(chain_size):
                nextChar = choice(source_string)
                f.write(nextChar + " ")
                if not nextChar in self.exact_count:
                    self.exact_count[nextChar]=0
                self.exact_count[nextChar] = self.exact_count[nextChar]+1
        self.order = sorted(self.exact_count.items(), key=lambda x: x[1], reverse=True)
        self.ranks = self.get_ranks()

    def get_ranks(self):
        ranks = {}
        n=1
        for i in self.order:
            ranks[i[0]] = n
            n+=1
        return ranks

    def __str__(self):
        
        header=["Symbol","Exact Ocurrences", "Exact Frequency", "Rank"]
        i=1
        table=[]
        for c,occ in self.order:
            row=[c,occ,str(100*occ/self.chain_size) + "%",i]
            table.append(row)
            i+=1
        return tabulate(table,headers=header)




class lossycounting_shareddelta:
    def __init__(self,s,epsilon,path):
    
        self.epsilon = epsilon
        self.k=ceil(1/self.epsilon)
        self.s=s
        self.path = path
        self.delta = 0
        self.n = 0
        self.t = {}
        self.__read()
       # self.__results()
    def __read(self):
        with open(self.path, "r", encoding="utf-8") as f:
            while True:
                i = f.read(2)
                if not i:
                    break
                self.n+=1
                i = i[0]
                if i in self.t:
                    self.t[i] = self.t[i] + 1
                else:
                    self.t[i] = 1 + self.delta
                
                possible_delta = floor(self.n/self.k)
                #print("iteration ",self.n, " possible delta: ", possible_delta, "actual delta ",self.delta)
                #print(self.t)
                if possible_delta != self.delta:
                    #print("cleaned")
                    self.delta = possible_delta
                    keys = list(self.t.keys())
                    for j in keys:
                        if self.t[j] <self.delta:
                            #print("removed " ,j)
                            self.t.pop(j)


    def __str__(self):
        header = ["Symbol","Estimated Rank", "Estimated Frequency", "Smallest Possible Frequency"]
        table=[]
        i=1
        sorted_keys = sorted(self.t, key=self.t.get,reverse=True)
        
        for item in sorted_keys:
            if self.t[item]>=(self.s - self.epsilon)*self.n:
                #print(str(item) + " " + str(self.t[item][0]) +" with max error: " + str(self.epsilon * self.n) )
                smallest = self.t[item]-self.epsilon * self.n
                if smallest<0:
                    smallest=0
                table.append([item,str(i),str(100*self.t[item]/self.n) + "%",str(100*smallest/self.n) + "%"])
                i+=1
                #table.append([item,str(self.t[item]),str(self.t[item]-self.epsilon * self.n)])
        return tabulate(table,headers=header)

    """
    def __results(self):

        for item in self.t:
            if self.t[item] >= (self.s-self.epsilon)*self.n:
                print(str(item) + " " + str(self.t[item]) +" with max error: " + str(self.epsilon * self.n) )

    """

class lossycounting_individualdelta:
    def __init__(self,s,epsilon,path):
        self.epsilon = epsilon
        self.k=ceil(1/epsilon)
        self.s=s
        self.path = path
        self.delta = {}
        self.n = 0
        self.t = {}
        self.__read()
        #self.__results()
    def __read(self):
        with open(self.path, "r", encoding="utf-8") as f:
            current_bucket=1
            while True:
                i = f.read(2)
                if not i:
                    break
                self.n+=1
                i = i[0]
                if i in self.t:
                    self.t[i] = self.t[i] + 1
                else:
                    self.t[i] = 1
                    self.delta[i]= current_bucket-1
                
                
                
                #print(self.t)
                if self.n%self.k==0:
                    #print("cleaned")
                    #self.delta = possible_delta
                    keys = list(self.t.keys())
                    for j in keys:
                        if self.t[j] + self.delta[j] <=current_bucket:
                            #print("removed " ,j)
                            self.t.pop(j)
                            self.delta.pop(j)
                    current_bucket+=1
    
    def __str__(self):
        header = ["Symbol", "Estimated Rank","Estimated Frequency", "Smallest Possible Frequency"]
        table=[]
        i=1
        sorted_keys = sorted(self.t, key=self.t.get,reverse=True)
        
        for item in sorted_keys:
            if self.t[item]>=(self.s - self.epsilon)*self.n:
                #print(str(item) + " " + str(self.t[item][0]) +" with max error: " + str(self.epsilon * self.n) )
                smallest = self.t[item]-self.epsilon * self.n
                if smallest<0:
                    smallest=0
                table.append([item,str(i),str(100*self.t[item]/self.n) + "%",str(100*smallest/self.n) + "%"])
                i+=1
        return tabulate(table,headers=header)

if __name__=="__main__":
    #t=char_chain("rodrigomiguelmaiaferreirarrrrrrrrrroooooo",100000,"../text_files/test.txt")
    t=char_chain("abbcdd",100000,"../text_files/test.txt")
    print(t)
    l=lossycounting_individualdelta(0.2,0.01,"../text_files/test.txt")
    print("individual_delta\n",l)
    l2=lossycounting_shareddelta(0.2,0.01,"../text_files/test.txt")
    print("shared_delta\n" , l2)