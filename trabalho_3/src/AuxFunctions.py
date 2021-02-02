from tabulate import tabulate

def average_error_to_table(error_ind:dict,error_sha:dict)->str:
    """
    Gets the averaged stats of both versions of the lossy counting algorithm and returns a string in the format of
    a table to get a better overview of its stats.

    Args:
        error_ind (dict): Average stats of the individual deltas version.
        error_sha (dict): Average stats of the shared delta version.

    Returns:
        str: Table providing an overview of all stats.
    """
    aux_table  = []
    aux_header = ["Version","Absolute Error", "Relative Error", "False Positive", "Rank Misplacement" ]
    row=["Individual Deltas"]
    for att in error_ind:
                
        row = row + [str(error_ind[att])]
    aux_table.append(row)
    row=["Shared Delta"]
    for att in error_sha:
            
        row = row + [str(error_sha[att])]
    aux_table.append(row)
    tabulated_table= tabulate(aux_table, headers=aux_header) + "\n\n"
        
    return tabulated_table

def initialize_error_dict()->dict:
    """
    Auxiliary function to initialize a dictionary with a specific format to track a simulation's stats.
    Used a lot throughout the simulations.

    Returns:
        dict: Initialized dictionary.
    """
    d={}
    d["Absolute Error"]=[]
    d["Relative Error"]=[]
    d["False Positive"]=[]
    d["Rank Misplacement"]=[]
    return d

def average_error_stats(error_stats:dict)->dict:
    """
    Given a dictionary with a list of stats for each key, it averages the results for each key.

    Args:
        error_stats (dict): Dictionary containing all the information.

    Returns:
        dict: Dictionary containing only average values.
    """
    avg_errors={}
    for metric in error_stats:
        if len(error_stats[metric])!=0:
            avg_errors[metric] = sum(error_stats[metric])/len(error_stats[metric])
    return avg_errors
