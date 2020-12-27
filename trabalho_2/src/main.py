import random
import math
import sys
from tabulate import tabulate

class char_chain:
    """
    Class that represents the test chains of characters. 
    Contains attributes such as the source string, size, the generated chain and exact counters.
    """
    def __init__(self,source_string,chain_size):
        self.source_string=source_string
        self.chain_size=chain_size
        self.chain=""
        self.exact_count={}
        for _ in range(chain_size):
            nextChar = random.choice(source_string)
            self.chain += nextChar
            if not nextChar in self.exact_count:
                self.exact_count[nextChar]=0
            self.exact_count[nextChar] = self.exact_count[nextChar]+1

    def __str__(self):
        return self.chain

class prob_counter:
    """
    Class that represents a probabilistic counter's (with fixed chance) application on a certain test chain.
    Contains attributes such as the test chain, the chance, the calculated occurrences, expected occurrences, errors, etc. 
    """
    def __init__(self, char_chain, p):    
        self.char_chain = char_chain
        self.p=p
        self.dict = {}
        self.count()
        self.expected_values = self.get_expected_values()
        self.relative_errors = self.get_relative_error()
        tableHeader = ['Char','Counter Value','Expected Value','Real Value','Absolute Error','Relative Error']
        tableArray=[]
        for i in self.dict:
            row = [i,self.dict[i],self.expected_values[i], self.char_chain.exact_count[i],abs(self.char_chain.exact_count[i]-self.expected_values[i]),self.relative_errors[i]]
            tableArray.append(row)
        self.table = tabulate(tableArray,headers=tableHeader)
        sortedErrors = sorted(self.relative_errors.items(), key=lambda x: x[1], reverse=True)
        self.max_relative_error = sortedErrors[0]
        self.min_relative_error = sortedErrors[-1]
        self.mean_relative_error = sum(self.relative_errors.values())/len(self.relative_errors)
     
    def  count(self):
        for c in self.char_chain.chain:
            if not c in self.dict:
                self.dict[c]=0
            to_add = random.choices([True,False],[self.p,1-self.p])[0]
          
            if to_add:
                self.dict[c] = self.dict[c] + 1
        return self.dict
    
    """
    def get_means(self):
        percentages={}
        for k in self.dict:
            percentages[k] = self.dict[k]/self.char_chain.chain_size
        return percentages
    
    def get_standard_deviation(self):
        means = self.get_means()
        std_dv={}
        for k in means:
            std_dv[k]=math.sqrt(math.pow(self.dict[k]-means[k],2)/self.char_chain.chain_size)
        return std_dv 
    """
            
    def get_expected_values(self):
        e_val = {}
        for k in self.dict:
            e_val[k] = self.dict[k]*(1/self.p)
        return e_val
    

    def get_relative_error(self):
        rel_error={}   
        for k in self.char_chain.exact_count:
            if self.char_chain.exact_count[k]>0:
                rel_error[k]=abs(self.char_chain.exact_count[k]-self.expected_values[k])/self.char_chain.exact_count[k]
            else:
                rel_error[k]=0

        return rel_error

    def __str__(self):
        text = "Fixed probabilistic counter with chance: " + str(self.p*100) + "%\n" +self.table + "\nMax Relative Error: " + str(self.max_relative_error[1]) + "\nMean Relative Error: " + str(self.mean_relative_error) + "\nMin Relative Error: " + str(self.min_relative_error[1]) + "\n"
        return text


class dec_prob_counter:
    """
    Class that represents a logarithmic probabilistic counter's (with decreasing chance) application on a certain test chain.
    Contains attributes such as the test chain, the base, the calculated occurrences, expected occurrences, errors, etc. 
    """
    def __init__(self, char_chain,base):    
        self.char_chain = char_chain
        self.base=base
        self.dict = {}
        self.count()
        self.expected_values = self.get_expected_values()
        self.relative_errors = self.get_relative_error()
        tableHeader = ['Char','Counter Value','Expected Value','Real Value','Absolute Error','Relative Error']
        tableArray=[]
        for i in self.dict:
            row = [i,self.dict[i],self.expected_values[i],self.char_chain.exact_count[i],abs(self.char_chain.exact_count[i]-self.expected_values[i]),self.relative_errors[i] ]
            tableArray.append(row)
        self.table = tabulate(tableArray,headers=tableHeader)
        sortedErrors = sorted(self.relative_errors.items(), key=lambda x: x[1], reverse=True)
        self.max_relative_error = sortedErrors[0]
        self.min_relative_error = sortedErrors[-1]
        self.mean_relative_error = sum(self.relative_errors.values())/len(self.relative_errors)
        
    """ 
    def  count(self):
        for c in self.char_chain.chain:
            if not c in self.dict:
                self.dict[c]=0
            chance = 1/math.pow(self.base,self.dict[c])
            to_add = random.choices([True,False],[chance,1-chance])[0]
          
            if to_add:
                self.dict[c] = self.dict[c] + 1
        return self.dict
     """
    def  count(self):
        for c in self.char_chain.chain:
            if not c in self.dict:
                self.dict[c]=0
            chance = 1/math.pow(self.base,self.dict[c])
            
            to_add = random.choices([True,False],[chance,1-chance])[0]
          
            if to_add:
                self.dict[c] = self.dict[c] + 1
        return self.dict
    

    def get_means(self):
        percentages={}
        for k in self.dict:
            percentages[k] = self.dict[k]/self.char_chain.chain_size
        return percentages
    
    def get_standard_deviation(self):
        means = self.get_means()
        std_dv={}
        for k in means:
            std_dv[k]=math.sqrt(math.pow(self.dict[k]-means[k],2)/self.char_chain.chain_size)
        return std_dv
            
    
    def get_expected_values(self):
        e_val = {}
        for k in self.dict:
            e_val[k] = int((math.pow(self.base,self.dict[k]) - self.base + 1)/(self.base-1))
            
        return e_val
   
    def get_relative_error(self):
        rel_error={}   
        for k in self.char_chain.exact_count:
            if self.char_chain.exact_count[k]>0:
                rel_error[k]=abs(self.char_chain.exact_count[k]-self.expected_values[k])/self.char_chain.exact_count[k]
            else:
                rel_error[k]=0

        return rel_error

    def __str__(self):
        text = "Decreasing chance logarithmic counter with base: " + str(self.base) + "\n" + self.table + "\nMax Relative Error: " + str(self.max_relative_error[1]) + "\nMean Relative Error: " + str(self.mean_relative_error) + "\nMin Relative Error: " + str(self.min_relative_error[1]) + "\n"
        return text




if __name__ == "__main__":


    test_chain = char_chain("rodrigomiguelmaiaferreira",10000)
    fpc=prob_counter(test_chain,0.5)
    dpc=dec_prob_counter(test_chain,math.sqrt(2))
    print(fpc)
    print(dpc)
  