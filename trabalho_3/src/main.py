from Simulation import Full_Simulation, Simple_Simulation
from CharChain import char_chain
from LossyCounting import lossycounting_id, lossycounting_sd


LIST_OF_INPUT_SIZES = [100, 1000, 10000, 100000, 1000000, 10000000]
LIST_OF_THRESHOLDS = [0.03, 0.05, 0.10, 0.15, 0.2]
LIST_OF_EPSILONS = [0.0001, 0.001, 0.005, 0.01, 0.05, 0.1]
GENERATE = True
PREFIX = "../text_files/"

if __name__ == "__main__":

    fs = Full_Simulation(
        LIST_OF_INPUT_SIZES, LIST_OF_THRESHOLDS, LIST_OF_EPSILONS, GENERATE
    )

    """
    #BASIC EXAMPLE OF SIMPLE OPERATIONS WITH CHAINS AND LOSSY COUNTING ALGORITHMS
    test_source="abcdeee"
    test_size=50
    test_threshold=0.3
    test_epsilon=0.001
    target_path = PREFIX + "chain_size_" + str(test_size) + "_1.txt"

    c1 = char_chain(test_source,test_size,target_path)
    l1=lossycounting_id(test_epsilon,target_path)
    l2=lossycounting_sd(test_epsilon,target_path)
    print(l1.get_frequency_table(test_threshold))
    print(l2.get_frequency_table(test_threshold))

    #Simple_Simulation class can also be used to quickly compare versions of the algorithm
    
    ss = Simple_Simulation(target_path,test_epsilon)
    print(ss.compare_versions_table(test_threshold))
    """
