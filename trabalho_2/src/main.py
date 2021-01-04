import random
import math
import sys
from tabulate import tabulate

FPC=0
LDPC=1

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
        text="Exact occurrences of the chain:\n"
        for c,occ in self.order:
            text+=c + ": " + str(occ) + "\n"
        return text

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
        stats = self.get_stats()
        self.absolute_errors = stats[0] 
        self.relative_errors = stats[1]
        self.accuracy_ratios = stats[2]
        tableHeader = ['Char','Counter Value','Expected Value','Real Value','Expected Rank','Real Rank','Accuracy Ratio','Absolute Error','Relative Error']
        tableArray=[]
        self.order = sorted(self.dict.items(), key=lambda x: x[1], reverse=True)
        n=1
        for i,_ in self.order:            
            row = [i,self.dict[i],self.expected_values[i],self.char_chain.exact_count[i],n,self.char_chain.ranks[i],str(self.accuracy_ratios[i]*100) + "%",self.absolute_errors[i],str(self.relative_errors[i]*100) + "%" ]
            tableArray.append(row)
            n+=1
        self.table = tabulate(tableArray,headers=tableHeader)
        #sortedAbsErrors = sorted(self.absolute_errors.items(), key=lambda x: x[1], reverse=True)
        #self.max_absolute_error = sortedAbsErrors[0]
        #self.min_absolute_error = sortedAbsErrors[-1]
        #self.mean_absolute_error = sum(self.absolute_errors.values())/len(self.absolute_errors)
        #sortedRelErrors = sorted(self.relative_errors.items(), key=lambda x: x[1], reverse=True)
        #self.max_relative_error = sortedRelErrors[0]
        #self.min_relative_error = sortedRelErrors[-1]
        #self.mean_relative_error = sum(self.relative_errors.values())/len(self.relative_errors)
        #self.mean_accuracy_ratio = sum(self.accuracy_ratios.values())/len(self.accuracy_ratios)
        
     
    def  count(self):
        for c in self.char_chain.chain:
            if not c in self.dict:
                self.dict[c]=0
            to_add = random.choices([True,False],[self.p,1-self.p])[0]
          
            if to_add:
                self.dict[c] = self.dict[c] + 1
        return self.dict
    
   
            
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

    def get_stats(self):
        absolute_errors={}
        relative_errors={}
        accuracy_ratios={}
        for k in self.char_chain.exact_count:
            if self.char_chain.exact_count[k]>0:
                relative_errors[k]=abs(self.char_chain.exact_count[k]-self.expected_values[k])/self.char_chain.exact_count[k]
                absolute_errors[k]=abs(self.char_chain.exact_count[k]-self.expected_values[k])
                accuracy_ratios[k]=self.expected_values[k]/self.char_chain.exact_count[k]
            else:
                relative_errors[k]=0
                absolute_errors[k]=0
                accuracy_ratios[k]=0
        return absolute_errors,relative_errors,accuracy_ratios


    def __str__(self):
        text = "Fixed probabilistic counter with chance: " + str(self.p*100) + "%\n" +self.table # + "\nMax Absolute Error: " + str(self.max_absolute_error[1]) + "\nMean Absolute Error: " + str(self.mean_absolute_error) + "\nMin Absolute Error: " + str(self.min_absolute_error[1]) +"\nMax Relative Error: " + str(self.max_relative_error[1]*100) + "%\nMean Relative Error: " + str(self.mean_relative_error*100) +"%\nMin Relative Error: " + str(self.min_relative_error[1]*100) + "%\nMean Accuracy Ratio: " + str(self.mean_accuracy_ratio*100) + "%\n" 
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
        #self.chances={}
        self.count()
        self.expected_values = self.get_expected_values()
        stats = self.get_stats()
        self.absolute_errors = stats[0] 
        self.relative_errors = stats[1]
        self.accuracy_ratios = stats[2]
        tableHeader = ['Char','Counter Value','Expected Value','Real Value','Expected Rank','Real Rank','Accuracy Ratio','Absolute Error','Relative Error']
        tableArray=[]
        self.order = sorted(self.dict.items(), key=lambda x: x[1], reverse=True)
        n=1
        for i,_ in self.order:            
            row = [i,self.dict[i],self.expected_values[i],self.char_chain.exact_count[i],n,self.char_chain.ranks[i],str(self.accuracy_ratios[i]*100) + "%",self.absolute_errors[i],str(self.relative_errors[i]*100) + "%" ]
            tableArray.append(row)
            n+=1
        self.table = tabulate(tableArray,headers=tableHeader)
        #sortedAbsErrors = sorted(self.absolute_errors.items(), key=lambda x: x[1], reverse=True)
        #self.max_absolute_error = sortedAbsErrors[0]
        #self.min_absolute_error = sortedAbsErrors[-1]
        #self.mean_absolute_error = sum(self.absolute_errors.values())/len(self.absolute_errors)
        #sortedRelErrors = sorted(self.relative_errors.items(), key=lambda x: x[1], reverse=True)
        #self.max_relative_error = sortedRelErrors[0]
        #self.min_relative_error = sortedRelErrors[-1]
        #self.mean_relative_error = sum(self.relative_errors.values())/len(self.relative_errors)
        #self.mean_accuracy_ratio = sum(self.accuracy_ratios.values())/len(self.accuracy_ratios)
        
       
   
    def  count(self):
        chances={}
        for c in self.char_chain.chain:
            if not c in self.dict:
                self.dict[c]=0
            if not self.dict[c] in chances:
                chances[self.dict[c]]= 1/math.pow(self.base,self.dict[c])
    
            to_add = random.choices([True,False],[chances[self.dict[c]],1-chances[self.dict[c]]])[0]
            if to_add:
                self.dict[c] = self.dict[c] + 1
        return self.dict
    
     
    def get_stats(self):
        absolute_errors={}
        relative_errors={}
        accuracy_ratios={}
        for k in self.char_chain.exact_count:
            if self.char_chain.exact_count[k]>0:
                relative_errors[k]=abs(self.char_chain.exact_count[k]-self.expected_values[k])/self.char_chain.exact_count[k]
                absolute_errors[k]=abs(self.char_chain.exact_count[k]-self.expected_values[k])
                accuracy_ratios[k]=self.expected_values[k]/self.char_chain.exact_count[k]
            else:
                relative_errors[k]=0
                absolute_errors[k]=0
                accuracy_ratios[k]=0
        return absolute_errors,relative_errors,accuracy_ratios

    def get_expected_values(self):
        e_val = {}
        for k in self.dict:
            e_val[k] = round((math.pow(self.base,self.dict[k]) - self.base + 1)/(self.base-1))
            
        return e_val
    
    def get_absolute_error(self):
        abs_error={}   
        for k in self.char_chain.exact_count:
            if self.char_chain.exact_count[k]>0:
                abs_error[k]=abs(self.char_chain.exact_count[k]-self.expected_values[k])
            else:
                abs_error[k]=0

        return abs_error

    def get_relative_error(self):
        rel_error={}   
        for k in self.char_chain.exact_count:
            if self.char_chain.exact_count[k]>0:
                rel_error[k]=abs(self.char_chain.exact_count[k]-self.expected_values[k])/self.char_chain.exact_count[k]
            else:
                rel_error[k]=0

        return rel_error

    def get_accuracy_ratio(self):
        acc_ratio={}   
        for k in self.char_chain.exact_count:
            if self.char_chain.exact_count[k]>0:
                acc_ratio[k]=self.expected_values[k]/self.char_chain.exact_count[k]
            else:
                acc_ratio[k]=0

        return acc_ratio


    def __str__(self):
        text = "Logarithmic decreasing probability counter with base: " + str(self.base) + "\n"# + self.table + "\nMax Absolute Error: " + str(self.max_absolute_error[1]) + "\nMean Absolute Error: " + str(self.mean_absolute_error) + "\nMin Absolute Error: " + str(self.min_absolute_error[1]) + "\nMax Relative Error: " + str(self.max_relative_error[1]*100) + "%\nMean Relative Error: " + str(self.mean_relative_error*100) + "%\nMin Relative Error: " + str(self.min_relative_error[1]*100) + "%\n" + "Mean Accuracy Ratio: " + str(self.mean_accuracy_ratio*100) + "%\n"
        return text


