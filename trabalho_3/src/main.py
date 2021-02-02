"""
from random import choice,randint, uniform
from math import floor, ceil
from tabulate import tabulate
from ast import literal_eval
from string import ascii_lowercase
from os import remove, listdir
"""
from Simulation import Full_Simulation

if __name__=="__main__":

    #simulation([100,1000,10000,100000,1000000,10000000],4,5,[0.05,0.1,0.2,0.30],[0.0001,0.001,0.01,0.05,0.1,0.2],True)
    
    LIST_OF_INPUT_SIZES=[100,1000,10000,100000,1000000,10000000]
    N_PER_SIZE=2
    LIST_OF_THRESHOLDS=[0.03,0.05,0.10,0.15,0.2]
    LIST_OF_EPSILONS=[0.0001,0.001,0.005,0.01,0.05,0.1]




    fs = Full_Simulation([100,1000],LIST_OF_THRESHOLDS,LIST_OF_EPSILONS, False)
