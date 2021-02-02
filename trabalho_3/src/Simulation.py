from LossyCounting import lossycounting_id,lossycounting_sd
from tabulate import tabulate
from math import ceil, floor
from os import listdir
import matplotlib.pyplot as plt
from CharChain import char_chain
from AuxFunctions import initialize_error_dict,average_error_stats,average_error_to_table

DEFAULT_CHAIN_SOURCE_1="abcdefghijklmnopqrstuvwxyz"
DEFAULT_CHAIN_SOURCE_2="aaaaabcdeeeeefghiiiiijklmnooooopqrstuuuuuvwxyz"
DEFAULT_CHAIN_SOURCE_3="xyz"

class sim_run:
    """
    Class containing information regarding the performance of both versions of the lossy counting algorithm for an instance of the problem.
    """
    def __init__(self,path:str, epsilon:float):
        """
        Initializes the class given a path to the chain to be tested and the epsilon to be used.

        Args:
            path (str): Path to the chain to be tested.
            epsilon (float): Epsilon to be used as a parameter for both versions of lossy counting.
        """
        self.path=path
        self.epsilon = epsilon
        self.individual_deltas=lossycounting_id(self.epsilon,self.path)
        self.shared_delta=lossycounting_sd(self.epsilon,self.path)

    def get_id_error_stats(self,s:float)->dict:
        """
        Gets a dictionary with average values for several error metrics acquired from running the individual deltas
        version of the lossy counting algorithm for a certain threshold.

        Args:
            s (float): Threshold to be used.

        Returns:
            dict: Dictionary containing the average values for various error metrics.
        """        
        d = self.individual_deltas.get_frequency(s)
        if not d:
            return None

        stats=initialize_error_dict()
        """
        stats={}
        stats["Absolute Error"]=[]
        stats["Relative Error"]=[]
        stats["False Positive"]=[]
        stats["Rank Misplacement"]=[]
        """
        for item in d:
            stats["Absolute Error"].append(d[item]["Absolute Error"])
            stats["Relative Error"].append(d[item]["Relative Error"])
            stats["False Positive"].append(d[item]["False Positive"])
            stats["Rank Misplacement"].append(abs(d[item]["Exact Rank"]-d[item]["Estimated Rank"])!=0)

        
        
        stats["Absolute Error"] = sum(stats["Absolute Error"])/len(stats["Absolute Error"])
        stats["Relative Error"]= sum(stats["Relative Error"])/len(stats["Relative Error"])
        stats["False Positive"]= sum(stats["False Positive"])
        stats["Rank Misplacement"]=sum(stats["Rank Misplacement"])
        
        return stats

    def get_sd_error_stats(self,s:float)->dict:
        """
        Gets a dictionary with average values for several error metrics acquired from running the shared delta
        version of the lossy counting algorithm for a certain threshold.

        Args:
            s (float): Threshold to be used.

        Returns:
            dict: Dictionary containing the average values for various error metrics.
        """  
        d=self.shared_delta.get_frequency(s)
        if not d:
            return None

        stats=initialize_error_dict()
        """
        stats={}
        stats["Absolute Error"]=[]
        stats["Relative Error"]=[]
        stats["False Positive"]=[]
        stats["Rank Misplacement"]=[]
        """

        for item in d:
            stats["Absolute Error"].append(d[item]["Absolute Error"])
            stats["Relative Error"].append(d[item]["Relative Error"])
            stats["False Positive"].append(d[item]["False Positive"])
            stats["Rank Misplacement"].append(abs(d[item]["Exact Rank"]-d[item]["Estimated Rank"])!=0)

        
        
        stats["Absolute Error"] = sum(stats["Absolute Error"])/len(stats["Absolute Error"])
        stats["Relative Error"]= sum(stats["Relative Error"])/len(stats["Relative Error"])
        stats["False Positive"]= sum(stats["False Positive"])
        stats["Rank Misplacement"]=sum(stats["Rank Misplacement"])
        
        return stats

    def get_error_stats(self,s:float)->(dict,dict):
        """
        Auxiliary function to return both version's average error metric stats.

        Args:
            s (float): Threshold to be used.

        Returns:
            dict,dict: Dictionaries with error metrics for each version of the lossy counting algorithm.
        """
        return self.get_id_error_stats(s),self.get_sd_error_stats(s)


   

    def compare_versions(self,s: float)->dict:
        """
        Compares the performance of both versions of the lossy counting algorithm for a given threshold frequency,

        Args:
            s (float): Threshold to be used.

        Returns:
            dict: Dictionary containing information on the performance of both versions.
        """
        stats_ind = self.individual_deltas.get_frequency(s)
        stats_sha = self.shared_delta.get_frequency(s)

    
        letters = set(list(stats_ind.keys()) + list(stats_sha.keys()))
        comparison = {}
        for k in letters:
            comparison[k]={}
            attributes = set(list(stats_ind.get(k,{}).keys()) + list(stats_sha.get(k,{}).keys()))
            for attr in attributes:
                if "Exact" in attr or "False" in attr:
                    comparison[k][attr] = str(stats_ind.get(k,{}).get(attr,"")) if stats_ind.get(k,{}).get(attr,"")!="" else str(stats_sha.get(k,{}).get(attr,"")) 
                    if "Frequency" in attr:
                        comparison[k][attr] = comparison[k][attr] + "%"
                else:
                    value_1=stats_ind.get(k,{}).get(attr,"None")
                    str_value_1 = value_1 if value_1 =="None" else str(round(value_1,3) )
                    value_2=stats_sha.get(k,{}).get(attr,"None")
                    str_value_2 = value_2 if value_2 =="None" else str(round(value_2,3) )
                    if not "None" in str_value_1 and not "Rank" in attr:
                        str_value_1+="%"
                    if not "None" in str_value_2 and not "Rank" in attr:
                        str_value_2+="%"
                    comparison[k][attr]=str_value_1 + " / " + str_value_2



        return comparison
    
    def compare_versions_table(self,s: float)->str:
        """
        Shows a visual comparison (table) of the performance of both versions of the lossy counting algorithm for a given threshold.

        Args:
            s (float): Threshold to be used.

        Returns:
            str: Table in the form of a string.
        """
        comparison = self.compare_versions(s)
        
        table=[]
        attributes = ["Symbol","Exact Frequency", "Exact Rank", "Estimated Frequency", "Estimated Rank", "False Positive", "Absolute Error", "Relative Error"]
        for k in comparison.keys():
            row=[k]
            #attributes=list(d.get(k).keys())
            for attr in attributes[1:]:
                row.append(comparison.get(k,{}).get(attr,""))
            table.append(row)

        #attributes= ["Symbol"] + attributes
        table.sort(key=lambda x: int(x[2]))
        t = tabulate(table,headers=attributes)
        desc = "\nIndividual Deltas / Shared Delta\n"
        return t + desc


