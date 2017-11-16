# MLProject_Pipeline
	Miles McDowall 10/18/17
Setup:
1. Install the list of dependices outlined by environment.yml (openable in text editor)
2. Install make. Here are some helpful links:
#Make can be downloaded here: https://www.gnu.org/software/make/
#http://gnuwin32.sourceforge.net/packages/coreutils.htm
#adding this to your path will give you some necessary linux commands.



USING THIS PIPELINE:
	First Run:
	-Download links in src/makefile
	-Check for project dependencies outlined in the environment.yml file (openable in text editor)
	
	Downloading:
	-I have included download makefile commands where possible, but several sites use "blob URLs" that I have not yet been able to successfully webscrape. I apologize for the inconvenience, but their parent pages have been provided at the top of the makefile.
	
	Using the MAKEFILE: 
	-format:
		dir/whatever/create_this_file(output):[tab]dir/whatever/required_file(input)
		[tab]python dir/scriptname $< $@ --options=whatever --options2=whatever --excel pathname/if/you/want/one.xlsx
		
	Basically the $< specifies the "prerequisite" (input file) and $@ specifies the "target" (output file) so data joiner will require one in between these representing input 2 as a relative path.
	Tabs are necessary or it will break. Never use "make clean".
	
	When you want to use your makefile command, it's as simple as calling "make [target (output file)]" in the src directory.
	Please check documentation for UNFINISHED warnings in scripts. They are liable to require hardcoded inputs.
	
	Algorithm Specific:
	-If necessary, add new algorithm to the list of options. Also write code servicing it.
	-KMEANS: Remove/dummy out categorical data. Change cluster size.
	
	
	EXAMPLE WORKFLOW:
		First, we grab a raw csv and convert it into a partially processed set we'll put in the "interim" folder. 
		We've sorted the data by country and year (in columns 0 and 2) and read the header from row 0 in the csv. 
		We use --excel [pathname] to generate a spreadsheet copy to review visually.
	
	data/interim/happinessladder.pickle: data/raw/happiness-cantril-ladder.csv
	python data/preprocess.py --csvheader=0  --multi="0,2" $< $@ --excel data/interim/happinessladder.xlsx
	
		Next, we merge the dataset with one I have already created. I pass happinessladder.pickle between the prereq & target
		as input file #2. Again, I review my output file in an excel sheet. 
	
data/interim/HapReportHappy.pickle: data/processed/mergedSet.pickle
	python data/data_joiner.py $< data/interim/happinessladder.pickle $@ --excel data/interim/HapReportHappy.xlsx
	
		Finally, I decide to interpolate the resulting dataset. As it's in pickle format, I make sure to used
		--preprocessed=True to read it in correctly.
		
data/processed/HapReportHappy_Interp.pickle: data/interim/HapReportHappy.pickle
	python data/preprocess.py $< $@ --intrpl=True --preprocessed=True --excel data/processed/HapReportHappy_Interp.xlsx 


	
TODO:
	
	1. Examine other interpolation methods.
		Create more figures for interpolated & uninterpolated data
		
		Improve Preprocess interpolation functions
			Something better than linear interpolation
			Back fill(?)
			Consider just imputing mean values from the set (?)
		
	2. Documentation
		At Method & Script Level
		
		Basic Project flow for developing Data Sets. (In Readme)
	
	3. Implement better tuning functionality for our learning algorithms.
	
	FRIDAY: 
		Literature to read
		https://www.econstor.eu/bitstream/10419/26439/1/577841831.PDF
	BY 10 PM !!!!!
	WEEKLY REPORT:
		-Scientific Question
			Working Hypothesis
		-Data sets (used, problems w/in dataset)
			-Methods used to analyze data set_test
		-Results obtained
		-Interpreted results.
	
	
	
	Functionality:
		Improve set_test.py; currently not of much use. (add perfomance requirement?)
		Include data cleaning functions, such as normalization.
		Transforms
		Add Webscraping & Blob download support to download.py

Citing:
tutorial: https://medium.com/towards-data-science/structure-and-automated-workflow-for-a-machine-learning-project-2fa30d661c1e	
stripping whitespace & alphabets: https://stackoverflow.com/questions/4071396/split-by-comma-and-strip-whitespace-in-python	
By Mateusz Bednarski