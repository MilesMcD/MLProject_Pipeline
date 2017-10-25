# MLProject_Pipeline
	Miles McDowall 10/18/17
Setup:
1. Install the list of dependices outlined by environment.yml (openable in text editor)
2. Install make. Here are some helpful links:
#Make can be downloaded here: https://www.gnu.org/software/make/
#http://gnuwin32.sourceforge.net/packages/coreutils.htm
#adding this to your path will give you some necessary linux commands.


Things that must be changed on a per-dataset/model basis:
	-Download links in src/makefile
	-# of features in exploratory.py dataset: line10, vars
	-type of algorithm; random_forest can be used as a template.
	-If necessary, add new algorithm to the list of options. Also write code servicing it.
	-KMEANS: Remove/dummy out categorical data. Change cluster size.

NOTE: I used jupyter notebook for some mockups of the result. 
	  WARN: Models will be deleted by the 'make clean' command. please exercise caution.
	
TODO:
	LOOK INTO 4 CLUSTER KMEANS FOR HAPPINESS V SUICIDE. I'm interested in cluster 4 in particular.
	Engineer Data on Social Inclusion & Tax Rate/GDP 
		
		Give Preprocess the ability to add missing indices and data points through interpolation.
			How will we do this?:
				We will first add missing indices (years in data sampling)
				We will then interpolate between indices. 
					However, we must not interpolate between countries. 
			
			
	Functionality:
		Improve set_test.py; currently not of much use. (add perfomance requirement?)
		Include data cleaning functions, such as normalization.
		Add Webscraping & Blob download support to download.py

Citing:
tutorial: https://medium.com/towards-data-science/structure-and-automated-workflow-for-a-machine-learning-project-2fa30d661c1e		
By Mateusz Bednarski