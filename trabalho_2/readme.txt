this assignment was done by Rodrigo Ferreira, 104737
made and tested with python 3.9 64-bit
/report/ contains the assignment's report
/src/ contains the code used
/testdata/ contains data collected
	/simulations/ contains each individual counter's simulations
	/stats/ contains statistics that came from the simulations
	/graphics/ contains relevant plots created from the simulated data

to run the code one must only go to the /src/ folder and run in the terminal:
	python main.py
there is a series of parameters which are explained when entered in the terminal:
	python main.py -h

basically, running the code will run all the simulations for the different sized chains,
altering the parameters will still run the simulations but with different values (default
for everything except for those changed)

there is also a special parameter to allow the user to mess around with the code
simply insert the desired code in the section with:
	if free_mode:
        ####################### Insert custom code here #######################
        
then, after saving, run in the terminal:
	python main.py -f 