class Full_Simulation:
    """
    Class that entails the full simulation, for every size, epsilon and threshold values.
    """
    def __init__(self,input_sizes, thresholds, epsilons, generate):
        self.input_sizes=input_sizes
        if generate:
            self.generate_chains()

        self.thresholds = thresholds
        self.epsilons=epsilons
        self.run_simulation()


    def run_simulation(self):
        errors_eps_ind={}
        errors_eps_sha={}
        for eps in self.epsilons:
            errors_eps_ind[eps]={}
            errors_eps_sha[eps]={}
            print("Simulating results for epsilon " + str(eps) + "...")
            err_ind,err_sha =self.simulate(eps)
            errors_eps_ind[eps]=err_ind
            errors_eps_sha[eps]=err_sha
        
        self.all_plots(errors_eps_ind,errors_eps_sha)
    
    
    def get_plottable_stats(self,errors_ind,errors_sha, attribute):
        plottable_ind={}
        plottable_sha={}
        for eps in errors_ind:
            plottable_ind[eps] = errors_ind[eps][attribute]
        for eps in errors_sha:
            plottable_sha[eps] = errors_sha[eps][attribute]
        print(plottable_ind)
        print(plottable_sha)
        return plottable_ind,plottable_sha
    
    def plot_stats(self,ind_stats,sha_stats, attribute):
        plt.plot(ind_stats.keys(),ind_stats.values(),label="Individual Deltas")
        plt.plot(sha_stats.keys(),sha_stats.values(),label="Shared Delta")
        plt.title(attribute)
        plt.legend(loc="upper left")
        plt.xlabel("epsilon")
        plt.show()

    def all_plots(self,ind_stats, sha_stats):
        attributes = ["Absolute Error", "Relative Error", "False Positive", "Rank Misplacement"]
        for att in attributes:
            ind,sha = self.get_plottable_stats(ind_stats, sha_stats,att)
            
            self.plot_stats(ind, sha, att)    
    
    
    
    def generate_chains(self)->None:
        """
        Generates the 6 chains used in the tests.
        2 simple ones and 4 achieved by concatenation to simulate more realistic data streams.
        """
        
        for size in self.input_sizes:
            print("Generating chains of size " + str(size) + "...")
            prefix = "../text_files/chain"
            char_chain(DEFAULT_CHAIN_SOURCE_1,size,prefix +"_size_" + str(size) + "_" + str(1) + ".txt")
            char_chain(DEFAULT_CHAIN_SOURCE_2,size,prefix +"_size_" + str(size) + "_" + str(2) + ".txt")
            temp1=char_chain(DEFAULT_CHAIN_SOURCE_1,floor(size/2),prefix +"_size_" + str(size) + "_temp" + str(1) + ".txt")
            temp2=char_chain(DEFAULT_CHAIN_SOURCE_2,ceil(size/2),prefix +"_size_" + str(size) + "_temp" + str(2) + ".txt")
            temp3=char_chain(DEFAULT_CHAIN_SOURCE_3,floor(size/2),prefix +"_size_" + str(size) + "_temp" + str(3) + ".txt" )
            temp1.concatenate(temp2,prefix +"_size_" + str(size) + "_" +str(3) + ".txt")
            temp2.concatenate(temp1,prefix +"_size_" + str(size) + "_" +str(4) + ".txt")
            temp2.concatenate(temp3,prefix +"_size_" + str(size) + "_" +str(5) + ".txt")
            temp3.concatenate(temp2,prefix +"_size_" + str(size) + "_" +str(6) + ".txt")
            temp1.delete_chain()
            temp2.delete_chain()
            temp3.delete_chain()




    def simulate(self,eps: float)->(dict,dict):
        """
        Simulates runs (both versions of the lossy counting) for all chains of the predefined sizes
        testing with different thresholds for a constant epsilon.
        Printing important stats to a file in the test_data folder and returning important error metrics 
        concerning the epsilon used.

        Args:
            eps (float): Constant epsilon to be used in all tests.

        Returns:
            dict,dict: Dictionaries containing important error metrics information for this specific epsilon, one for each lossy counting version.
        """
        with open("../test_data/stats_eps_" + str(eps) + ".txt","w",encoding="utf-8") as f:
            total_error_ind=initialize_error_dict()
            total_error_sha=initialize_error_dict()
            f.write("File containing statistics for chains of various sizes and using various thresholds with constant epsilon " + str(eps) + "\nTotal average stats are at the bottom\n\n")
            for size in self.input_sizes:
                f.write("######################################################################## For chains of size " + str(size) + " ########################################################################\n")
                relevant_chains = self.get_relevant_chains(size)
                
                for i,chain in enumerate(relevant_chains):
                    f.write("##### Chain Number " + str(i+1) + " #####\n\n")
                    local_error_ind=initialize_error_dict()
                    local_error_sha=initialize_error_dict()
                    chain_stats = self.get_chain_stats(chain)
                    f.write(chain_stats + "\n\n")
                    s = sim_run(chain,eps)
                    for threshold in self.thresholds:
                        if threshold >=eps:
                            f.write("For threshold " + str(threshold) + "\n")
                            f.write(s.compare_versions_table(threshold) + "\n")
                            error_ind,error_sha = s.get_error_stats(threshold)
                            if error_ind!=None:
                                for k in local_error_ind:
                                    local_error_ind[k].append(error_ind[k])
                                    total_error_ind[k].append(error_ind[k])
                            if error_sha!=None:
                                for k in local_error_sha:
                                    local_error_sha[k].append(error_sha[k])
                                    total_error_sha[k].append(error_sha[k])
                        else :
                            f.write("Epsilon value " + str(eps) + " is higher than threshold " + str(threshold) + " no output generated.\n")
                    local_error_ind=average_error_stats(local_error_ind)                    
                    local_error_sha=average_error_stats(local_error_sha)
                    average_table = average_error_to_table(local_error_ind,local_error_sha)
                    f.write("Average Errors for chain " + str(i+1) + "\n")
                    f.write(average_table + "\n")
                    
                
            total_error_ind=average_error_stats(total_error_ind)                    
            total_error_sha=average_error_stats(total_error_sha)
            average_table = average_error_to_table(total_error_ind,total_error_sha)
            f.write("Average Errors for eps " + str(eps) + "\n")
            f.write(average_table + "\n")
            

        return total_error_ind,total_error_sha
   
    def get_chain_stats(self,chain_path:str)->str:
        """
        Given the path of a certain character chain, retrieves its description in the form of a string.

        Args:
            chain_path (str): Path to the chain's file.

        Returns:
            str: Description of the chain's main stats.
        """
        text = ""
        with open(chain_path,"r",encoding="utf-8") as f:
            f.readline()
            f.readline()
            while True:
                content=f.readline()
                if not content:
                    break
                text+=content
        return text

    def get_relevant_chains(self,size: int)->list:
        """
        Given a certain size, retrieves a list of the chains of corresponding size, present in the 
        text_files folder.

        Args:
            size (int): Size of the desired chains.

        Returns:
            list: List of paths to the chains of corresponding size.
        """
        relevant_chains=[]
        prefix = "chain_size_" + str(size) + "_"
        for chain in listdir("../text_files/"):
            if prefix in chain:
                relevant_chains.append("../text_files/" + chain)
        return relevant_chains
