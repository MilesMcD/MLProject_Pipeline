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
	-import in train_model.py line 3 &  17; import/use correct algorithm.
	-alter get_features & preprocess_data to include correct # of features.

NOTE: I used jupyter notebook for some mockups of the result. 
	  WARN: Models will be deleted by the 'make clean' command. please exercise caution.
	
TODO:
	Genericization:
		Make train_model.py more generic.
		Generalize preprocess; hard but ideal. Maybe with matrix splicing? (probably)
			namely, get_features, preprocess_data, read_processed_data .
	
	Functionality:
		Improve set_test.py; currently not of much use. (add perfomance requirement?)
		Include data cleaning functions, such as normalization.

Citing:
tutorial: https://medium.com/towards-data-science/structure-and-automated-workflow-for-a-machine-learning-project-2fa30d661c1e		
By Mateusz Bednarski