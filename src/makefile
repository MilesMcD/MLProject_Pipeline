#Make can be downloaded here: https://www.gnu.org/software/make/
#http://gnuwin32.sourceforge.net/packages/coreutils.htm
#adding this to your path will give you some necessary linux commands.
IRIS_URL = "https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data"
#this will remove any raw data csvs.

#these are not related to file structure.
.PHONY: all clean test

all: data/raw/iris.csv reports/figures/exploratory.png data/processed/processed.pickle models/random_forest.model
#Note: the '-' before rm will mean clean continues despite errors. Remove these for troubleshooting.
#WARN: CLEAN CURRENTLY DELETES MODELS. REMOVE FINALIZED MODELS BEFORE CLEANING THE PROJECT.
clean:
	-rm -f data/raw/*.csv
	-rm -f data/processed/*.pickle
	-rm -f data/processed/*.xlsx
	-rm -f reports/figures/*.png
	-rm -f models/*.model
#test goes up a directory and calls a makefile that tests the size of the dataset.
test: all
	$(MAKE) -C .. all
#python -m pytest src
# $@ = first prerequisite
# $< = first target
data/raw/iris.csv:
	python data/download.py $(IRIS_URL)	$@
reports/figures/exploratory.png: data/processed/processed.pickle
	python visualizations/exploratory.py $< $@
data/processed/processed.pickle: data/raw/iris.csv
	python data/preprocess.py $< $@ --excel data/processed/processed.xlsx
models/random_forest.model: data/processed/processed.pickle
	python models/train_model.py $< $@

	

