import random
from math import sqrt,pow,ceil,log
import sys
from tabulate import tabulate
import matplotlib.pyplot as plt

#Global variables
FPC=0
LDPC=1
EXACT=3
DEFAULT_TEST_CHAIN_STRING="rodrigomiguelmaiaferreirarrrrrrrrrroooooo"
DEFAULT_FPC_P=0.5
DEFAULT_LDPC_BASE=2**(1/2)
DEFAULT_N_SIMULATIONS=20
DEFAULT_SIMULATION_STRING_SIZES=[100,500,1000,5000,10000,50000,100000,500000,1000000]

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
    Class that represents a fixed chance probabilistic counter's application on a certain test chain.
    Contains attributes such as the test chain, the chance, the calculated occurrences, estimated occurrences, errors, etc. 
    """
    def __init__(self, char_chain, p):    
        self.char_chain = char_chain
        self.p=p
        self.dict = {} ##the counters
        self.count()
        self.estimated_values = self.get_estimated_values()
        stats = self.get_stats()
        self.absolute_errors = stats[0] 
        self.relative_errors = stats[1]
        self.accuracy_ratios = stats[2]
        tableHeader = ['Char','Counter Value','Estimated Value','Real Value','Estimated Rank','Real Rank','Accuracy Ratio','Absolute Error','Relative Error']
        tableArray=[]
        self.order = sorted(self.dict.items(), key=lambda x: x[1], reverse=True)
        n=1
        for i,_ in self.order:            
            row = [i,self.dict[i],self.estimated_values[i],self.char_chain.exact_count[i],n,self.char_chain.ranks[i],str(self.accuracy_ratios[i]*100) + "%",self.absolute_errors[i],str(self.relative_errors[i]*100) + "%" ]
            tableArray.append(row)
            n+=1
        self.table = tabulate(tableArray,headers=tableHeader)
        
     
    def  count(self):
        for c in self.char_chain.chain:
            if not c in self.dict:
                self.dict[c]=0
            to_add = random.choices([True,False],[self.p,1-self.p])[0]
          
            if to_add:
                self.dict[c] = self.dict[c] + 1
        return self.dict
    
   
            
    def get_estimated_values(self):
        e_val = {}
        for k in self.dict:
            e_val[k] = self.dict[k]*(1/self.p)
        return e_val
    

    def get_relative_error(self):
        rel_error={}   
        for k in self.char_chain.exact_count:
            if self.char_chain.exact_count[k]>0:
                rel_error[k]=abs(self.char_chain.exact_count[k]-self.estimated_values[k])/self.char_chain.exact_count[k]
            else:
                rel_error[k]=0

        return rel_error

    def get_stats(self):
        absolute_errors={}
        relative_errors={}
        accuracy_ratios={}
        for k in self.char_chain.exact_count:
            if self.char_chain.exact_count[k]>0:
                relative_errors[k]=abs(self.char_chain.exact_count[k]-self.estimated_values[k])/self.char_chain.exact_count[k]
                absolute_errors[k]=abs(self.char_chain.exact_count[k]-self.estimated_values[k])
                accuracy_ratios[k]=self.estimated_values[k]/self.char_chain.exact_count[k]
            else:
                relative_errors[k]=0
                absolute_errors[k]=0
                accuracy_ratios[k]=0
        return absolute_errors,relative_errors,accuracy_ratios


    def __str__(self):
        text = "Fixed probabilistic counter with chance: " + str(self.p*100) + "%\n" +self.table +"\n"
        return text


class dec_prob_counter:
    """
    Class that represents a logarithmic decreasing chance probabilistic counter's application on a certain test chain.
    Contains attributes such as the test chain, the base, the calculated occurrences, estimated occurrences, errors, etc. 
    """
    def __init__(self, char_chain,base):    
        self.char_chain = char_chain
        self.base=base
        self.dict = {} ##the counters
        self.count()
        self.estimated_values = self.get_estimated_values()
        stats = self.get_stats()
        self.absolute_errors = stats[0] 
        self.relative_errors = stats[1]
        self.accuracy_ratios = stats[2]
        tableHeader = ['Char','Counter Value','Estimated Value','Real Value','Estimated Rank','Real Rank','Accuracy Ratio','Absolute Error','Relative Error']
        tableArray=[]
        self.order = sorted(self.dict.items(), key=lambda x: x[1], reverse=True)
        n=1
        for i,_ in self.order:            
            row = [i,self.dict[i],self.estimated_values[i],self.char_chain.exact_count[i],n,self.char_chain.ranks[i],str(self.accuracy_ratios[i]*100) + "%",self.absolute_errors[i],str(self.relative_errors[i]*100) + "%" ]
            tableArray.append(row)
            n+=1
        self.table = tabulate(tableArray,headers=tableHeader)
        
       
   
    def  count(self):
        chances={}
        for c in self.char_chain.chain:
            if not c in self.dict:
                self.dict[c]=0
            if not self.dict[c] in chances:
                chances[self.dict[c]]= 1/pow(self.base,self.dict[c])
    
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
                relative_errors[k]=abs(self.char_chain.exact_count[k]-self.estimated_values[k])/self.char_chain.exact_count[k]
                absolute_errors[k]=abs(self.char_chain.exact_count[k]-self.estimated_values[k])
                accuracy_ratios[k]=self.estimated_values[k]/self.char_chain.exact_count[k]
            else:
                relative_errors[k]=0
                absolute_errors[k]=0
                accuracy_ratios[k]=0
        return absolute_errors,relative_errors,accuracy_ratios

    def get_estimated_values(self):
        e_val = {}
        for k in self.dict:
            e_val[k] = round((pow(self.base,self.dict[k]) - self.base + 1)/(self.base-1))            
            
        return e_val
    
    def get_absolute_error(self):
        abs_error={}   
        for k in self.char_chain.exact_count:
            if self.char_chain.exact_count[k]>0:
                abs_error[k]=abs(self.char_chain.exact_count[k]-self.estimated_values[k])
            else:
                abs_error[k]=0

        return abs_error

    def get_relative_error(self):
        rel_error={}   
        for k in self.char_chain.exact_count:
            if self.char_chain.exact_count[k]>0:
                rel_error[k]=abs(self.char_chain.exact_count[k]-self.estimated_values[k])/self.char_chain.exact_count[k]
            else:
                rel_error[k]=0

        return rel_error

    def get_accuracy_ratio(self):
        acc_ratio={}   
        for k in self.char_chain.exact_count:
            if self.char_chain.exact_count[k]>0:
                acc_ratio[k]=self.estimated_values[k]/self.char_chain.exact_count[k]
            else:
                acc_ratio[k]=0

        return acc_ratio


    def __str__(self):
        text = "Logarithmic decreasing probability counter with base: " + str(self.base) + "\n" + self.table + "\n"
        return text


def simulate(path: str,test_chain: char_chain,n_simulations: int,counter_type: int,aux: float)->(dict,dict,dict,dict,dict):
    """
    Method to run multiple simulations of probabilistic counters (FPC or LDPC) on a test chain of characters, and collect stats.
    Also creates 2 files, one containing all the counters simulated and another with an overview of the stats collected across all counters simulated.

    Args:
        path (str): prefix to the files that will be created containing data.
        test_chain (char_chain): chain of characters to be tested.
        n_simulations (int): number of simulations to run.
        counter_type (int): type of counter to run (FPC or LDPC)
        aux (float): p chance in the case of FPC or base in the case of LDPC

    Returns:
        dict,dict,dict,dict,dict: dictionaries containing data on mean: absolute error, accuracy ratio, counters, relative errors and rankings.
    """
    with open("../testdata/simulations/" + path + ".txt","w",encoding="utf-8") as f:
        
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
            max_values = {p[0]:int(round((pow(aux,max(p[1]))-aux+1)/(aux-1))) for p in all_counters.items()}
            min_values = {p[0]:int(round((pow(aux,min(p[1]))-aux+1)/(aux-1))) for p in all_counters.items()}
            mean_values = {p[0]:int(round((pow(aux,p[1])-aux+1)/(aux-1))) for p in mean_counters.items()}

        
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
        
            
            
        tableHeader = ['Char','Counter Value','Estimated Value','Real Value','Estimated Rank','Real Rank','Accuracy Ratio','Absolute Error','Relative Error']
        
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
            

    with open("../testdata/stats/" + path + ".txt","w",encoding="utf-8") as f2:    
        if counter_type==FPC:           
            f2.write("simulating fixed probability counter with p=" + str(aux) + " " + str(n_simulations)  + " times" +" for test chain of size " + str(test_chain.chain_size)+"\n" )
        elif counter_type==LDPC:
            f2.write("simulating logarithmic decreasing probability counter with base=" + str(aux) + " " + str(n_simulations)  + " times"+" for test chain of size " + str(test_chain.chain_size)+"\n" )
        f2.write("######################## Stats across all simulations ########################\n")
        f2.write(tabulate(table_arr,headers=tableHeader))
        f2.write("\nMin/Mean/Max")
       
        
        
    
    return mean_abs_error,mean_acc_ratio,mean_counters,mean_rel_error,mean_ranks


def plot_relative_error(relative_errors: dict)->None:
    """
    Plot the average relative errors for the various types of counters for various input sizes.

    Args:
        relative_errors (dict): dictionary containing average relative errors for the various counters for various test_chain sizes
    """
    average_rel_FPC={}
    average_rel_LDPC={}
    for k in relative_errors[FPC]:
        average_rel_FPC[k] = sum(relative_errors[FPC][k].values())/len(relative_errors[FPC][k])
        average_rel_LDPC[k] = sum(relative_errors[LDPC][k].values())/len(relative_errors[LDPC][k])
    
    plt.plot(average_rel_FPC.keys(),average_rel_FPC.values(),label="FPC")
    plt.plot(average_rel_LDPC.keys(),average_rel_LDPC.values(),label="LDPC")
    plt.title("Relative Error evolution for String size n")
    plt.xlabel("n")
    plt.ylabel("%")
    plt.xticks(list(relative_errors[FPC].keys()),rotation=70)
    plt.legend(loc="upper left")
    plt.savefig("../testdata/graphics/relative_error.png")
    plt.show()








def plot_absolute_error(absolute_errors: dict)->None:
    """
    Plot the average absolue error for the various types of counters for inputs of different sizes.

    Args:
        absolute_errors (dict): dictionary containing average absolute errors for the various counters for various test_chain sizes
    """
    average_abs_FPC={}
    average_abs_LDPC={}
    for k in absolute_errors[FPC]:
        average_abs_FPC[k] = sum(absolute_errors[FPC][k].values())/len(absolute_errors[FPC][k])
        average_abs_LDPC[k] = sum(absolute_errors[LDPC][k].values())/len(absolute_errors[LDPC][k])

    plt.plot(average_abs_FPC.keys(),average_abs_FPC.values(),label="FPC")
    plt.plot(average_abs_LDPC.keys(),average_abs_LDPC.values(),label="LDPC")
    plt.title("Absolute Error evolution for string size n")
    plt.xlabel("n")
    plt.ylabel("events")
    plt.xticks(list(absolute_errors[FPC].keys()),rotation=70)
    plt.legend(loc="upper left")
    plt.savefig("../testdata/graphics/absolute_error.png")
    plt.show()


def plot_accuracy_ratio(accuracy_ratios:dict)->None:
    """
    Plot the average accuracy ratios for the various types of counters for inputs of different sizes.

    Args:
        accuracy_ratios (dict): dictionary containing average accuracy ratios for the various counters for various test_chain sizes
    """
    average_acc_FPC={}
    average_acc_LDPC={}
    for k in accuracy_ratios[FPC]:
        average_acc_FPC[k] = sum(accuracy_ratios[FPC][k].values())/len(accuracy_ratios[FPC][k])
        average_acc_LDPC[k] = sum(accuracy_ratios[LDPC][k].values())/len(accuracy_ratios[LDPC][k])

    plt.plot(average_acc_FPC.keys(),average_acc_FPC.values(), label="FPC")
    plt.plot(average_acc_LDPC.keys(),average_acc_LDPC.values(),label="LDPC")
    plt.title("Accuracy ratio evolution for string size n")
    plt.xlabel("n")
    plt.ylabel("%")
    plt.xticks(list(accuracy_ratios[FPC].keys()),rotation=70)
    plt.legend(loc="upper left")
    plt.savefig("../testdata/graphics/accuracy_ratio.png")
    plt.show()

def plot_counter_size(average_counters:dict)->None:
    """
    Plot the amount of bits needed to represent the average counters of each type of counter

    Args:
        average_counters (dict): dictionary containing average counter values for the various counters for various test_chain sizes
    """
    average_counter_size_FPC={}
    average_counter_size_LDPC={}
    exact_counter_digits = {}
    
    for k in average_counters[FPC]:
        average_counter_size_FPC[k] = ceil(log(sum(average_counters[FPC][k].values())/len(average_counters[FPC][k]),2))
        average_counter_size_LDPC[k] = ceil(log(sum(average_counters[LDPC][k].values())/len(average_counters[LDPC][k]),2))
        exact_counter_digits[k]=ceil(log(sum(average_counters[EXACT][k].values())/len(average_counters[EXACT][k]),2)) 
    
    
    plt.plot(exact_counter_digits.keys(),exact_counter_digits.values(),label="Exact counter")
    plt.plot(average_counter_size_FPC.keys(),average_counter_size_FPC.values(),label="FPC")
    plt.plot(average_counter_size_LDPC.keys(),average_counter_size_LDPC.values(),label="LDPC")
    plt.title("Average counter bits for string size n")
    plt.xlabel("n")
    plt.xticks(list(average_counters[FPC].keys()),rotation=70)
    plt.ylabel("number of bits")
    plt.legend(loc="upper left")
    plt.savefig("../testdata/graphics/bits_required.png")
    plt.show()

if __name__ == "__main__":
    
    args = sys.argv
    free_mode=False
    for i in range(2, len(args)):
        if i % 2 == 0:
            if args[i - 1] == "-nsims":
                nsims = int(args[i])

                if nsims>0:

                    DEFAULT_N_SIMULATIONS = nsims
                else:
                    print("Invalid number of simulations, must be int bigger than 0")
                    sys.exit()
            elif args[i - 1] == "-fpc":
                p = float(args[i])

                if p>0:

                    DEFAULT_FPC_P=p

                else:
                    print("Invalid probability for FPC, must be number bigger than 0")
                    sys.exit()
            elif args[i - 1] == "-ldpc":
                
                base = eval(args[i],{"__builtins__":None},{"sqrt":sqrt,"log":log})
                print(base)              
                if base>0 and base!=1:

                    DEFAULT_LDPC_BASE=base

                else:
                    print("Invalid base for LDPC, must be number bigger than 0 and not 1")
                    sys.exit()
            elif args[i - 1] == "-test_chain":
                src_string = str(args[i])

                if len(src_string)>0:

                    DEFAULT_TEST_CHAIN_STRING=src_string

                else:
                    print("Invalid source string for test chain, must have length bigger than 0")
                    sys.exit()
            elif args[i - 1] == "-chain_sizes":
                
                chain_sizes = eval(args[i],{"__builtins__":None})

                if isinstance(chain_sizes,list) and all(isinstance(item, int) for item in chain_sizes):

                    DEFAULT_SIMULATION_STRING_SIZES=chain_sizes

                else:
                    print("Invalid chain_sizes list")
                    sys.exit()
    if len(args) == 1:
        print("Executing simulations with default values similar to those shown in the report/testdata\n")
        
    elif len(args) == 2 and args[len(args) - 1] == "-h":
        print("\nBy default the program will generate simulations for both counters, of many sizes, to generate data like shown in the report and testdata folder\n"
              "\n"
              "Changing the following parameters will still run the simulations, but with the newly defined values\n"
              "\n\nParameters:\n"
              "-nsims: integer larger than 0 to denote the number of times each counter will be simulated for each test chain (default = 20)\n"
              "-test_chain: string from which the test chains will be built (default = \"rodrigomiguelmaiaferreirarrrrrrrrrroooooo\" )\n"
              "-chain_sizes: list containing the various chain sizes to be simulated (default = [100,500,1000,5000,10000,50000,100000,500000,1000000])\n"
              "-fpc: float larger than 0 which will be used as the probability in the FPC (default = 0.5)\n"
              "-ldpc: string expression (accepts sqrt(n) and log(n) besides the basic expressions) to represent the base for the LDPC which must be larger than 0 (default = 2**1/2) \n"
              "\n"
              "There is also a special parameter that allows the user to run his own code, after inserted in the denoted section in the bottom of the program:\n"
              "\n-f: executes the code inserted by the user in the free_mode section of the program (just -h, no argument needed)\n"
              )
        sys.exit()

    elif len(args) == 2 and args[len(args) - 1] == "-f":
        free_mode=True
        
    
    

    if free_mode:
        ####################### Insert custom code here #######################
        
        print("\n")
    else:
        rel_err={}
        rel_err[FPC]={}
        rel_err[LDPC]={}
        abs_err={}
        abs_err[FPC]={}
        abs_err[LDPC]={}
        acc_ratio={}
        acc_ratio[FPC]={}
        acc_ratio[LDPC]={}
        counters={}
        counters[FPC]={}
        counters[LDPC]={}
        counters[EXACT]={}
        for i in DEFAULT_SIMULATION_STRING_SIZES:
            test_chain = char_chain(DEFAULT_TEST_CHAIN_STRING,i)
            resfpc=simulate("fpc"+str(i),test_chain,DEFAULT_N_SIMULATIONS,FPC,DEFAULT_FPC_P)
            resldpc=simulate("ldpc"+str(i),test_chain,DEFAULT_N_SIMULATIONS,LDPC,DEFAULT_LDPC_BASE)
            rel_err[FPC][i]=resfpc[3]
            rel_err[LDPC][i]=resldpc[3]
            abs_err[FPC][i]=resfpc[0]
            abs_err[LDPC][i]=resldpc[0]
            acc_ratio[FPC][i]=resfpc[1]
            acc_ratio[LDPC][i]=resldpc[1]
            counters[FPC][i]=resfpc[2]
            counters[LDPC][i]=resldpc[2]
            counters[EXACT][i]=test_chain.exact_count
            print(i ,"complete")  
        plot_relative_error(rel_err)
        plot_absolute_error(abs_err)
        plot_accuracy_ratio(acc_ratio)
        plot_counter_size(counters)
        