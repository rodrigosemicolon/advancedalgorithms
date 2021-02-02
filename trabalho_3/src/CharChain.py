from random import choice
from os import remove
from tabulate import tabulate

DEFAULT_CHAR_BREAK = " "

class char_chain:
    """
    Class that represents the test chains of characters. 
    Contains attributes such as the source string, size, the generated chain and exact counters.
    The chain is automatically printed to a file separated only by spaces, once complete, a "\n" is inserted
    and some stats are displayed below.
    """
    def __init__(self,source_string: str,chain_size: int, path: str):
        """
        Initiates the character chain.

        Args:
            source_string (str): String to pick letters from.
            chain_size (int): Size of the chain to be generated.
            path (str): Path to the file that will contain the chain and its stats.
        """
       
        self.source_string=source_string
        self.chain_size=chain_size
        self.exact_count={}
        self.path=path
        with open(self.path, "w", encoding="utf-8") as f:
            for _ in range(chain_size):
                nextChar = choice(source_string)
                f.write(nextChar + DEFAULT_CHAR_BREAK)
                if not nextChar in self.exact_count:
                    self.exact_count[nextChar]=0
                self.exact_count[nextChar] = self.exact_count[nextChar]+1
            f.write("\n\n")
        self.order = sorted(self.exact_count.items(), key=lambda x: (-x[1],x[0]), reverse=False)
        self.ranks = self.get_ranks()
        self.to_file()
    
    def delete_chain(self)->None:
        """
        Deletes this chains files.
        """
        remove(self.path)
   

    def to_file(self)->None:
        """
        Outputs this chain's information to its text file.
        """
        
        with open(self.path,"a",encoding="utf-8") as f:
            f.write(str(self))

    def get_ranks(self)->dict:
        """
        Gets a dictionary with the items and their respective ranks according to their frequencies, ties are solved alphabetically.

        Returns:
            dict: Dictionary mapping items to their rank.
        """
        ranks = {}
        n=1
        for i in self.order:
            ranks[i[0]] = n
            n+=1
        return ranks

    def concatenate(self,other_chain: 'char_chain', path: str)->None:
        """
        Concatenates the current chain with another.

        Args:
            other_chain (char_chain): Chain to be concatenated with this one.
            path (str): Path to the resulting chain.
        """        
        with open(path, "w", encoding="utf-8") as fw:
            with open(self.path,"r",encoding="utf-8") as f1:

              
                i  = f1.readline()[:-1]
                fw.write(i)

            with open(other_chain.path,"r",encoding="utf-8") as f2:

                
                i=f2.readline()[:-1]
                fw.write(i)

            fw.write("\n\n")
           
            exact_count={}
            for val in self.exact_count:
                exact_count[val]=self.exact_count[val]
            for occurrence in other_chain.exact_count:
                
                exact_count[occurrence] = self.exact_count.get(occurrence,0) + other_chain.exact_count[occurrence]
            source_string = self.source_string +" + " + other_chain.source_string
            chain_size = self.chain_size + other_chain.chain_size
            order = sorted(exact_count.items(), key=lambda x: (-x[1],x[0]), reverse=False)
            ranks = {}
            n=1

            for i in order:
                ranks[i[0]] = n
                n+=1

            txt = ("Source String:" + str(source_string)
                    + "\nN:" + str(chain_size)
                    + "\nExact Counts:" + str(exact_count)
                    + "\nExact Ranks:" + str(ranks)
                    + "\n\nTable:\n")

            
            header=["Symbol","Exact Occurrences", "Exact Frequency", "Rank"]
            i=1
            table=[]
            for c,occ in order:
                row=[c,occ,str(100*occ/chain_size) + "%",i]
                table.append(row)
                i+=1


            
            full_page=txt + tabulate(table,headers=header)
            fw.write(full_page)



    def __str__(self):
        txt = ("Source String:" + str(self.source_string)
                + "\nN:" + str(self.chain_size)
                + "\nExact Counts:" + str(self.exact_count)
                + "\nExact Ranks:" + str(self.ranks)
                + "\n\nTable:\n")

        
        header=["Symbol","Exact Occurrences", "Exact Frequency", "Rank"]
        i=1
        table=[]
        for c,occ in self.order:
            row=[c,occ,str(100*occ/self.chain_size) + "%",i]
            table.append(row)
            i+=1
        return txt + tabulate(table,headers=header)
