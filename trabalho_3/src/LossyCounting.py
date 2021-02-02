from math import ceil, floor
from ast import literal_eval
from tabulate import tabulate

class lossycounting_sd:
    """
    Class that represents the implementation of the lossy counting algorithm, more specifically the version with one common delta for every item.
    """
    def __init__(self,epsilon:float,path:str):
        """
        Initiates the class with the desired epsilon and the path to the character chain file.

        Args:
            epsilon (float): Max error percentage accepted (below).
            path (str): Path to the file containing the character chain that will act as a stream of data.
        """
        self.epsilon = epsilon
        self.k=ceil(1/self.epsilon)
        
        self.ranks={}
        self.path = path
        
        self.get_stats()
        self.delta = 0
        self.n = 0
        self.t = {}
        self.__read()
        self.get_ranks()
      


    def get_stats(self)->None:
        """
        Gets the exact stats of the chain to be tested.
        """
        
        with open(self.path,"r",encoding="utf-8") as f:
            f.readline()
            f.readline()
            self.source_string = f.readline().split(":")[-1][:-1]
            self.source_n = int(f.readline().split(":")[-1][:-1])
            self.source_exact_count = literal_eval(f.readline().strip("Exact Counts:")[:-1])
            self.source_ranks = literal_eval(f.readline().strip("Exact Ranks:")[:-1])
    
    def get_ranks(self)->None:
        """
        Method to update the item's ranks based on their estimated frequency.
        """
        i=1
        sorted_keys = sorted(self.t.items(), key=lambda x: (-x[1],x[0]), reverse=False)
        for item in sorted_keys:
            self.ranks[i]=item
            i+=1

    
    def __read(self)->None:
        """
        The actual lossy counting algorithm implementation.
        """
        with open(self.path, "r", encoding="utf-8") as f:
            while True:
                i = f.read(2)
                if "\n" in i:
                    break
                self.n+=1
                i = i[0]
                if i in self.t:
                    self.t[i] = self.t[i] + 1
                else:
                    self.t[i] = 1 + self.delta
                
                latest_delta = floor(self.n/self.k)
                if latest_delta != self.delta:
                    self.delta = latest_delta
                
                    keys = list(self.t.keys())
                    for j in keys:
                        if self.t[j] <self.delta:
                            self.t.pop(j)
                            

  
    def get_frequency(self, s:float)->dict:
        """
        Returns a dictionary with the results for the threshold frequency s.

        Args:
            s (float): Threshold frequency desired.

        Returns:
            dict: Dictionary containing same results.
        """

        
        stats_structure={}
        for ranking in self.ranks:
            item = self.ranks[ranking][0]
            if self.t[item]>=(s - self.epsilon)*self.n:
                stats_structure[item]={}
                real_freq = self.source_exact_count[item]/self.source_n
                est_freq = 100*self.t[item]/self.n
                false_positive = True if real_freq<s else False
                real_freq = 100*real_freq
                stats_structure[item]["Exact Frequency"]=real_freq
                stats_structure[item]["Exact Rank"] = self.source_ranks[item]
                stats_structure[item]["Estimated Frequency"]=est_freq
                stats_structure[item]["Estimated Rank"]=ranking
                stats_structure[item]["False Positive"]=false_positive
                stats_structure[item]["Absolute Error"]=abs(real_freq-est_freq)
                stats_structure[item]["Relative Error"]=100*abs(real_freq-est_freq)/real_freq
                
                
        return stats_structure

    def get_frequency_table(self,s: float)->str:
        """
        Returns the results for a certain threshold but in the form of a table to get a better overview.

        Args:
            s (float): Desired frequency threshold.

        Returns:
            str: String representing the table with the data.
        """
        stats_structure = self.get_frequency(s)
        header = ["Symbol","Exact Rank","Exact Frequency","Estimated Rank", "Estimated Frequency", "False Positive","Absolute Error","Relative Error"]
        table=[]
        desc = ("Lossy Counting implementation with a common shared delta for frequency threshold " 
        + str(s*100) 
        + "%"
        + " and epsilon " 
        + str(self.epsilon*100) 
        + "%\n\n")

        for item in stats_structure:
            table.append([item,str(stats_structure[item]["Exact Rank"])
                                ,str(stats_structure[item]["Exact Frequency"]) + "%"
                                ,str(stats_structure[item]["Estimated Rank"])
                                ,str(stats_structure[item]["Estimated Frequency"]) + "%"
                                ,str(stats_structure[item]["False Positive"])
                                ,str(stats_structure[item]["Absolute Error"]) + "%"
                                ,str(stats_structure[item]["Relative Error"]) + "%"])

        return desc + tabulate(table,headers=header)