def simulate(path,test_chain,n_simulations,counter_type,aux):
    with open("../testdata/" + path + "sims.txt","w",encoding="utf-8") as f:
        
        all_rel_error={}
        all_acc_ratio={}
        all_abs_error={}
        all_ranks={}
        all_counters={}
        
        if counter_type==FPC:          
            f.write("simulating fixed probability counter with p=" + str(aux) + " " + str(n_simulations)  + " times" +" for test chain of size " + str(test_chain.chain_size)+"\n" )
        elif counter_type==LDPC:
            f.write("simulating logarithmic decreasing probability counter with base=" + str(aux) + " " + str(n_simulations)  + " times"+" for test chain of size " + str(test_chain.chain_size)+"\n" )
        f.write(test_chain.__str__() + "\n")

        for i in range(n_simulations):
            if counter_type==FPC:
                counter = prob_counter(test_chain,aux)
            elif counter_type==LDPC:
                counter = dec_prob_counter(test_chain,aux)
            n=1
            for c,cval in counter.order:
                
                #mean_values[c]=mean_values.get(c,0)+counter.expected_values[c]
                if not c in all_counters:
                    all_counters[c]=[]
                    all_abs_error[c]=[]
                    all_rel_error[c]=[]
                    all_acc_ratio[c]=[]
                    all_ranks[c]=[]
                all_counters[c].append(cval)                        
                all_acc_ratio[c].append(counter.accuracy_ratios[c]*100)
                all_abs_error[c].append(counter.absolute_errors[c])
                all_rel_error[c].append(counter.relative_errors[c]*100)
                all_ranks[c].append(n)
                n+=1 
            f.write("######################## Simulation nr " + str(i+1)+ " ########################\n")
            f.write(counter.__str__())
            f.write("\n\n")
        
        max_counters =  {p[0]:int(max(p[1])) for p in all_counters.items()}
        min_counters =  {p[0]:int(min(p[1])) for p in all_counters.items()}  
        mean_counters = {p[0]:int(round(sum(p[1])/n_simulations)) for p in all_counters.items()}

        if counter_type==0:
            max_values = {p[0]:int((round(max(p[1]))*1/aux)) for p in all_counters.items()}
            min_values = {p[0]:int((round(min(p[1]))*1/aux)) for p in all_counters.items()}
            mean_values = {p[0]:int(round(p[1])*1/aux) for p in mean_counters.items()}
        elif counter_type==1:
            max_values = {p[0]:int(round((math.pow(aux,max(p[1]))-aux+1)/(aux-1))) for p in all_counters.items()}
            min_values = {p[0]:int(round((math.pow(aux,min(p[1]))-aux+1)/(aux-1))) for p in all_counters.items()}
            mean_values = {p[0]:int(round((math.pow(aux,p[1])-aux+1)/(aux-1))) for p in mean_counters.items()}

        
        max_abs_error={p[0]:int(max(p[1])) for p in all_abs_error.items()}
        min_abs_error={p[0]:int(min(p[1])) for p in all_abs_error.items()}           
        mean_abs_error = {p[0]:int(round(sum(p[1])/n_simulations)) for p in all_abs_error.items()}   

        max_rel_error={p[0]:max(p[1]) for p in all_rel_error.items()}
        min_rel_error={p[0]:min(p[1]) for p in all_rel_error.items()} 
        mean_rel_error = {p[0]:(sum(p[1])/n_simulations) for p in all_rel_error.items()}           
        
        max_ranks = {p[0]:int(max(p[1])) for p in all_ranks.items()}
        min_ranks = {p[0]:int(min(p[1])) for p in all_ranks.items()}
        mean_ranks = {p[0]:int(round(sum(p[1])/n_simulations)) for p in all_ranks.items()}
        
        max_acc_ratio ={p[0]:max(p[1]) for p in all_acc_ratio.items()}
        min_acc_ratio ={p[0]:min(p[1]) for p in all_acc_ratio.items()} 
        mean_acc_ratio={p[0]:sum(p[1])/n_simulations for p in all_acc_ratio.items()}
        
            
            
        tableHeader = ['Char','Counter Value','Expected Value','Real Value','Expected Rank','Real Rank','Accuracy Ratio','Absolute Error','Relative Error']
        
        ordered_avg_values=sorted(mean_values.items(), key=lambda x: x[1], reverse=True)
        table_arr=[]
        for t,_ in ordered_avg_values:
            counterstring = str(min_counters[t]) + " / " + str(mean_counters[t]) + " / " + str(max_counters[t])
            valuestring = str(min_values[t]) + " / " + str(mean_values[t]) + " / " + str(max_values[t])
            rankstring = str(min_ranks[t]) + " / " + str(mean_ranks[t]) + " / " + str(max_ranks[t])
            accstring = str(round(min_acc_ratio[t],2)) + "% / " + str(round(mean_acc_ratio[t],2)) + "% / " + str(round(max_acc_ratio[t],2)) + "%"
            abserrstring = str(min_abs_error[t]) + " / " + str(mean_abs_error[t]) + " / " + str(max_abs_error[t])
            relerrstring = str(round(min_rel_error[t],2)) + "% / " + str(round(mean_rel_error[t],2)) + "% / " + str(round(max_rel_error[t],2)) + "%"
            row=[t,counterstring,valuestring,test_chain.exact_count[t],rankstring,test_chain.ranks[t],accstring,abserrstring,relerrstring]
            table_arr.append(row)
            #print(counterstring)

    with open("../testdata/" + path + "stats.txt","w",encoding="utf-8") as f2:    
        if counter_type==FPC:            ###################change to globally defined constants
            f2.write("simulating fixed probability counter with p=" + str(aux) + " " + str(n_simulations)  + " times" +" for test chain of size " + str(test_chain.chain_size)+"\n" )
        elif counter_type==LDPC:
            f2.write("simulating logarithmic decreasing probability counter with base=" + str(aux) + " " + str(n_simulations)  + " times"+" for test chain of size " + str(test_chain.chain_size)+"\n" )
        f2.write("######################## Stats across all simulations ########################\n")
        f2.write(tabulate(table_arr,headers=tableHeader))
        f2.write("\nMin/Mean/Max")
        #print(tabulate(table_arr,headers=tableHeader)) 
        
        





import time 
if __name__ == "__main__":
    
    for i in [100,1000,10000,100000,1000000]:
        test_chain = char_chain("rodrigomiguelmaiaferreirarrrrrrrrrroooooo",i)
        
        simulate("fpc"+str(i),test_chain,20,FPC,0.5)
        simulate("ldpc"+str(i),test_chain,20,LDPC,math.sqrt(2))
        print(i ,"complete")
    
    """    
    test_chain = char_chain("rodrigomiguelmaiaferreirarrrrrrrrrroooooo",10000)
    #counter = dec_prob_counter(test_chain,math.sqrt(2))
    #counter2 = prob_counter(test_chain,.5)
    #print(counter)
    #print(counter2)
    simulate("finaltestfpc",test_chain,5,0,0.5)
    simulate("finaltestldpb",test_chain,5,1,math.sqrt(2))
    """
    """
    test_chain = char_chain("rodrigomiguelmaiaferreirarrrrrrrrrroooooo",10000)
    fpctest=prob_counter(test_chain,.5)
    dectest = dec_prob_counter(test_chain,math.sqrt(2))
    print(fpctest)
    print(dectest)
    """