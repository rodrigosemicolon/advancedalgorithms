Author: Rodrigo Ferreira 104737 rodrigommf@ua.pt

The whole program was built and tested using python 3.9 on windows 10.
The file submitted will contain both chains and results generated from running the simulation with the default parameters on main.

Should the user desire to do everything from scratch, some steps must be followed:
	1.Delete all the chains files in the text_files folder.
	2.Delete all result files in the test_data folder.
	3.Set the desired parameters in main.py with GENERATE = True.
	4.Run the code from the src folder as the current working directory like so:
		python main.py

If the user simply wants to reuse the chains provided but still generate the results, these are the steps:
	1.Delete all result files in the test_data folder.
	2.Set the desired parameters in main.py with GENERATE = False.
	3.Run the code from the src folder as the current working directory like so:
		python main.py

The code gets more complex regarding the Full_Simulation but it is commented and should there be any doubt, feel free to contact me.
The rest of the code tends to be more straight forward.
There is even a simple example of how the char_chain, lossycounting_id, lossycounting_sd and Simple_Simulation interact, commented in main.
The user is invited to play around with this if he so desires by simply commenting the line calling the Full_Simulation class and removing the '"""' comments from the lines below.
To make it more simple, some variables were created to facilitate experimentation (test_source, test_size, test_threshold, test_epsilon and target_path).


It's important to note that the program is built assuming the user will always run it from src/ , the chains will always be in text_files/ and the results in test_data/.
Regardless the full relative path is still supplied to most methods and functions that require it, so the PREFIX in main should be used (more comprehensible looking at the
commented example code). 