class lossycounting_id:
    """
    Class that represents the implementation of the lossy counting algorithm, more specifically the version with an individual delta for each item.
    """
    def __init__(self,epsilon:float,path:str):
        """
        Initiates the class with the desired epsilon and the path to the character chain file.

        Args:
            epsilon (float): Max error percentage accepted (below).
            path (str): Path to the file containing the character chain that will act as a stream of data.
        """
        self.epsilon = epsilon
        self.k=ceil(1/epsilon)
        
        self.ranks={}
        self.path = path
        self.get_stats()
        self.delta = {}
        self.n = 0
        self.t = {}
        self.__read()
        self.get_ranks()
        

    def get_stats(self)->None:
        """
        Gets the exact stats of the chain to be tested.
        """
        
        with open(self.path,"r",encoding="utf-8") as f:
            f.readline()
            f.readline()
            self.source_string = f.readline().split(":")[-1][:-1]
            self.source_n = int(f.readline().split(":")[-1][:-1])
            self.source_exact_count = literal_eval(f.readline().strip("Exact Counts:")[:-1])
            self.source_ranks = literal_eval(f.readline().strip("Exact Ranks:")[:-1])
            
    def __read(self)->None:
        """
        The actual lossy counting algorithm implementation.
        """
        with open(self.path, "r", encoding="utf-8") as f:
            current_bucket=1
            while True:
                i = f.read(2)
                if "\n" in i:
                    break
                self.n+=1
                i = i[0]
                if i in self.t:
                    self.t[i] = self.t[i] + 1
                else:
                    self.t[i] = 1
                    self.delta[i]= current_bucket-1
                
                
                
                
                if self.n%self.k==0:
                    
                    keys = list(self.t.keys())
                    for j in keys:
                        if self.t[j] + self.delta[j] <=current_bucket:
                            
                            self.t.pop(j)
                            self.delta.pop(j)
                    current_bucket+=1
   
    def get_ranks(self)->None:
        """
        Method to update the item's ranks based on their estimated frequency.
        """
        i=1
        sorted_keys = sorted(self.t.items(), key=lambda x: (-x[1],x[0]), reverse=False)
        for item in sorted_keys:
            self.ranks[i]=item
            i+=1

    def get_frequency(self, s:float)->dict:
        """
        Returns a dictionary with the results for the threshold frequency s.

        Args:
            s (float): Threshold frequency desired.

        Returns:
            dict: Dictionary containing same results.
        """


        
        stats_structure={}
        for ranking in self.ranks:
            item = self.ranks[ranking][0]
            if self.t[item]>=(s - self.epsilon)*self.n:
                stats_structure[item]={}
                real_freq = self.source_exact_count[item]/self.source_n
                est_freq = 100*self.t[item]/self.n
                false_positive = True if real_freq<s else False
                real_freq = 100*real_freq
                stats_structure[item]["Exact Frequency"]=real_freq
                stats_structure[item]["Exact Rank"] = self.source_ranks[item]
                stats_structure[item]["Estimated Frequency"]=est_freq
                stats_structure[item]["Estimated Rank"]=ranking
                stats_structure[item]["False Positive"]=false_positive
                stats_structure[item]["Absolute Error"]=abs(real_freq-est_freq)
                stats_structure[item]["Relative Error"]=100*abs(real_freq-est_freq)/real_freq
                
                
        return stats_structure

    def get_frequency_table(self,s: float)->str:
        """
        Returns the results for a certain threshold but in the form of a table to get a better overview.

        Args:
            s (float): Desired frequency threshold.

        Returns:
            str: String representing the table with the data.
        """
        stats_structure = self.get_frequency(s)
        header = ["Symbol","Exact Rank","Exact Frequency","Estimated Rank", "Estimated Frequency", "False Positive","Absolute Error","Relative Error"]
        table=[]
        desc = ("Lossy Counting implementation with individual deltas for frequency threshold " 
        + str(s*100) 
        + "%"
        + " and epsilon " 
        + str(self.epsilon*100) 
        + "%\n\n")

        for item in stats_structure:
            table.append([item,str(stats_structure[item]["Exact Rank"])
                                ,str(stats_structure[item]["Exact Frequency"]) + "%"
                                ,str(stats_structure[item]["Estimated Rank"])
                                ,str(stats_structure[item]["Estimated Frequency"]) + "%"
                                ,str(stats_structure[item]["False Positive"])
                                ,str(stats_structure[item]["Absolute Error"]) + "%"
                                ,str(stats_structure[item]["Relative Error"]) + "%"])

        return desc + tabulate(table,headers=header)